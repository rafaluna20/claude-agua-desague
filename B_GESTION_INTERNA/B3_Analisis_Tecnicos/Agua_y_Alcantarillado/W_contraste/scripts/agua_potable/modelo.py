# -*- coding: utf-8 -*-
"""Modelo hidraulico PRELIMINAR (regimen permanente, Hazen-Williams, metodo del gradiente) de las redes R1 y R2.
Solver propio (numpy/scipy) contrastado contra EPANET 2.2 oficial. Escenarios: hora punta, estatica maxima,
rotura de tramo, simulacion de 24 h (EPANET), bomba de llenado y presion por lote.
Todos los parametros salen de parametros_agua_potable_v1.json."""
import collections, json, math, os
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import spsolve
import epanet
from comun import escribir_json


# ------------------------------------------------------------------ terreno
class Terreno:
    def __init__(self, P):
        g = P.datos["archivos"]["grilla"]
        self.nx, self.ny, self.x0, self.y0, self.cs = g["nx"], g["ny"], g["x0"], g["y0"], g["paso_m"]
        self.G = np.fromfile(P.archivo("terreno_grilla"), dtype="<f4").reshape(self.ny, self.nx).astype(float)
        self.G[self.G < -9000] = np.nan

    def __call__(self, x, y):
        fx = (x - self.x0) / self.cs
        fy = (self.ny - 1) - (y - self.y0) / self.cs
        i, j = int(np.floor(fx)), int(np.floor(fy))
        if i < 0 or j < 0 or i >= self.nx - 1 or j >= self.ny - 1:
            return float("nan")
        a, b = fx - i, fy - j
        v = [self.G[j, i], self.G[j, i + 1], self.G[j + 1, i], self.G[j + 1, i + 1]]
        if any(np.isnan(v)):
            return float("nan")
        return v[0] * (1 - a) * (1 - b) + v[1] * a * (1 - b) + v[2] * (1 - a) * b + v[3] * a * b


# ------------------------------------------------------------------ topologia
def _seg_pt(p, a, b):
    ab = b - a
    t = np.clip(np.dot(p - a, ab) / np.dot(ab, ab), 0, 1)
    q = a + t * ab
    return np.hypot(*(p - q)), t, q


def construir(pls_in, tol, paso):
    pls = [[np.array(v, float) for v in pl] for pl in pls_in]
    for i, Pi in enumerate(pls):  # union en T: vertices que tocan el interior de otro trazado
        for v in Pi:
            for j, Q in enumerate(pls):
                if i == j:
                    continue
                for k in range(len(Q) - 1):
                    if min(np.hypot(*(v - Q[k])), np.hypot(*(v - Q[k + 1]))) <= tol:
                        continue
                    d, t, q = _seg_pt(v, Q[k], Q[k + 1])
                    if d <= tol:
                        Q.insert(k + 1, q.copy())
                        break
    nodos = []

    def nid(p):
        for n, q in enumerate(nodos):
            if np.hypot(*(p - q)) <= tol:
                return n
        nodos.append(p.copy())
        return len(nodos) - 1

    aristas = {}
    for Pi in pls:
        for a, b in zip(Pi[:-1], Pi[1:]):
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
        m = max(1, int(math.ceil(Lm / paso)))
        prev = na
        for t in range(1, m):
            nodos2.append(nodos[na] + (nodos[nb] - nodos[na]) * t / m)
            cur = len(nodos2) - 1
            ed.append((prev, cur, Lm / m))
            prev = cur
        ed.append((prev, nb, Lm / m))
    return np.array(nodos2), ed


def alcanzables(nn, ed, inicio, excluir=None):
    adj = collections.defaultdict(list)
    for p, (a, b, _) in enumerate(ed):
        if p == excluir:
            continue
        adj[a].append(b)
        adj[b].append(a)
    vis, st = {inicio}, [inicio]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in vis:
                vis.add(v)
                st.append(v)
    return vis, adj


