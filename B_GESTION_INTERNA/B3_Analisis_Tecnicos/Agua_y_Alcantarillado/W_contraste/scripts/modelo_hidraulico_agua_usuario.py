# -*- coding: utf-8 -*-
"""Modelo hidraulico PRELIMINAR (regimen permanente, Hazen-Williams, metodo del gradiente) de la red de agua
dibujada por el usuario. Dos redes independientes (fronteras cerradas): R1 = sector1; R2 = matriz + sector2..6.
Solver propio (numpy/scipy); NO es EPANET. Diametros: predimensionamiento automatico (supuesto)."""
import json, os, sys, collections, math
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import spsolve

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(B, "resultados", "v2_red_agua_usuario")
os.makedirs(OUT, exist_ok=True)
R = json.load(open(os.path.join(B, "datos/v5_habilitacion_1341/red_agua_sectores_usuario_v1.json")))
L = {l["cod"]: l for l in json.load(open(os.path.join(B, "resultados/v1_demanda_agua_1341/lotes_clasificados_v1.json"), encoding="utf-8"))}
C = json.load(open(os.path.join(B, "datos/v5_habilitacion_1341/topografia/cotas_lotes_terreno_2m_v1.json")))
nx, ny, x0, y0, cs = 523, 308, 308140.0, 8622675.0, 2.0
G = np.fromfile(os.path.join(B, "datos/v5_habilitacion_1341/topografia/terreno_habilitacion_2m_v1.f32"), dtype="<f4").reshape(ny, nx).astype(float)
G[G < -9000] = np.nan


def terr(x, y):
    fx = (x - x0) / cs
    fy = (ny - 1) - (y - y0) / cs
    i = int(np.floor(fx))
    j = int(np.floor(fy))
    if i < 0 or j < 0 or i >= nx - 1 or j >= ny - 1:
        return float("nan")
    a = fx - i
    b = fy - j
    v = [G[j, i], G[j, i + 1], G[j + 1, i], G[j + 1, i + 1]]
    if any(np.isnan(v)):
        return float("nan")
    return v[0] * (1 - a) * (1 - b) + v[1] * a * (1 - b) + v[2] * (1 - a) * b + v[3] * a * b


K2 = float(os.environ.get("K2", 2.5))
TOL = 1.0
PASO = 30.0
NIV = {"R1": (132.7, 134.7), "R2": (118.2, 120.2)}  # Nmin, Nmax (supuestos)
GRUPOS = {"R1": ["sector1"], "R2": ["matriz", "sector2", "sector3", "sector4", "sector5", "sector6"]}
SALIDA = {"R1": (308306.41, 8622839.35), "R2": (308394.50, 8622884.28)}
DNS = [(90, 0.081), (110, 0.099), (160, 0.144), (200, 0.180), (250, 0.226), (315, 0.285)]  # DN, ID supuesto ~0.9 DN
VMAX = float(os.environ.get("VMAX", 1.2))
GMAX = float(os.environ.get("GMAX", 8.0))


def vol(l):
    if l["clase"] == "Vivienda ordinaria":
        return 6 * 169 / 1000
    if l["clase"] == "Multifamiliar":
        return 84 * 169 / 1000
    if l["clase"].startswith("Comercial"):
        return l["area"] * 0.6 * 6 / 1000
    return 0.0


def seg_pt(p, a, b):
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1)
    q = a + t * ab
    return np.hypot(*(p - q)), t, q


def construir(grupo):
    pls = []
    for s in GRUPOS[grupo]:
        for pl in R[s]:
            pls.append([np.array(v, float) for v in pl])
    for i, P in enumerate(pls):  # union en T: vertices que tocan el interior de otro trazado
        for v in P:
            for j, Q in enumerate(pls):
                if i == j:
                    continue
                for k in range(len(Q) - 1):
                    if min(np.hypot(*(v - Q[k])), np.hypot(*(v - Q[k + 1]))) <= TOL:
                        continue
                    d, t, q = seg_pt(v, Q[k], Q[k + 1])
                    if d <= TOL:
                        Q.insert(k + 1, q.copy())
                        break
    nodos = []

    def nid(p):
        for n, q in enumerate(nodos):
            if np.hypot(*(p - q)) <= TOL:
                return n
        nodos.append(p.copy())
        return len(nodos) - 1

    aristas = {}
    for P in pls:
        for a, b in zip(P[:-1], P[1:]):
            na, nb = nid(a), nid(b)
            if na == nb:
                continue
            key = (min(na, nb), max(na, nb))
            if key not in aristas:
                aristas[key] = (na, nb)
    nodos2 = [n.copy() for n in nodos]
    ed = []
    for (na, nb) in aristas.values():
        Lm = float(np.hypot(*(nodos[nb] - nodos[na])))
        m = max(1, int(math.ceil(Lm / PASO)))
        prev = na
        for t in range(1, m):
            nodos2.append(nodos[na] + (nodos[nb] - nodos[na]) * t / m)
            cur = len(nodos2) - 1
            ed.append((prev, cur, Lm / m))
            prev = cur
        ed.append((prev, nb, Lm / m))
    return np.array(nodos2), ed


