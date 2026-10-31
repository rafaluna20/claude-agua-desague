# -*- coding: utf-8 -*-
"""Exporta a DXF (Civil 3D) y Excel los resultados de EPANET de las redes R1 y R2.
Nodos: cota (m) y presion (m.c.a.). Tramos: longitud (m) y DN comercial.
Presiones: motor oficial EPANET 2.2 (runepanet.exe) sobre los .inp de resultados/v2_red_agua_usuario/epanet.
PRELIMINAR: hora punta (K2 = 2.5), reservorios en Nmin, diametros de predimensionamiento."""
import os, re, math, subprocess, tempfile, shutil, sys
from openpyxl import Workbook

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INPDIR = os.path.join(B, "resultados", "v2_red_agua_usuario", "epanet")
OUTDIR = os.path.join(B, "resultados", "v2_red_agua_usuario", "civil3d")
os.makedirs(OUTDIR, exist_ok=True)
EPA = r"C:\Program Files (x86)\EPANET 2.2\runepanet.exe"
K2 = sys.argv[1] if len(sys.argv) > 1 else "2.5"
H = float(os.environ.get("ALTO_TEXTO", 1.0))  # altura de texto en metros de dibujo
DN_DE_ID = [(81, 90), (99, 110), (144, 160), (180, 200), (226, 250), (285, 315)]
COLOR_DN = {90: 6, 110: 4, 160: 3, 200: 2, 250: 1, 315: 5}


def dn(idmm):
    return min(DN_DE_ID, key=lambda t: abs(t[0] - idmm))[1]


def leer_inp(path):
    sec, cur = {}, None
    for l in open(path, encoding="ascii", errors="replace"):
        l = l.rstrip("\n")
        if l.startswith("["):
            cur = l.strip()
            sec[cur] = []
        elif l.strip() and not l.startswith(";") and cur:
            sec[cur].append(l.split())
    return sec


def correr_epanet(inp):
    tmp = tempfile.mkdtemp()
    t = open(inp, encoding="ascii").read().replace("Status No", "Status Yes").replace("Summary No", "Summary Yes\nNodes ALL\nLinks ALL")
    ti = os.path.join(tmp, "t.inp")
    open(ti, "w", encoding="ascii").write(t)
    r = subprocess.run([EPA, ti, os.path.join(tmp, "t.rpt")], capture_output=True, text=True)
    rpt = open(os.path.join(tmp, "t.rpt"), encoding="latin-1").read()
    shutil.rmtree(tmp, ignore_errors=True)
    nodes = rpt.split("Node Results")[1].split("Link Results")[0]
    pres = {}
    for l in nodes.splitlines():
        m = re.match(r"^\s*(\S+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*$", l)
        if m:
            pres[m.group(1)] = (float(m.group(3)) - float(m.group(4)), float(m.group(4)))  # cota, presion
    return pres


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


wb = Workbook()
wsn = wb.active
wsn.title = "Nodos"
wsn.append(["Red", "Nodo", "X (UTM)", "Y (UTM)", "Cota terreno (m)", "Presion hora punta (m.c.a.)", "Demanda (L/s)"])
wst = wb.create_sheet("Tramos")
wst.append(["Red", "Tramo", "Nodo inicio", "Nodo fin", "Longitud (m)", "DN (mm)", "Diametro interior supuesto (mm)"])
resumen = []
for g in ("R1", "R2"):
    inp = os.path.join(INPDIR, "red_%s_K2_%s.inp" % (g, K2))
    sec = leer_inp(inp)
    pres = correr_epanet(inp)
    xy = {r[0]: (float(r[1]), float(r[2])) for r in sec["[COORDINATES]"]}
    dem = {r[0]: float(r[2]) for r in sec["[JUNCTIONS]"]}
    pmin = 1e9
    for nid, (x, y) in xy.items():
        if nid.startswith("RES_"):
            c = capa("EPANET_RESERVORIO", 5)
            circulo(c, x, y, 7.0)
            texto(capa("EPANET_NODO_TXT", 7), x + 9, y, H * 2, "Reservorio %s - nivel de calculo %.1f m" % (g[1], float(sec["[RESERVOIRS]"][0][1])))
            continue
        cota, p = pres[nid]
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
        d = dn(D)
        x1, y1 = xy[a]
        x2, y2 = xy[b]
        linea(capa("EPANET_TUBO_DN%d" % d, COLOR_DN[d]), x1, y1, x2, y2)
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
    resumen.append((g, len([n for n in xy if not n.startswith('RES_')]), len(sec["[PIPES]"]) - 1, pmin))

dxf = ["0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n0\nENDSEC", "0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n%d" % len(capas)]
for n, c in capas.items():
    dxf.append("0\nLAYER\n2\n%s\n70\n0\n62\n%d\n6\nCONTINUOUS" % (n, c))
dxf.append("0\nENDTAB\n0\nENDSEC")
dxf.append("0\nSECTION\n2\nENTITIES\n" + "\n".join(ents) + "\n0\nENDSEC\n0\nEOF")
open(os.path.join(OUTDIR, "red_agua_modelo_epanet_v1.dxf"), "w", encoding="ascii", errors="replace", newline="\r\n").write("\n".join(dxf) + "\n")
for ws in (wsn, wst):
    for c in ws[1]:
        c.font = c.font.copy(bold=True)
    ws.freeze_panes = "A2"
wb.save(os.path.join(OUTDIR, "nodos_y_tramos_v1.xlsx"))
for r in resumen:
    print("Red %s: %d nodos, %d tramos, presion minima %.1f mca" % r)
print("capas:", ", ".join(sorted(capas)))
print("entidades DXF:", len(ents))