# ------------------------------------------------------------------ solver
def resolver(q, ed, nn, D, fijo, C, it=80):
    libres = [i for i in range(nn) if i not in fijo]
    idx = {n: k for k, n in enumerate(libres)}
    npipe = len(ed)
    r = np.array([10.67 * Lm / (C ** 1.852 * D[p] ** 4.871) for p, (a, b, Lm) in enumerate(ed)])
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


# ------------------------------------------------------------------ utilidades
def tabla_dn(P):
    return [(int(dn), float(idm)) for dn, idm in P("hidraulica.diametros_comerciales_dn_id_m")]


def dn_de_id(tab, d):
    return min(tab, key=lambda t: abs(t[1] - d))[0]


def id_de_dn(tab, dn):
    return [i for d, i in tab if d == dn][0]


def hf_hw(q_m3s, D, L, C):
    return 10.67 * L * abs(q_m3s) ** 1.852 / (C ** 1.852 * D ** 4.871)


# ------------------------------------------------------------------ modelo por red
def modelar_red(g, P, pls, reservorio, salida_xy, lotes_red, terr, k2, outdir):
    """lotes_red: lista de (cod, x, y, cota, vol_m3d). Devuelve diccionario con todo lo necesario para escenarios y salidas."""
    tol, paso = P("hidraulica.tolerancia_union_m"), P("hidraulica.paso_discretizacion_m")
    C = P("hidraulica.hazen_williams_c")
    tab = tabla_dn(P)
    vmax, gmax = P("hidraulica.velocidad_max_diseno_ms"), P("hidraulica.gradiente_max_m_km")
    nmin, nmax = P("reservorios.niveles_calculo_m")[g]
    nodos, ed = construir(pls, tol, paso)
    nn = len(nodos)
    tr = cKDTree(nodos)
    dres, nres = tr.query(salida_xy)
    nres = int(nres)
    vis, adj = alcanzables(nn, ed, nres)
    cen = np.array([[l[1], l[2]] for l in lotes_red])
    lv = np.array([l[4] for l in lotes_red])
    lz = np.array([l[3] for l in lotes_red])
    dlote, asign = tr.query(cen) if len(cen) else (np.array([]), np.array([], int))
    qp = np.zeros(nn)  # caudal promedio por nodo, m3/s
    for k, n in enumerate(asign):
        qp[n] += lv[k] / 86400.0
    q = k2 * qp
    zn = np.array([terr(*p) for p in nodos])
    zn = np.where(np.isnan(zn), np.nanmean(zn), zn)
    dn_min = int(P("hidraulica.dn_minimo_mm"))
    D = np.array([id_de_dn(tab, dn_min)] * len(ed))
    for ciclo in range(20):
        H, Q, nit = resolver(q, ed, nn, D, {nres: nmin}, C)
        v = np.abs(Q) / (np.pi * D ** 2 / 4)
        hl = np.array([hf_hw(Q[p], D[p], Lm, C) for p, (a, b, Lm) in enumerate(ed)])
        grad = hl / np.array([e[2] for e in ed]) * 1000
        cambio = False
        for p in range(len(ed)):
            if (v[p] > vmax or grad[p] > gmax) and D[p] < tab[-1][1]:
                D[p] = [d for _, d in tab if d > D[p]][0]
                cambio = True
        if not cambio:
            break
    pr = H - zn
    mask = np.array([i in vis for i in range(nn)])
    Hs, Qs, _ = resolver(np.zeros(nn), ed, nn, D, {nres: nmax}, C)
    ps = Hs - zn
    dem = (q > 0) & mask
    grado = np.array([len(adj[i]) for i in range(nn)])
    R = dict(g=g, nodos=nodos, ed=ed, nn=nn, nres=nres, D=D, q=q, qp=qp, zn=zn, H=H, Q=Q, v=v, grad=grad, pr=pr, ps=ps,
             mask=mask, dem=dem, grado=grado, adj=adj, vis=vis, asign=asign, dlote=dlote, lotes=lotes_red, cen=cen,
             lz=lz, lv=lv, nmin=nmin, nmax=nmax, salida_xy=salida_xy, reservorio=reservorio, tab=tab, C=C, k2=k2, dist_salida=float(dres))
    R["resumen"] = dict(
        red=g, lotes=len(lotes_red), nodos=nn, tuberias=len(ed), longitud_m=round(sum(e[2] for e in ed)),
        nodos_aislados_del_reservorio=int(nn - len(vis)), distancia_salida_a_nodo_m=round(float(dres), 1),
        Qmh_Ls=round(float(q.sum() * 1000), 2), Qp_Ls=round(float(qp.sum() * 1000), 2), iteraciones=int(nit),
        presion_min_pico=round(float(pr[dem].min()), 1), presion_p5_pico=round(float(np.percentile(pr[dem], 5)), 1),
        presion_mediana_pico=round(float(np.median(pr[dem])), 1), nodos_con_demanda=int(dem.sum()),
        nodos_menos_10=int((pr[dem] < 10).sum()), nodos_menos_15=int((pr[dem] < 15).sum()),
        estatica_max=round(float(ps[mask].max()), 1), nodos_mas_50=int((ps[mask] > 50).sum()),
        v_max=round(float(v.max()), 2), v_min=round(float(v.min()), 2), grad_max_m_km=round(float(grad.max()), 1),
        DN=dict(sorted(collections.Counter([dn_de_id(tab, d) for d in D]).items())),
        puntas_muertas=int((grado == 1).sum()),
        caudal_salida_reservorio_Ls=round(float(sum(abs(Q[p]) for p, (a, b, Lm) in enumerate(ed) if a == nres or b == nres) * 1000), 2),
        niveles_usados=[nmin, nmax])
    return R


