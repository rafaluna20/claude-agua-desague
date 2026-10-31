# -*- coding: utf-8 -*-
"""Exporta a DXF (para pegar en Civil 3D) y Excel los resultados de EPANET (motor oficial) de las redes R1 y R2.
Capas: EPANET_NODO_P_*, EPANET_NODO_TXT, EPANET_TUBO_DN*, EPANET_TUBO_TXT, EPANET_RESERVORIO y EPANET_REVISAR
(puntas muertas, fronteras, lotes sin tuberia, presiones fuera de rango, aduccion y llenado por bomba)."""
import math, os
from openpyxl import Workbook
from openpyxl.styles import Font
import epanet
from modelo import dn_de_id, tabla_dn

COLOR_DN = {75: 8, 90: 6, 110: 4, 160: 3, 200: 2, 250: 1, 315: 5}


def exportar(P, outdir, revisar, lotes_presion, alto_texto=1.0, redes=("R1", "R2")):
    exe = P.datos["archivos"]["epanet_cli"]
    tab = tabla_dn(P)
    pmin_d = P("hidraulica.presion_min_diseno_mca")
    ents, capas = [], {}

    def capa(nombre, color):
        capas[nombre] = color
        return nombre

    def circulo(layer, x, y, r):
        ents.append("0\nCIRCLE\n8\n%s\n10\n%.3f\n20\n%.3f\n30\n0.0\n40\n%.3f" % (layer, x, y, r))

    def linea(layer, x1, y1, x2, y2):
        ents.append("0\nLINE\n8\n%s\n10\n%.3f\n20\n%.3f\n30\n0.0\n11\n%.3f\n21\n%.3f\n31\n0.0" % (layer, x1, y1, x2, y2))

    def texto(layer, x, y, h, s, rot=0.0):
        ents.append("0\nTEXT\n8\n%s\n10\n%.3f\n20\n%.3f\n30\n0.0\n40\n%.3f\n1\n%s\n50\n%.2f" % (layer, x, y, h, s, rot))

    H = alto_texto
    wb = Workbook()
    wsn = wb.active
    wsn.title = "Nodos"
    wsn.append(["Red", "Nodo", "X (UTM)", "Y (UTM)", "Cota terreno (m)", "Presion hora punta (m.c.a.)", "Demanda (L/s)"])
    wst = wb.create_sheet("Tramos")
    wst.append(["Red", "Tramo", "Nodo inicio", "Nodo fin", "Longitud (m)", "DN (mm)", "Diametro interior supuesto (mm)"])
    resumen = []
    for g in redes:
        inp = os.path.join(outdir, "epanet", "red_%s_punta.inp" % g)
        sec = epanet.leer_inp(inp)
        res = epanet.correr(inp, exe)[0]["nodos"]
        xy = {r[0]: (float(r[1]), float(r[2])) for r in sec["[COORDINATES]"]}
        dem = {r[0]: float(r[2]) for r in sec["[JUNCTIONS]"]}
        cotas = {r[0]: float(r[1]) for r in sec["[JUNCTIONS]"]}
        pmin = 1e9
        for nid, (x, y) in xy.items():
            if nid.startswith("RES_"):
                circulo(capa("EPANET_RESERVORIO", 5), x, y, 7.0)
                texto(capa("EPANET_NODO_TXT", 7), x + 9, y, H * 2, "Reservorio %s - nivel de calculo %.1f m" % (g[1], float(sec["[RESERVOIRS]"][0][1])))
                continue
            p = res[nid][2]
            cota = cotas[nid]
            pmin = min(pmin, p)
            cl = "EPANET_NODO_P_menor15" if p < 15 else "EPANET_NODO_P_15_25" if p < 25 else "EPANET_NODO_P_25_35" if p < 35 else "EPANET_NODO_P_mayor35"
            col = 1 if p < 15 else 2 if p < 25 else 3 if p < 35 else 4
            circulo(capa(cl, col), x, y, 0.8)
            tl = capa("EPANET_NODO_TXT", 7)
            texto(tl, x + 1.2, y + 0.3, H, "C=%.2f" % cota)
            texto(tl, x + 1.2, y - 1.4, H, "P=%.1f mca" % p)
            wsn.append([g, nid, round(x, 2), round(y, 2), round(cota, 2), round(p, 1), round(dem.get(nid, 0), 4)])
        for r in sec["[PIPES]"]:
            pid, a, b, L, D = r[0], r[1], r[2], float(r[3]), float(r[4])
            if pid.startswith("SALIDA"):
                continue
            d = dn_de_id(tab, D / 1000.0)
            x1, y1 = xy[a]
            x2, y2 = xy[b]
            linea(capa("EPANET_TUBO_DN%d" % d, COLOR_DN.get(d, 7)), x1, y1, x2, y2)
            ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            if ang > 90 or ang <= -90:
                ang += 180
            ang = ((ang + 180) % 360) - 180
            s = "L=%.1f m  DN%d" % (L, d)
            w = 0.62 * H * len(s)
            th = math.radians(ang)
            cx, cy = (x1 + x2) / 2 - math.sin(th) * (H * 1.3), (y1 + y2) / 2 + math.cos(th) * (H * 1.3)
            texto(capa("EPANET_TUBO_TXT", 8), cx - w / 2 * math.cos(th), cy - w / 2 * math.sin(th), H, s, ang)
            wst.append([g, pid, a, b, round(L, 1), d, round(D, 0)])
        resumen.append((g, len([n for n in xy if not n.startswith("RES_")]), len(sec["[PIPES]"]) - 1, pmin))

    # capa de puntos a revisar
    wsr = wb.create_sheet("Revisar")
    wsr.append(["Tipo", "Red", "Gravedad", "X (UTM)", "Y (UTM)", "Detalle"])
    cr = capa("EPANET_REVISAR", 6)
    for it in sorted(revisar, key=lambda i: (i["gravedad"], i["tipo"])):
        circulo(cr, it["x"], it["y"], 3.0 if it["gravedad"] == 1 else 2.0)
        texto(cr, it["x"] + 3.5, it["y"] + 1.0, H * 1.2, "REVISAR: " + it["texto"])
        wsr.append([it["tipo"], it["red"], "critico" if it["gravedad"] == 1 else "aviso", round(it["x"], 1), round(it["y"], 1), it["texto"]])

    wsl = wb.create_sheet("Presion por lote")
    wsl.append(["Lote", "Red", "X", "Y", "Cota terreno (m)", "Nodo", "Distancia a nodo (m)", "Presion punta (mca)", "Presion estatica (mca)"])
    for f in lotes_presion:
        wsl.append([f["lote"], f["red"], f["x"], f["y"], f["cota_terreno"], f["nodo"], f["dist_a_nodo_m"], f["presion_punta_mca"], f["presion_estatica_mca"]])

    dxf = ["0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC", "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n%d" % len(capas)]
    for n, c in capas.items():
        dxf.append("0\nLAYER\n2\n%s\n70\n0\n62\n%d\n6\nCONTINUOUS" % (n, c))
    dxf.append("0\nENDTAB\n0\nENDSEC")
    dxf.append("0\nSECTION\n2\nENTITIES\n" + "\n".join(ents) + "\n0\nENDSEC\n0\nEOF")
    os.makedirs(os.path.join(outdir, "civil3d"), exist_ok=True)
    p_dxf = os.path.join(outdir, "civil3d", "red_agua_modelo_epanet.dxf")
    with open(p_dxf, "w", encoding="ascii", errors="replace", newline="\r\n") as f:
        f.write("\n".join(dxf) + "\n")
    for ws in wb.worksheets:
        for c in ws[1]:
            c.font = Font(bold=True)
        ws.freeze_panes = "A2"
    p_xlsx = os.path.join(outdir, "civil3d", "nodos_tramos_revisar.xlsx")
    wb.save(p_xlsx)
    return dict(dxf=p_dxf, xlsx=p_xlsx, resumen=resumen, capas=sorted(capas), entidades=len(ents),
                revisar_criticos=sum(1 for i in revisar if i["gravedad"] == 1), revisar_avisos=sum(1 for i in revisar if i["gravedad"] == 2))