def resolver(q, ed, nn, D, fijo, it=80):
    libres = [i for i in range(nn) if i not in fijo]
    idx = {n: k for k, n in enumerate(libres)}
    npipe = len(ed)
    r = np.array([10.67 * Lm / (140 ** 1.852 * D[p] ** 4.871) for p, (a, b, Lm) in enumerate(ed)])
    A12 = np.zeros((npipe, len(libres)))
    A10 = np.zeros((npipe, len(fijo)))
    fk = {n: k for k, n in enumerate(fijo)}
    for p, (a, b, Lm) in enumerate(ed):
        for n, sg in ((a, 1), (b, -1)):
            if n in idx:
                A12[p, idx[n]] = sg
            else:
                A10[p, fk[n]] = sg
    A12 = csr_matrix(A12)
    H0 = np.array([fijo[n] for n in fijo])
    qq = np.array([q[n] for n in libres])
    Q = np.full(npipe, 0.002)
    Hl = np.full(len(libres), float(np.mean(H0)))
    k = 0
    for k in range(it):
        a11 = r * np.abs(Q) ** 0.852 + 1e-9
        Dm = 1.852 * a11
        f1 = a11 * Q - A12 @ Hl - A10 @ H0
        f2 = A12.T @ Q + qq
        Dinv = diags(1 / Dm)
        F = (A12.T @ Dinv @ A12).tocsc()
        dH = spsolve(F, A12.T @ (Dinv @ f1) - f2)
        dQ = Dinv @ (A12 @ dH - f1)
        Hl = Hl + dH
        Q = Q + dQ
        if np.max(np.abs(dQ)) < 1e-9:
            break
    H = np.zeros(nn)
    for n, k2 in idx.items():
        H[n] = Hl[k2]
    for n in fijo:
        H[n] = fijo[n]
    return H, Q, k


lot_ids = list(C)
cen = np.array([C[k][:2] for k in lot_ids])
lv = np.array([vol(L[k]) for k in lot_ids])
lz = np.array([C[k][2] for k in lot_ids])
allp = {g: [] for g in GRUPOS}
for g, ss in GRUPOS.items():
    for s in ss:
        for pl in R[s]:
            for a, b in zip(pl[:-1], pl[1:]):
                n = max(1, int(np.hypot(b[0] - a[0], b[1] - a[1])))
                for t in np.linspace(0, 1, n, endpoint=False):
                    allp[g].append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
