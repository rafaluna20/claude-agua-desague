# -*- coding: utf-8 -*-
"""Orquesta el calculo completo de agua potable de Terra Lima (PRELIMINAR):
   (opcional) importar red desde export de Civil 3D -> demanda -> modelo R1/R2 -> escenarios -> validacion EPANET -> DXF/Excel -> informe.
Uso:  python correr.py [--export export.json] [--red red.json] [--corrida c01] [--set seccion.clave=valor ...]
No hace commit ni modifica archivos fuera de resultados/v3_agua/<corrida>/."""
import argparse, csv, datetime, json, os, re, sys, glob
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import demanda, importar_red, modelo, exportar_dxf, informe
from comun import Parametros, leer_set, escribir_json, sha256, sha_scripts, BASE, dir_corrida


def siguiente_corrida():
    base = os.path.join(BASE, "resultados", "v3_agua")
    n = 1 + max([int(m.group(1)) for d in glob.glob(os.path.join(base, "c*")) for m in [re.match(r"c(\d+)_", os.path.basename(d))] if m] + [0])
    return "c%02d_%s" % (n, datetime.date.today().isoformat())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="JSON de civil3d_export_layer_lines (con la red dibujada)")
    ap.add_argument("--red", help="JSON de red ya convertido (por defecto el de parametros)")
    ap.add_argument("--corrida", help="nombre de la carpeta de salida (por defecto c<nn>_<fecha>)")
    ap.add_argument("--set", nargs="*", default=[], help="cambios de parametros: seccion.clave=valor (JSON)")
    ap.add_argument("--ignorar-terreno", action="store_true", help="no abortar si la grilla del terreno no coincide con el hash esperado")
    ap.add_argument("--permitir-dwg-distinto", action="store_true")
    ap.add_argument("--sin-rotura", action="store_true", help="omitir el escenario de rotura (es el mas lento)")
    a = ap.parse_args(argv)

    P = Parametros(cambios=leer_set(a.set))
    corrida = a.corrida or siguiente_corrida()
    out = dir_corrida(corrida)
    exe = P.datos["archivos"]["epanet_cli"]
    if not os.path.exists(exe):
        sys.exit("COMPUERTA: no se encontro EPANET en %s (instalar con: winget install --id USEPA.EPANET -e)" % exe)
    k2 = P("demanda.k2")
    entradas = {"parametros_agua_potable_v1.json": P.sha[:16]}

    # 1. red
    if a.export:
        r = importar_red.importar(a.export, P, os.path.join(out, "red_agua_importada.json"), a.permitir_dwg_distinto)
        for t in r["avisos"]:
            print("AVISO:", t)
        if not r["ok"]:
            print("COMPUERTA: la red importada no es valida:")
            for t in r["errores"]:
                print("  -", t)
            sys.exit(2)
        red_path = os.path.join(out, "red_agua_importada.json")
        entradas["Export de Civil 3D"] = "%s (%s)" % (sha256(a.export, 16), r["dwg"])
    else:
        red_path = a.red or P.archivo("red_dibujada")
    red = json.load(open(red_path, encoding="utf-8"))
    entradas["Red dibujada (%s)" % os.path.basename(red_path)] = "%s; %s" % (sha256(red_path, 16), str(red.get("_fuente", ""))[:90].replace("|", "/"))

    # 2. terreno (compuerta de hash)
    g_hash = sha256(P.archivo("terreno_grilla"), 64).upper()
    esperado = P.datos["archivos"]["grilla"]["sha256_16"].upper()
    if not g_hash.startswith(esperado):
        msg = "La grilla del terreno (%s...) no coincide con la esperada (%s...)." % (g_hash[:8], esperado)
        if not a.ignorar_terreno:
            sys.exit("COMPUERTA: " + msg + " Si el TIN cambio, vuelva a muestrear (civil3d_sample_surface_grid) y actualice el hash en los parametros; o use --ignorar-terreno.")
        print("AVISO:", msg)
    entradas["Grilla del terreno"] = g_hash[:16]
    entradas["Cotas de lotes"] = sha256(P.archivo("cotas_lotes"), 16)
    entradas["Lotes (parcels_export)"] = sha256(P.archivo("parcels"), 16)

    # 3. demanda
    lotes, dem = demanda.correr(P, out)
    cotas = json.load(open(P.archivo("cotas_lotes")))
    faltan = [l["cod"] for l in lotes if l["cod"] not in cotas]
    if faltan:
        sys.exit("COMPUERTA: %d lotes sin cota en cotas_lotes (ej. %s)" % (len(faltan), faltan[:3]))
    print("Demanda base: %d hab, %.0f m3/d, Qmh %.1f L/s" % (dem["escenarios"]["BASE"]["pob"], dem["escenarios"]["BASE"]["vol_total"], dem["escenarios"]["BASE"]["qmh"]))

    # 4. asignar lotes a la red mas cercana
    grupos = P("reservorios.grupos")
    allp = {}
    for g, caps in grupos.items():
        pts = []
        for s in caps:
            for pl in red[s]:
                for p, q in zip(pl[:-1], pl[1:]):
                    n = max(1, int(np.hypot(q[0] - p[0], q[1] - p[1])))
                    for t in np.linspace(0, 1, n, endpoint=False):
                        pts.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        allp[g] = np.array(pts)
    from scipy.spatial import cKDTree
    cen = np.array([cotas[l["cod"]][:2] for l in lotes])
    nombres = list(grupos)
    dists = np.vstack([cKDTree(allp[g]).query(cen)[0] for g in nombres])
    cual = dists.argmin(0)

    # 5. modelo por red
    terr = modelo.Terreno(P)
    medidor = P("fuente_agua.punto_medidor_xy")
    Rs, resumenes, val = {}, {}, {}
    for gi, g in enumerate(nombres):
        sel = [(l["cod"], cotas[l["cod"]][0], cotas[l["cod"]][1], cotas[l["cod"]][2], l["vol_m3d"]) for k, l in enumerate(lotes) if cual[k] == gi]
        rk = "reservorio" + g[1:]
        pls = [pl for s in grupos[g] for pl in red[s]]
        R = modelo.modelar_red(g, P, pls, red[rk], tuple(red[rk]["c"]), sel, terr, k2, out)
        inp = modelo.escribir_salidas_red(R, P, out, "(DN minimo %s mm)" % P("hidraulica.dn_minimo_mm"))
        val[g] = modelo.validar_con_epanet(R, inp, exe)
        R["pob"] = sum(l["pob"] for k, l in enumerate(lotes) if cual[k] == gi)
        Rs[g] = R
        resumenes[g] = R["resumen"]
        print("%s: %d lotes, Pmin %.1f mca, estatica max %.1f mca, DN %s | EPANET dif %.3f m" % (
            g, R["resumen"]["lotes"], R["resumen"]["presion_min_pico"], R["resumen"]["estatica_max"], R["resumen"]["DN"], val[g]["dif_max_presion_m"]))

    for R in Rs.values():
        R["pob_total"] = sum(x["pob"] for x in Rs.values())

    # 6. escenarios
    esc = dict(volumen=[modelo.volumen_reservorio(R, P) for R in Rs.values()],
               **{"24h": [modelo.escenario_24h(R, P, out, exe) for R in Rs.values()]},
               bomba=[modelo.escenario_bomba(R, P, medidor) for R in Rs.values()],
               incendio=[modelo.escenario_incendio(R, P) for R in Rs.values()] if (P("demanda.incendio_incluir") and P("demanda.incendio_verificar_hidraulica")) else [],
               rotura=[] if a.sin_rotura else [modelo.escenario_rotura(R, P) for R in Rs.values()])
    if a.sin_rotura:
        esc["rotura"] = [dict(red=g, tramos_evaluados=0, tramos_que_dejan_sin_agua=0, peor_corte=[], peor_presion_sin_corte=[], todos=[]) for g in Rs]
    lotes_presion = [f for R in Rs.values() for f in modelo.presion_por_lote(R)]
    with open(os.path.join(out, "presion_lotes.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lotes_presion[0]))
        w.writeheader()
        w.writerows(lotes_presion)
    rev = modelo.puntos_revisar(Rs, P, lotes, medidor)
    escribir_json(os.path.join(out, "revisar.json"), rev)
    escribir_json(os.path.join(out, "escenarios.json"), esc)
    escribir_json(os.path.join(out, "resultados_modelo.json"), dict(resumenes=resumenes, validacion_epanet=val, parametros_usados=P.tabla_estados()))

    # 7. DXF / Excel
    ex = exportar_dxf.exportar(P, out, rev, lotes_presion, float(os.environ.get("ALTO_TEXTO", 1.0)), tuple(nombres))
    print("DXF:", ex["dxf"], "| entidades", ex["entidades"], "| revisar: %d criticos, %d avisos" % (ex["revisar_criticos"], ex["revisar_avisos"]))

    # 8. informe
    archivos = sorted(os.path.relpath(p, out).replace("\\", "/") for p in glob.glob(os.path.join(out, "**", "*"), recursive=True) if os.path.isfile(p))
    ver = re.search(r"EPANET\s*([\d.]+)", exe)
    informe.escribir(os.path.join(out, "INFORME.md"), dict(
        P=P, demanda=dem, resumenes=resumenes, escenarios=esc, revisar=rev, validacion=val, entradas=entradas, scripts=sha_scripts(),
        corrida=corrida, fecha=datetime.date.today().isoformat(), epanet_version=ver.group(1) if ver else "?", k2=k2,
        lotes_presion=lotes_presion, archivos=archivos + ["INFORME.md"]))
    escribir_json(os.path.join(out, "procedencia.json"), dict(corrida=corrida, fecha=datetime.datetime.now().isoformat(timespec="seconds"),
                  entradas=entradas, scripts=sha_scripts(), parametros_sha256_16=P.sha[:16], cambios=P.cambios))
    print("\nCorrida lista en:", out)
    print("INFORME:", os.path.join(out, "INFORME.md"))
    print("Sin commit: revise los resultados y pida el commit si corresponde.")
    return out


if __name__ == "__main__":
    main()