def escribir_salidas_red(R, P, outdir, titulo_extra=""):
    g = R["g"]
    os.makedirs(os.path.join(outdir, "epanet"), exist_ok=True)
    tab, ed, D, nodos = R["tab"], R["ed"], R["D"], R["nodos"]
    with open(os.path.join(outdir, "tuberias_%s.csv" % g), "w", encoding="utf-8") as fh:
        fh.write("x1,y1,x2,y2,L_m,DN,Q_Ls,v_ms,hf_m_km,p_nodo1_pico,p_nodo2_pico\n")
        for p, (a, b, Lm) in enumerate(ed):
            fh.write("%.1f,%.1f,%.1f,%.1f,%.1f,%d,%.2f,%.2f,%.1f,%.1f,%.1f\n" % (
                nodos[a][0], nodos[a][1], nodos[b][0], nodos[b][1], Lm, dn_de_id(tab, D[p]), abs(R["Q"][p]) * 1000,
                R["v"][p], R["grad"][p], R["pr"][a], R["pr"][b]))
    ruta = os.path.join(outdir, "epanet", "red_%s_punta.inp" % g)
    epanet.escribir_inp(ruta, "Red %s - PRELIMINAR - hora punta K2=%s - diametros de predimensionamiento %s" % (g, R["k2"], titulo_extra),
                        "RES_" + g, R["nmin"], R["salida_xy"], nodos, R["zn"], R["q"] * 1000, ed, D, R["nres"])
    return ruta


# ------------------------------------------------------------------ validacion contra EPANET oficial
def validar_con_epanet(R, inp, exe):
    res = epanet.correr(inp, exe)[0]
    dmax, dq = 0.0, 0.0
    for i in range(R["nn"]):
        if not R["mask"][i]:
            continue
        _, h, p = res["nodos"]["N%d" % i]
        dmax = max(dmax, abs(p - R["pr"][i]))
    for p in range(len(R["ed"])):
        qe = abs(res["enlaces"]["T%d" % p][0]) / 1000
        dq = max(dq, abs(qe - abs(R["Q"][p])))
    return dict(dif_max_presion_m=round(dmax, 3), dif_max_caudal_Ls=round(dq * 1000, 4))


