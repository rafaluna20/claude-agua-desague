# -*- coding: utf-8 -*-
"""Evalua la sectorizacion de agua dibujada por el usuario (sectores de agua.dwg, 2026-10-31). PRELIMINAR."""
import json, numpy as np, collections, os
from scipy.spatial import cKDTree
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
R = json.load(open(os.path.join(B, "datos/v5_habilitacion_1341/red_agua_sectores_usuario_v1.json")))
L = {l["cod"]: l for l in json.load(open(os.path.join(B, "resultados/v1_demanda_agua_1341/lotes_clasificados_v1.json"), encoding="utf-8"))}
C = json.load(open(os.path.join(B, "datos/v5_habilitacion_1341/topografia/cotas_lotes_terreno_2m_v1.json")))
P = json.load(open(os.path.join(B, "datos/v3_48calles/parcels_export.json"), encoding="utf-8"))
nx, ny, x0, y0, c = 523, 308, 308140.0, 8622675.0, 2.0
G = np.fromfile(os.path.join(B, "datos/v5_habilitacion_1341/topografia/terreno_habilitacion_2m_v1.f32"), dtype="<f4").reshape(ny, nx).astype(float); G[G < -9000] = np.nan
def terr(x, y):
    j = int(round((ny - 1) - (y - y0) / c)); i = int(round((x - x0) / c))
    return float(G[j, i]) if 0 <= j < ny and 0 <= i < nx else float("nan")
def vol(l):
    if l["clase"] == "Vivienda ordinaria": return 6 * 169 / 1000
    if l["clase"] == "Multifamiliar": return 84 * 169 / 1000
    if l["clase"].startswith("Comercial"): return l["area"] * 0.6 * 6 / 1000
    return 0.0
import sys
R1_SECS = tuple(a for a in sys.argv[1:] if a.startswith("sector")) or ("sector1", "sector2")
SEC = ["matriz", "sector1", "sector2", "sector3", "sector4", "sector5", "sector6"]
def sample(pls, step=1.0):
    pts = []
    for pl in pls:
        for a, b in zip(pl[:-1], pl[1:]):
            n = max(1, int(np.hypot(b[0] - a[0], b[1] - a[1]) / step))
            for t in np.linspace(0, 1, n, endpoint=False): pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        pts.append(tuple(pl[-1]))
    return np.array(pts) if pts else np.zeros((0, 2))
def length(pls): return sum(np.hypot(b[0] - a[0], b[1] - a[1]) for pl in pls for a, b in zip(pl[:-1], pl[1:]))
S = {s: sample(R[s]) for s in SEC}
T = {s: cKDTree(S[s]) for s in SEC if len(S[s])}
print("== LONGITUDES (m)"); [print(f"{s}: {length(R[s]):.0f} m, {len(R[s])} trazos") for s in SEC]
print("   total", round(sum(length(R[s]) for s in SEC)))
print("\n== CONEXIONES (distancia minima entre trazados, m)")
for i, a in enumerate(SEC):
    for b in SEC[i + 1:]:
        if a in T and b in T:
            d = T[b].query(S[a])[0].min()
            if d < 15: print(f"  {a} - {b}: {d:.1f} m")
# alimentacion de reservorios
for rn in ("reservorio1", "reservorio2"):
    cc = np.array(R[rn]["c"]); print(f"\n{rn}: terreno {terr(*cc):.1f} m; trazos a <=10 m del borde:",
        [s for s in SEC if s in T and abs(T[s].query(cc)[0] - 7) < 3.5])
# lotes
keys = list(P); cen = np.array([C[k][:2] for k in keys]); Z = np.array([C[k][2] for k in keys]); V = np.array([vol(L[k]) for k in keys])
dist = np.vstack([T[s].query(cen)[0] if s in T else np.full(len(keys), 1e9) for s in SEC])
near = dist.argmin(0); dmin = dist.min(0)
print("\n== COBERTURA: distancia del centroide del lote a la tuberia mas cercana (cualquier capa)")
for u in (20, 30, 40, 60, 100): print(f"  <= {u} m: {int((dmin <= u).sum())} lotes ({(dmin <= u).mean() * 100:.0f} %)")
far = [(keys[i], round(dmin[i])) for i in np.argsort(-dmin)[:15]]; print("  mas alejados:", far)
sinc = np.where(dmin > 40)[0]
print(f"  lotes a >40 m: {len(sinc)}; por manzana:", collections.Counter(keys[i][:6] for i in sinc).most_common(12))
print("  area que centroide >40 m: E:", collections.Counter(keys[i][:3] for i in sinc))
# asignacion por sector (solo lotes a <=40 m)
print("\n== LOTES POR SECTOR (asignacion por trazado mas cercano, <=40 m)")
tot = collections.OrderedDict()
for si, s in enumerate(SEC):
    m = (near == si) & (dmin <= 40)
    if not m.any(): print(f"{s}: 0 lotes"); continue
    v = V[m].sum(); qmh = 2.5 * v / 86.4
    print(f"{s}: {m.sum()} lotes | cota {Z[m].min():.1f}-{Z[m].max():.1f} (media {Z[m].mean():.1f}) | {v:.0f} m3/d | Qmh {qmh:.1f} L/s | trazado {length(R[s]):.0f} m ({length(R[s]) / m.sum():.1f} m/lote)")
    tot[s] = m
