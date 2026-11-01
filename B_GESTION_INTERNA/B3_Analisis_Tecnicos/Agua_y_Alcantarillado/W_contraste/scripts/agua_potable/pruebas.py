# -*- coding: utf-8 -*-
"""Pruebas de regresion del calculo de agua potable. Ejecutar antes de confiar en una corrida nueva o tras cambiar scripts/parametros:
    python pruebas.py
Escribe en resultados/v3_agua/_pruebas (carpeta desechable)."""
import contextlib, io, json, os, sys, tempfile, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import correr, importar_red
from comun import Parametros, BASE

RESULTADOS = []
# Agrupacion del diseno de 2026-10-31 (sector2 con R2) que usan las pruebas contra la red v1 transcrita a mano
GRUPOS_V1 = 'reservorios.grupos={"R1": ["sector1"], "R2": ["matriz", "sector2", "sector3", "sector4", "sector5", "sector6"]}'


def prueba(nombre):
    def deco(f):
        try:
            f()
            RESULTADOS.append((nombre, True, ""))
        except Exception as e:  # noqa
            RESULTADOS.append((nombre, False, "%s: %s" % (type(e).__name__, e)))
            traceback.print_exc()
        return f
    return deco


def correr_silencioso(args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = correr.main(args)
    return out


# ---- 1. parametros
@prueba("Todos los parametros tienen valor, fuente y estado valido")
def _():
    P = Parametros()
    validos = set(P.datos["_meta"]["estados_validos"])
    malos = []
    for sec, d in P.datos.items():
        if sec in ("_meta", "archivos"):
            continue
        for k, n in d.items():
            if not all(c in n for c in ("valor", "fuente", "estado")) or n["estado"] not in validos:
                malos.append(sec + "." + k)
    assert not malos, malos


# ---- 2. regresion contra v1 (DN110) y solver contra EPANET
V1 = {}


@prueba("Con DN minimo 110 se reproducen las cifras de v1 (14.4 / 18.6 mca, estatica 39.7 / 41.7)")
def _():
    out = correr_silencioso(["--corrida", "_pruebas", "--set", "hidraulica.dn_minimo_mm=110", GRUPOS_V1, "--sin-rotura"])
    V1["res"] = json.load(open(os.path.join(out, "resultados_modelo.json"), encoding="utf-8"))
    V1["out"] = out
    ref = json.load(open(os.path.join(BASE, "resultados", "v2_red_agua_usuario", "resultados_modelo_K2_2.5_V1.2_G8.0.json"), encoding="utf-8"))
    ref = {r["red"]: r for r in ref}
    for g in ("R1", "R2"):
        n = V1["res"]["resumenes"][g]
        for k in ("presion_min_pico", "estatica_max", "lotes", "nodos"):
            assert abs(n[k] - ref[g][k]) <= 0.15, (g, k, n[k], ref[g][k])
        assert abs(n["Qmh_Ls"] - ref[g]["Qmh_Ls"]) < 0.02, (g, "Qmh")


@prueba("Solver propio coincide con EPANET 2.2 (presion < 0.05 m, caudal < 0.05 L/s)")
def _():
    for g, v in V1["res"]["validacion_epanet"].items():
        assert v["dif_max_presion_m"] < 0.05 and v["dif_max_caudal_Ls"] < 0.05, (g, v)


# ---- 3. piso DN90, 24 h, escenarios
@prueba("Con los parametros por defecto ninguna tuberia baja de DN90 y se cumple la velocidad maxima de diseno")
def _():
    out = correr_silencioso(["--corrida", "_pruebas", "--set", GRUPOS_V1, "--sin-rotura"])
    V1["base"] = out
    for g in ("R1", "R2"):
        for linea in open(os.path.join(out, "tuberias_%s.csv" % g), encoding="utf-8").read().splitlines()[1:]:
            c = linea.split(",")
            assert int(c[5]) >= 90, (g, linea)
            assert float(c[7]) <= 1.2 + 0.01, (g, linea)


@prueba("La simulacion de 24 h coincide con la hora punta (misma presion minima a +-0.15 m (redondeo a 0.1) en la hora de mayor demanda)")
def _():
    esc = json.load(open(os.path.join(V1["base"], "escenarios.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(V1["base"], "resultados_modelo.json"), encoding="utf-8"))["resumenes"]
    for e in esc["24h"]:
        assert len(e["horas"]) == 25 and e["hora_p_min"] != 0, e["hora_p_min"]
        assert abs(e["p_min_global"] - res[e["red"]]["presion_min_pico"]) <= 0.15, (e["red"], e["p_min_global"], res[e["red"]]["presion_min_pico"])


@prueba("Escenario de rotura: en una red en arbol el corte en la salida deja sin agua toda la red")
def _():
    from modelo import escenario_rotura  # noqa
    out = correr_silencioso(["--corrida", "_pruebas", "--set", GRUPOS_V1])
    esc = json.load(open(os.path.join(out, "escenarios.json"), encoding="utf-8"))
    for e in esc["rotura"]:
        assert e["tramos_evaluados"] > 0
        assert max(f["pct_demanda_perdida"] for f in e["peor_corte"]) > 99.0


@prueba("Los 100 m3 de incendio se reparten entre R1 y R2 en proporcion a la poblacion (suma 100) y sin hidrantes no se corre la prueba de gasto coincidente")
def _():
    esc = json.load(open(os.path.join(V1["base"], "escenarios.json"), encoding="utf-8"))
    vols = esc["volumen"]
    assert abs(sum(v["incendio_m3"] for v in vols) - 100.0) < 0.15, vols
    for v in vols:
        assert abs(v["incendio_m3"] - v["pct_pob"]) < 0.15, v
        assert abs(v["total_m3"] - (v["regulacion_m3"] + v["reserva_m3"] + v["incendio_m3"])) <= 1, v
    assert esc["incendio"] == []


# ---- 4. importador
def _export_sintetico(red, dwg, quitar=None):
    P = Parametros()
    mapa = P("reservorios.capas_dibujo")
    capas = {}
    for clave, capa in mapa.items():
        if capa == quitar:
            continue
        if clave.startswith("reservorio"):
            ents = [dict(handle="R", type="Circle", cx=red[clave]["c"][0], cy=red[clave]["c"][1], radius=red[clave]["r"])]
        else:
            ents = [dict(handle=str(i), type="Polyline", closed=False, elevation=0, length=0, vertices=[[x, y, 0.0] for x, y in pl]) for i, pl in enumerate(red[clave])]
        capas[capa] = dict(count=len(ents), typeCounts={}, entities=ents)
    return dict(tool="export_layer_lines v1", dwg=dwg, exportedUtc="2026-10-31T00:00:00Z", layers=capas)


@prueba("El importador reconstruye la red actual a partir de un export en formato de la herramienta del plugin")
def _():
    P = Parametros()
    red = json.load(open(P.archivo("red_dibujada"), encoding="utf-8"))
    ex = _export_sintetico(red, r"C:\x\sectores de agua.dwg")
    tmp = os.path.join(tempfile.gettempdir(), "export_sintetico_agua.json")
    json.dump(ex, open(tmp, "w"))
    r = importar_red.importar(tmp, P)
    assert r["ok"], r["errores"]
    for k in red:
        if k == "_fuente" or k not in P("reservorios.capas_dibujo"):
            continue
        assert r["red"][k] == red[k] or k.startswith("reservorio") and r["red"][k]["c"] == red[k]["c"], k


@prueba("El importador rechaza un DWG equivocado y una capa faltante")
def _():
    P = Parametros()
    red = json.load(open(P.archivo("red_dibujada"), encoding="utf-8"))
    tmp = os.path.join(tempfile.gettempdir(), "export_sintetico_agua2.json")
    json.dump(_export_sintetico(red, r"C:\x\Curvas de Nivel.dwg"), open(tmp, "w"))
    assert not importar_red.importar(tmp, P)["ok"]
    json.dump(_export_sintetico(red, r"C:\x\sectores de agua.dwg", quitar="agua_sector3"), open(tmp, "w"))
    r = importar_red.importar(tmp, P)
    assert not r["ok"] and any("agua_sector3" in e for e in r["errores"])


if __name__ == "__main__":
    print()
    for nombre, ok, msg in RESULTADOS:
        print("%s  %s%s" % ("PASA " if ok else "FALLA", nombre, ("  -> " + msg) if msg else ""))
    fallas = [r for r in RESULTADOS if not r[1]]
    print("\n%d pruebas, %d fallas" % (len(RESULTADOS), len(fallas)))
    sys.exit(1 if fallas else 0)