# ------------------------------------------------------------------ escenarios
def escenario_rotura(R, P, lotes_por_nodo=None):
    """Quita, de a uno, cada tramo de calculo (~30 m) en hora punta. Sin valvulas de aislamiento dibujadas se supone
    que se corta solo ese tramo."""
    ed, nn, nres, D, q, C, zn = R["ed"], R["nn"], R["nres"], R["D"], R["q"], R["C"], R["zn"]
    filas = []
    q_tot = q.sum()
    nodo_lotes = collections.Counter(R["asign"].tolist())
    for p in range(len(ed)):
        vis, _ = alcanzables(nn, ed, nres, excluir=p)
        perdido = [i for i in range(nn) if i not in vis]
        q_perd = float(sum(q[i] for i in perdido))
        lotes_perd = int(sum(nodo_lotes.get(i, 0) for i in perdido))
        pmin = None
        if len(vis) > 1:
            orden = sorted(vis)
            nuevo = {n: k for k, n in enumerate(orden)}
            ed2, D2, qd = [], [], np.zeros(len(orden))
            for r, (a, b, Lm) in enumerate(ed):
                if r != p and a in nuevo and b in nuevo:
                    ed2.append((nuevo[a], nuevo[b], Lm))
                    D2.append(D[r])
            for n in orden:
                qd[nuevo[n]] = q[n]
            H2, Q2, _ = resolver(qd, ed2, len(orden), np.array(D2), {nuevo[nres]: R["nmin"]}, C)
            pr2 = np.array([H2[nuevo[n]] - zn[n] for n in orden])
            dd = np.array([qd[nuevo[n]] > 0 for n in orden])
            pmin = float(pr2[dd].min()) if dd.any() else None
        a, b, Lm = ed[p]
        filas.append(dict(tramo=p, x=float((R["nodos"][a][0] + R["nodos"][b][0]) / 2), y=float((R["nodos"][a][1] + R["nodos"][b][1]) / 2),
                          demanda_perdida_Ls=round(q_perd * 1000, 2), pct_demanda_perdida=round(100 * q_perd / q_tot, 1) if q_tot else 0.0,
                          lotes_sin_servicio=lotes_perd, presion_min_restante=None if pmin is None else round(pmin, 1)))
    cortan = [f for f in filas if f["demanda_perdida_Ls"] > 0]
    sin_corte = [f for f in filas if f["demanda_perdida_Ls"] == 0 and f["presion_min_restante"] is not None]
    dist = dict(mas_50_pct=sum(1 for f in cortan if f["pct_demanda_perdida"] >= 50),
                entre_10_y_50_pct=sum(1 for f in cortan if 10 <= f["pct_demanda_perdida"] < 50),
                menos_10_pct=sum(1 for f in cortan if f["pct_demanda_perdida"] < 10))
    return dict(red=R["g"], tramos_evaluados=len(filas), tramos_que_dejan_sin_agua=len(cortan), distribucion_cortes=dist,
                peor_corte=sorted(cortan, key=lambda f: -f["demanda_perdida_Ls"])[:10],
                peor_presion_sin_corte=sorted(sin_corte, key=lambda f: f["presion_min_restante"])[:10],
                todos=filas)


def patron_24h(P, k2):
    forma = np.array(P("hidraulica.patron_24h_forma"), float)
    forma = forma / forma.mean()
    a = (k2 - 1.0) / (forma.max() - 1.0)
    p = 1.0 + (forma - 1.0) * a
    if p.min() <= 0:
        p = np.clip(p, 0.05, None)
        p = p / p.mean()
    return p