dg = {g: cKDTree(np.array(v)).query(cen)[0] for g, v in allp.items()}
grupo_lote = np.where(dg["R1"] < dg["R2"], "R1", "R2")
informe = []
res = {}
for g in ("R1", "R2"):
    nodos, ed = construir(g)
    nn = len(nodos)
    tr = cKDTree(nodos)
    dres, nres = tr.query(SALIDA[g])
    nres = int(nres)
    adj = collections.defaultdict(list)
    for a, b, Lm in ed:
        adj[a].append(b)
        adj[b].append(a)
    vis = {nres}
    st = [nres]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in vis:
                vis.add(v)
                st.append(v)
    aislados = nn - len(vis)
    m = grupo_lote == g
    q = np.zeros(nn)
    asign = tr.query(cen[m])[1]
    for k, n in zip(np.where(m)[0], asign):
        q[n] += K2 * lv[k] / 86400.0
    zn = np.array([terr(*p) for p in nodos])
    grado = np.array([len(adj[i]) for i in range(nn)])
    D = np.array([0.099] * len(ed))
    for ciclo in range(15):
        H, Q, nit = resolver(q, ed, nn, D, {nres: NIV[g][0]})
        v = np.abs(Q) / (np.pi * D ** 2 / 4)
        hl = np.array([10.67 * Lm * abs(Q[p]) ** 1.852 / (140 ** 1.852 * D[p] ** 4.871) for p, (a, b, Lm) in enumerate(ed)])
        grad = hl / np.array([e[2] for e in ed]) * 1000
        cambio = False
        for p in range(len(ed)):
            if (v[p] > VMAX or grad[p] > GMAX) and D[p] < 0.285:
                D[p] = [d for _, d in DNS if d > D[p]][0]
                cambio = True
        if not cambio:
            break
    pr = H - zn
    mask = np.array([i in vis for i in range(nn)])
    Hs, Qs, _ = resolver(np.zeros(nn), ed, nn, D, {nres: NIV[g][1]})
    ps = Hs - zn
    dem = (q > 0) & mask
    out = dict(red=g, lotes=int(m.sum()), nodos=nn, tuberias=len(ed), longitud_m=round(sum(e[2] for e in ed)),
               nodos_aislados_del_reservorio=int(aislados), distancia_salida_a_nodo_m=round(float(dres), 1),
               Qmh_Ls=round(float(q.sum() * 1000), 2), iteraciones=int(nit),
               presion_min_pico=round(float(pr[dem].min()), 1), presion_p5_pico=round(float(np.percentile(pr[dem], 5)), 1),
               presion_mediana_pico=round(float(np.median(pr[dem])), 1),
               nodos_con_demanda=int(dem.sum()), nodos_menos_10=int((pr[dem] < 10).sum()), nodos_menos_15=int((pr[dem] < 15).sum()),
               estatica_max=round(float(ps[mask].max()), 1), nodos_mas_50=int((ps[mask] > 50).sum()),
               v_max=round(float(v.max()), 2), grad_max_m_km=round(float(grad.max()), 1),
               DN=dict(sorted(collections.Counter([min(DNS, key=lambda t: abs(t[1] - d))[0] for d in D]).items())),
               puntas_muertas=int((grado == 1).sum()))
    lotes_g = np.where(m)[0]
    pl_lote = pr[asign]
    peor = sorted(zip(pl_lote, [lot_ids[k] for k in lotes_g], lz[lotes_g]))[:8]
    out["peores_lotes"] = [(i, round(float(p), 1), round(float(z), 1)) for p, i, z in peor]
    p = int(np.argmax(grad))
    out["tubo_mas_cargado"] = dict(Q_Ls=round(abs(Q[p]) * 1000, 2), v=round(float(v[p]), 2),
                                   DN=min(DNS, key=lambda t: abs(t[1] - D[p]))[0], x=round(float(nodos[ed[p][0]][0])), y=round(float(nodos[ed[p][0]][1])))
    out["caudal_salida_reservorio_Ls"] = round(float(sum(abs(Q[p]) for p, (a, b, Lm) in enumerate(ed) if a == nres or b == nres) * 1000), 2)
    out["nivel_min_max_usado"] = NIV[g]
    informe.append(out)
    with open(os.path.join(OUT, "tuberias_%s_K2_%s.csv" % (g, K2)), "w", encoding="utf-8") as fh:
        fh.write("x1,y1,x2,y2,L_m,DN,Q_Ls,v_ms,hf_m_km,p_nodo1_pico,p_nodo2_pico\n")
        for p_, (a_, b_, Lm_) in enumerate(ed):
            fh.write("%.1f,%.1f,%.1f,%.1f,%.1f,%d,%.2f,%.2f,%.1f,%.1f,%.1f\n" % (
                nodos[a_][0], nodos[a_][1], nodos[b_][0], nodos[b_][1], Lm_,
                min(DNS, key=lambda t: abs(t[1] - D[p_]))[0], abs(Q[p_]) * 1000, v[p_], grad[p_], pr[a_], pr[b_]))
    res[g] = dict(lotes=[(lot_ids[k], float(p)) for k, p in zip(lotes_g, pl_lote)])

json.dump(informe, open(os.path.join(OUT, "resultados_modelo_K2_%s_V%s_G%s.json" % (K2, VMAX, GMAX)), "w"), indent=1, ensure_ascii=False)
for o in informe:
    print(json.dumps(o, ensure_ascii=False))