g1 = np.zeros(len(keys), bool); g2 = np.zeros(len(keys), bool)
for s in R1_SECS:
    if s in tot: g1 |= tot[s]
for s in ("sector1", "sector2", "sector3", "sector4", "sector5", "sector6"):
    if s not in R1_SECS and s in tot: g2 |= tot[s]
mat = (near == 0) & (dmin <= 40)
print(f"matriz mas cercana: {mat.sum()} lotes (no tienen sector) cota {Z[mat].min():.0f}-{Z[mat].max():.0f}" if mat.any() else "matriz: 0 lotes propios")
for nm, g, rn in (("RESERVORIO 1 (" + "+".join(R1_SECS) + ")", g1, "reservorio1"), ("RESERVORIO 2 (resto)", g2, "reservorio2")):
    zt = terr(*R[rn]["c"]); v = V[g].sum()
    zmin, zmax = Z[g].min(), Z[g].max()
    print(f"\n{nm}: {g.sum()} lotes, {v:.0f} m3/d, Qmd {1.3 * v / 86.4:.1f} Qmh {2.5 * v / 86.4:.1f} L/s, reservorio ~{0.25 * v + 0.07 * 1.3 * v:.0f} m3")
    print(f"   cotas lotes {zmin:.1f}-{zmax:.1f}; terreno del reservorio {zt:.1f}")
    nmin = zmax + 15; print(f"   nivel minimo necesario (lote mas alto + 10 m + 5 m perdidas): {nmin:.1f}; max {nmin + 2:.1f}; estatica max {nmin + 2 - zmin:.1f} m; "
                            f"altura sobre el terreno del reservorio: {nmin - zt:+.1f} m")
    for N in (zt + 2, zt + 4, zt + 6):
        print(f"   si Nmin={N:.1f}: lotes <10 m: {(N - Z[g] < 10).sum()}, <15 m: {(N - Z[g] < 15).sum()}, >50 con Nmax={N + 2:.0f}: {(N + 2 - Z[g] > 50).sum()}")
# trazados dentro de lotes
bb = np.array([[min(p[0] for p in P[k]), max(p[0] for p in P[k]), min(p[1] for p in P[k]), max(p[1] for p in P[k])] for k in keys])
def inside(x, y):
    cand = np.where((bb[:, 0] <= x) & (bb[:, 1] >= x) & (bb[:, 2] <= y) & (bb[:, 3] >= y))[0]
    for i in cand:
        p = P[keys[i]]; ins = False; j = len(p) - 1
        for k in range(len(p)):
            xi, yi = p[k]; xj, yj = p[j]
            if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi: ins = not ins
            j = k
        if ins: return keys[i]
    return None
print("\n== TRAZADO QUE ATRAVIESA LOTES (muestreo cada 3 m)")
for s in SEC:
    pts = sample(R[s], 3.0)
    hit = [inside(x, y) for x, y in pts]; n = sum(h is not None for h in hit)
    lots = sorted({h for h in hit if h})
    print(f"  {s}: {n} de {len(pts)} puntos dentro de lotes ({n * 3} m aprox.); lotes: {lots[:12]}{'...' if len(lots) > 12 else ''}")