def escenario_24h(R, P, outdir, exe):
    patron = patron_24h(P, R["k2"])
    ruta = os.path.join(outdir, "epanet", "red_%s_24h.inp" % R["g"])
    epanet.escribir_inp(ruta, "Red %s - PRELIMINAR - 24 h, reservorio a nivel minimo fijo" % R["g"], "RES_" + R["g"], R["nmin"],
                        R["salida_xy"], R["nodos"], R["zn"], R["qp"] * 1000, R["ed"], R["D"], R["nres"], patron=list(patron), horas=24)
    res = epanet.correr(ruta, exe)
    dem = [i for i in range(R["nn"]) if R["dem"][i]]
    horas = []
    for h in sorted(res):
        pres = np.array([res[h]["nodos"]["N%d" % i][2] for i in dem])
        horas.append(dict(hora=h, multiplicador=round(float(patron[h % 24]), 2), p_min=round(float(pres.min()), 1), p_max=round(float(pres.max()), 1)))
    hp = min(horas, key=lambda x: x["p_min"])
    hm = max(horas, key=lambda x: x["p_max"])
    return dict(red=R["g"], inp=ruta, patron=[round(float(x), 3) for x in patron], horas=horas,
                p_min_global=hp["p_min"], hora_p_min=hp["hora"], p_max_global=hm["p_max"], hora_p_max=hm["hora"],
                nota="El reservorio se mantiene a su nivel minimo (no se simula el vaciado/llenado del tanque). Patron SUPUESTO.")


def escenario_bomba(R, P, medidor_xy):
    """Aduccion medidor -> reservorio: diametro, perdida y altura de bombeo para distintas cargas de la fuente."""
    C = R["C"]
    tab = R["tab"]
    k1 = P("demanda.k1")
    horas = P("bombeo_llenado.horas_bombeo_dia")
    eta = P("bombeo_llenado.eficiencia_bomba")
    fac = P("bombeo_llenado.factor_longitud_aduccion")
    vel = P("bombeo_llenado.velocidad_aduccion_ms")
    loc = P("bombeo_llenado.perdidas_locales_fraccion")
    cx, cy = R["reservorio"]["c"]
    Ldir = float(np.hypot(cx - medidor_xy[0], cy - medidor_xy[1]))
    L = Ldir * fac
    qmd = k1 * R["qp"].sum()  # m3/s
    q_fill = qmd * 24.0 / horas
    area_req = q_fill / vel
    dn_ok = [(dn, i) for dn, i in tab if np.pi * i ** 2 / 4 >= area_req]
    dn, idm = (dn_ok[0] if dn_ok else tab[-1])
    hf = hf_hw(q_fill, idm, L, C) * (1 + loc)
    filas = []
    for carga in P("fuente_agua.sensibilidad_carga_m"):
        tdh = R["nmax"] - carga + hf
        filas.append(dict(carga_fuente_m=carga, altura_dinamica_m=round(float(tdh), 1), requiere_bomba=bool(tdh > 0),
                          potencia_kW=round(float(9.81 * q_fill * max(tdh, 0) / eta), 1) if tdh > 0 else 0.0))
    return dict(red=R["g"], distancia_recta_m=round(Ldir, 1), longitud_aduccion_m=round(L, 1), qmd_Ls=round(qmd * 1000, 2),
                caudal_llenado_Ls=round(q_fill * 1000, 2), horas_bombeo=horas, DN_aduccion=dn, v_ms=round(float(q_fill / (np.pi * idm ** 2 / 4)), 2),
                perdida_hf_m=round(float(hf), 2), nivel_max_reservorio=R["nmax"], casos=filas,
                nota="Aduccion en linea recta x factor; el trazado real no esta dibujado. La carga de la fuente es NO VERIFICADA.")


def volumen_reservorio(R, P):
    vol = float(R["lv"].sum())  # m3/d
    reg = P("demanda.regulacion_fraccion") * vol
    qmd_m3d = P("demanda.k1") * vol
    res = P("demanda.reserva_fraccion_qmd") * qmd_m3d
    inc = 0.0
    if P("demanda.incendio_incluir"):
        V = P("demanda.incendio_volumen_m3")
        modo = P("demanda.incendio_reparto")
        if modo == "proporcional_poblacion":
            inc = V * R["pob"] / R["pob_total"]
        elif modo == "por_reservorio":
            inc = V
        else:  # unico_R2
            inc = V if R["g"] == "R2" else 0.0
    return dict(red=R["g"], vol_diario_m3=round(vol), regulacion_m3=round(reg), reserva_m3=round(res), total_sin_incendio_m3=round(reg + res),
                incendio_m3=round(inc, 1), total_m3=round(reg + res + inc), pob=R["pob"], pct_pob=round(100.0 * R["pob"] / R["pob_total"], 1))


def escenario_incendio(R, P):
    """Gasto coincidente (CTPS-PR-02 8.2.3): Qmd + caudal de incendio en un hidrante. Se prueba cada nodo como hidrante
    con los diametros de la hora punta (no se redimensiona). Compara ademas con la hora punta para saber cual gobierna."""
    ed, nn, nres, D, C, zn = R["ed"], R["nn"], R["nres"], R["D"], R["C"], R["zn"]
    qinc = P("demanda.incendio_caudal_ls") / 1000.0
    qmd = P("demanda.k1") * R["qp"]  # m3/s por nodo
    pres_min = P("demanda.incendio_presion_residual_mca")
    vmax_n = P("demanda.incendio_velocidad_max_ms")
    area = np.pi * D ** 2 / 4
    candidatos = [i for i in range(nn) if R["mask"][i] and i != nres]
    filas = []
    for i in candidatos:
        q = qmd.copy()
        q[i] += qinc
        H, Q, _ = resolver(q, ed, nn, D, {nres: R["nmin"]}, C)
        p = H - zn
        v = np.abs(Q) / area
        filas.append((i, float(p[i]), float(p[R["dem"]].min()), float(v.max())))
    ok = [f for f in filas if f[1] >= pres_min]
    peor = sorted(filas, key=lambda f: f[1])[:8]
    qmh_ls = float(R["q"].sum() * 1000)
    qmd_ls = float(qmd.sum() * 1000)
    return dict(red=R["g"], qmh_ls=round(qmh_ls, 2), qmd_ls=round(qmd_ls, 2), qmd_mas_incendio_ls=round(qmd_ls + qinc * 1000, 2),
                gobierna="incendio" if qmd_ls + qinc * 1000 > qmh_ls else "hora punta", caudal_incendio_ls=qinc * 1000,
                hidrantes_probados=len(filas), hidrantes_con_presion_residual_ok=len(ok), presion_residual_exigida=pres_min,
                presion_min_en_hidrante=round(min(f[1] for f in filas), 1), presion_min_resto_red=round(min(f[2] for f in filas), 1),
                velocidad_max_ms=round(max(f[3] for f in filas), 2), velocidad_max_norma_ms=vmax_n,
                casos_con_velocidad_sobre_norma=sum(1 for f in filas if f[3] > vmax_n),
                peores_hidrantes=[dict(nodo="N%d" % f[0], x=round(float(R["nodos"][f[0]][0])), y=round(float(R["nodos"][f[0]][1])),
                                       presion_residual=round(f[1], 1), presion_min_resto=round(f[2], 1), v_max=round(f[3], 2)) for f in peor],
                nota="Cada nodo se prueba como hidrante con los diametros de hora punta (sin redimensionar). Aun no hay hidrantes ubicados en el diseno.")


def presion_por_lote(R):
    filas = []
    for k, (cod, x, y, cota, v) in enumerate(R["lotes"]):
        n = int(R["asign"][k])
        filas.append(dict(lote=cod, red=R["g"], x=round(x, 1), y=round(y, 1), cota_terreno=round(cota, 2), nodo="N%d" % n,
                          dist_a_nodo_m=round(float(R["dlote"][k]), 1), presion_punta_mca=round(float(R["pr"][n] + (R["zn"][n] - cota)), 1),
                          presion_estatica_mca=round(float(R["ps"][n] + (R["zn"][n] - cota)), 1)))
    return filas