# ---------- Parte 2: detalle ----------
print("\n\n===== PARTE 2 =====")
# trazos individuales
allpl = [(s, i, pl) for s in SEC for i, pl in enumerate(R[s])]
PTS = [sample([pl]) for _, _, pl in allpl]
TR = [cKDTree(p) for p in PTS]
dd = np.vstack([t.query(cen)[0] for t in TR]); nr = dd.argmin(0); dm2 = dd.min(0)
print("\n-- Lotes por trazado individual en sector1 y sector2 (cota)")
for k, (s, i, pl) in enumerate(allpl):
    if s in ("sector1", "sector2"):
        m = (nr == k) & (dm2 <= 40)
        if m.any(): print(f"  {s} trazo {i}: {m.sum()} lotes, cota {Z[m].min():.1f}-{Z[m].max():.1f} media {Z[m].mean():.1f}; >103 m: {(Z[m] > 103).sum()}; <=100 m: {(Z[m] <= 100).sum()}")
        else: print(f"  {s} trazo {i}: 0 lotes propios (longitud {length([pl]):.0f} m)")
# contactos entre grupo R1 (s1,s2) y el resto
print("\n-- Puntos donde la red de R1 (sector1+2) toca o se acerca (<=12 m) a otras capas")
otros = [k for k, (s, i, pl) in enumerate(allpl) if s not in R1_SECS]
for k, (s, i, pl) in enumerate(allpl):
    if s in R1_SECS:
        for j in otros:
            d, idx = TR[j].query(PTS[k])
            m = d <= 12
            if m.any():
                pts = PTS[k][m]; print(f"  {s}[{i}] con {allpl[j][0]}[{allpl[j][1]}]: min {d.min():.1f} m en ({pts[d[m].argmin()][0]:.0f},{pts[d[m].argmin()][1]:.0f})")
# puntas muertas
print("\n-- Puntas muertas (extremo de trazado a >3 m de cualquier otro trazado o de si mismo)")
dead = collections.defaultdict(list)
for k, (s, i, pl) in enumerate(allpl):
    if np.hypot(pl[0][0] - pl[-1][0], pl[0][1] - pl[-1][1]) < 1: ends = []
    else: ends = [pl[0], pl[-1]]
    for e in ends:
        dmin_o = min([TR[j].query(e)[0] for j in range(len(allpl)) if j != k] + [np.inf])
        # tambien contra su propio trazado salvo el extremo (autointerseccion)
        own = PTS[k]; far = own[np.hypot(own[:, 0] - e[0], own[:, 1] - e[1]) > 6]
        dself = cKDTree(far).query(e)[0] if len(far) else np.inf
        if min(dmin_o, dself) > 3:
            if "reservorio" in s: continue
            dead[s].append((round(e[0]), round(e[1])))
for s in SEC:
    if dead[s]: print(f"  {s}: {len(dead[s])} -> {dead[s]}")
# reservorio 1 alimenta a que
# lotes de la matriz
mm = np.where((near == 0) & (dmin <= 40))[0]
print("\n-- 37 lotes cuyo trazado mas cercano es la matriz:", collections.Counter(keys[i][:6] for i in mm).most_common(8), " dist media", round(float(dmin[mm].mean()), 1))
# perdida indicativa en matriz
def hf(q, D, Lm, Cc=140): return 10.67 * Lm * (q / 1000) ** 1.852 / (Cc ** 1.852 * D ** 4.87)
Lmz = length(R["matriz"])
for q in (15, 30, 45):
    for D in (0.2, 0.25, 0.315):
        print(f"  matriz {Lmz:.0f} m, Q {q} L/s, D {D * 1000:.0f} mm: v {q / 1000 / (np.pi * D ** 2 / 4):.2f} m/s, hf {hf(q, D, Lmz):.2f} m")

print("\n===== PARTE 3: R1 con niveles 132.7/134.7 y propuesta de reasignacion =====")
for u in (45, 40, 35):
    print(f"  R1 actual (462 lotes): estatica > {u} m en Nmax 134.7: {(134.7 - Z[g1] > u).sum()} lotes")
for corte in (100, 103, 105):
    a = g1 & (Z > corte); b = g1 & (Z <= corte)
    v = V[a].sum()
    print(f"  corte {corte} m: R1 se quedaria con {a.sum()} lotes ({v:.0f} m3/d, Qmh {2.5 * v / 86.4:.1f} L/s, reservorio ~{0.25 * v + 0.07 * 1.3 * v:.0f} m3); pasarian a R2: {b.sum()} lotes ({V[b].sum():.0f} m3/d)")
    vv = V[g2 | b | mat].sum(); print(f"     R2 total quedaria: {(g2 | b | mat).sum()} lotes, {vv:.0f} m3/d, Qmd {1.3 * vv / 86.4:.1f} Qmh {2.5 * vv / 86.4:.1f} L/s, reservorio ~{0.25 * vv + 0.07 * 1.3 * vv:.0f} m3; cota max {Z[g2 | b | mat].max():.1f}")
# Qmh toda la zona de R2 si fuera uno