# ------------------------------------------------------------------ puntos a revisar
def puntos_revisar(Rs, P, lotes_todos, medidor_xy):
    """Lista de puntos para la capa EPANET_REVISAR del DXF. Gravedad: 1 = critico, 2 = aviso."""
    items = []
    pmin_d, pmin_n = P("hidraulica.presion_min_diseno_mca"), P("hidraulica.presion_min_normativa_mca")
    pmax = P("hidraulica.presion_estatica_max_mca")
    for g, R in Rs.items():
        for i in range(R["nn"]):
            x, y = R["nodos"][i]
            if R["grado"][i] == 1 and i != R["nres"]:
                items.append(dict(tipo="Punta muerta", red=g, x=x, y=y, gravedad=2, texto="Punta muerta: prever purga o cierre en lazo"))
            if R["dem"][i] and R["pr"][i] < pmin_n:
                items.append(dict(tipo="Presion < norma", red=g, x=x, y=y, gravedad=1, texto="P=%.1f mca < %.0f (norma)" % (R["pr"][i], pmin_n)))
            elif R["dem"][i] and R["pr"][i] < pmin_d:
                items.append(dict(tipo="Presion < diseno", red=g, x=x, y=y, gravedad=2, texto="P=%.1f mca < %.0f (diseno)" % (R["pr"][i], pmin_d)))
            if R["mask"][i] and R["ps"][i] > pmax:
                items.append(dict(tipo="Estatica > 50 m", red=g, x=x, y=y, gravedad=1, texto="Estatica %.1f m > %.0f" % (R["ps"][i], pmax)))
        if R["nn"] - len(R["vis"]) > 0:
            aisl = [i for i in range(R["nn"]) if i not in R["vis"]]
            for i in aisl[:20]:
                x, y = R["nodos"][i]
                items.append(dict(tipo="Nodo aislado", red=g, x=x, y=y, gravedad=1, texto="Nodo sin conexion al reservorio"))
    # fronteras entre redes
    if len(Rs) == 2:
        (g1, R1), (g2, R2) = list(Rs.items())
        t2 = cKDTree(R2["nodos"])
        d, j = t2.query(R1["nodos"])
        dmax = P("hidraulica.distancia_frontera_m")
        usados = []
        for i in np.argsort(d):
            if d[i] > dmax:
                break
            mx, my = (R1["nodos"][i] + R2["nodos"][j[i]]) / 2
            if any(np.hypot(mx - ux, my - uy) < 15 for ux, uy in usados):
                continue
            usados.append((mx, my))
            items.append(dict(tipo="Frontera R1/R2", red="R1/R2", x=float(mx), y=float(my), gravedad=1,
                              texto="Frontera %s/%s a %.1f m: valvula cerrada entre redes" % (g1, g2, d[i])))
    # reservorios sobre la carga de la fuente y aduccion no dibujada
    carga = P("fuente_agua.carga_hidraulica_m")
    for g, R in Rs.items():
        cx, cy = R["reservorio"]["c"]
        if R["nmax"] > carga:
            items.append(dict(tipo="Llenado por bomba", red=g, x=cx, y=cy, gravedad=1,
                              texto="Reservorio %s: nivel max %.1f > carga fuente %.1f (NO VERIFICADA): llenado con bomba" % (g, R["nmax"], carga)))
    todos = np.vstack([R["nodos"] for R in Rs.values()])
    dm = float(np.hypot(todos[:, 0] - medidor_xy[0], todos[:, 1] - medidor_xy[1]).min())
    if dm > 15:
        items.append(dict(tipo="Aduccion", red="-", x=medidor_xy[0], y=medidor_xy[1], gravedad=1,
                          texto="Falta dibujar la aduccion desde el medidor (red mas cercana a %.0f m)" % dm))
    # lotes lejos de la tuberia
    lim = P("hidraulica.distancia_max_lote_tuberia_m")
    for g, R in Rs.items():
        for k, (cod, x, y, cota, v) in enumerate(R["lotes"]):
            if R["dlote"][k] > lim:
                items.append(dict(tipo="Lote sin tuberia", red=g, x=x, y=y, gravedad=2,
                                  texto="%s a %.0f m de la red" % (cod, R["dlote"][k])))
    return items
