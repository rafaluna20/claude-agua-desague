# -*- coding: utf-8 -*-
"""Demanda de agua potable de TODA la habilitacion (1,341 lotes). PRELIMINAR.
Entradas: datos/v3_48calles (parcels_export, jardin, aportes). Salidas: resultados/v1_demanda_agua_1341/
Supuestos del usuario 2026-10-31: 1,341 lotes reciben agua; 1 vivienda/lote ordinario; multifamiliar 7 pisos
promedio; 6 hab/vivienda; riego de parques y areas verdes; fuente Santa Maria abastece todo.
Aclaracion del usuario 2026-10-31 (2): manzana Z (001-006) = grifo y zonas comerciales; el riego tendra tuberia propia
con agua tratada de la PTAR (sale de la demanda de agua potable). Fuente: Santa Maria abastece todo (asuncion).
Supuestos del asistente (a validar): 2 viv/piso en multifamiliar; comercial 6 L/m2/d sobre 60 % del lote (NO VERIFICADO).
"""
import json, re, sys, os, hashlib, collections
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
D = os.path.join(BASE, "datos", "v3_48calles")
OUT = os.path.join(BASE, "resultados", "v1_demanda_agua_1341")

def area(p):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(p, p[1:] + p[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2

def sha(f):
    return hashlib.sha256(open(f, "rb").read()).hexdigest()[:16]

P = json.load(open(os.path.join(D, "parcels_export.json"), encoding="utf-8"))
PTAR = "E03MZD049P"
NO_RES_MANZ = "Z"          # E04MZZ***: manzana Z, uso no definido (lotes de 487 a 7,000 m2)
UMBRAL_MF = 300.0
PARAM = dict(hab_viv=6, pisos_mf=7, viv_piso_mf=2, dot_base=169, dot_alt=155, k1=1.3, k2_base=2.5, k2_alt=2.0,
             riego_l_m2_d=2.0, com_l_m2_d=6.0, com_cobertura=0.6)

def clasifica(cod, a):
    m = re.match(r"^(E\d\d)MZ([A-Z])", cod)
    et, mz = m.group(1), m.group(2)
    if cod == PTAR: return et, mz, "PTAR (sin poblacion)"
    if mz == NO_RES_MANZ: return et, mz, "Comercial / grifo (manzana Z)"
    if a >= UMBRAL_MF: return et, mz, "Multifamiliar"
    return et, mz, "Vivienda ordinaria"

lotes = []
for cod, v in sorted(P.items()):
    a = area(v); et, mz, cl = clasifica(cod, a)
    lotes.append(dict(cod=cod, etapa=et, manzana=et + "-" + mz, area=a, clase=cl))

def poblacion(l, viv_piso=PARAM["viv_piso_mf"], pisos=PARAM["pisos_mf"], hv=PARAM["hab_viv"], regla_area=False):
    if l["clase"] == "Vivienda ordinaria": return hv
    if l["clase"] == "Multifamiliar":
        vp = max(1, round(l["area"] * 0.6 / 80)) if regla_area else viv_piso   # variante: 60 % cobertura, 80 m2/vivienda
        return pisos * vp * hv
    return 0

# areas verdes / aportes
def suma(f):
    d = json.load(open(os.path.join(D, f), encoding="utf-8"))
    return {k: area(v["coordinates"]) for k, v in d.items()}
jard = suma("jardin_import.json"); rec = suma("aporte_recreacion_import.json")
edu = suma("aporte_educacion_import.json"); otr = suma("aporte_otros_import.json")
A_jard, A_rec = sum(jard.values()), sum(rec.values())

def escenario(dot, k2, regla_area=False, riego=False, cobertura=None, com=True):
    cobertura = PARAM["com_cobertura"] if cobertura is None else cobertura
    pob = sum(poblacion(l, regla_area=regla_area) for l in lotes)
    a_com = sum(l["area"] for l in lotes if l["clase"].startswith("Comercial")) if com else 0.0
    vol_com = a_com * cobertura * PARAM["com_l_m2_d"] / 1000          # m3/d
    vol_dom = pob * dot / 1000 + vol_com               # m3/d (vivienda + comercial; ambos con K1 y K2)
    vol_ref_riego = (A_jard + A_rec) * PARAM["riego_l_m2_d"] / 1000  # solo referencia: va por red de agua tratada
    q_dom = vol_dom * 1000 / 86400                     # L/s  (Qp potable)
    q_riego_vol = vol_ref_riego if riego else 0.0
    q_riego = q_riego_vol * 1000 / 86400
    qp = q_dom + q_riego
    qmd = PARAM["k1"] * q_dom + q_riego
    qmh = k2 * q_dom + q_riego
    vol_tot = vol_dom + q_riego_vol
    reg = 0.25 * vol_tot
    reserva = 0.07 * qmd * 86.4                       # 7 % del consumo maximo diario (m3)
    inc = 0 if pob < 10000 else 100                   # CTPS 100 m3; con < 10,000 hab no se considera
    return dict(dot=dot, k2=k2, pob=pob, vol_com=vol_com, riego_ref=vol_ref_riego, vol_dom=vol_dom, vol_riego=q_riego_vol, vol_total=vol_tot,
                qp=qp, qmd=qmd, qmh=qmh, q_dom=q_dom, q_riego=q_riego,
                regulacion=reg, reserva7=reserva, incendio=inc, v_reservorio=reg + reserva + inc,
                llenado_24h=qmd, llenado_12h=qmd * 2, llenado_6h=qmd * 4)

esc = {
 "BASE (169 L, K2 2.5, 2 viv/piso, riego con agua tratada)": escenario(169, 2.5),
 "K2 = 2.0": escenario(169, 2.0),
 "Clima templado (155 L)": escenario(155, 2.5),
 "155 L y K2 = 2.0": escenario(155, 2.0),
 "MF por area (60 % cobertura, 80 m2/viv)": escenario(169, 2.5, regla_area=True),
 "Comercial al 100 % del lote": escenario(169, 2.5, cobertura=1.0),
 "Sin comercial (referencia)": escenario(169, 2.5, com=False),
 "Riego con agua potable (referencia, no es el diseno)": escenario(169, 2.5, riego=True),
}
cnt = collections.Counter(l["clase"] for l in lotes)
res = dict(parametros=PARAM, conteo=dict(cnt), total_lotes=len(lotes),
           areas_m2=dict(jardines=A_jard, n_jardines=len(jard), recreacion=A_rec, n_recreacion=len(rec),
                         educacion=sum(edu.values()), otros=sum(otr.values())),
           escenarios=esc,
           entradas_sha256_16={f: sha(os.path.join(D, f)) for f in ("parcels_export.json", "jardin_import.json", "aporte_recreacion_import.json")})
json.dump(res, open(os.path.join(OUT, "demanda_agua_1341_v1.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(lotes, open(os.path.join(OUT, "lotes_clasificados_v1.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)

if "-q" not in sys.argv:
    print(dict(cnt), "total", len(lotes))
    print("area lotes m2", round(sum(l["area"] for l in lotes)))
    print("jardines", len(jard), round(A_jard), "recreacion", len(rec), round(A_rec), "edu", round(sum(edu.values())), "otros", round(sum(otr.values())))
    for k, e in esc.items():
        print(f"\n{k}\n  pob {e['pob']} | vol {e['vol_total']:.0f} m3/d (comercial {e['vol_com']:.0f}, riego {e['vol_riego']:.0f}) | Qp {e['qp']:.2f} Qmd {e['qmd']:.2f} Qmh {e['qmh']:.2f} L/s"
              f" | reservorio: reg {e['regulacion']:.0f}+res7% {e['reserva7']:.0f}+inc {e['incendio']} = {e['v_reservorio']:.0f} m3")
    print("\nMultifamiliares:"); [print(" ", l["cod"], round(l["area"], 1)) for l in lotes if l["clase"] == "Multifamiliar"]
    print("Manzana Z:"); [print(" ", l["cod"], round(l["area"], 1)) for l in lotes if l["clase"].startswith("Manzana Z")]
    print("jardin: mayores", sorted(((round(a), k) for k, a in jard.items()), reverse=True)[:5])
    print("recreacion:", {k: round(a) for k, a in rec.items()})

# ---------- Excel ----------
if "-x" in sys.argv:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook(); H = Font(bold=True, color="FFFFFF"); F = PatternFill("solid", fgColor="1F4E79")
    def hoja(ws, filas, anchos=None):
        for r in filas: ws.append(r)
        for c in ws[1]: c.font = H; c.fill = F; c.alignment = Alignment(wrap_text=True, vertical="center")
        for i, w in enumerate(anchos or [], 1): ws.column_dimensions[chr(64 + i)].width = w
        ws.freeze_panes = "A2"
    ws = wb.active; ws.title = "Escenarios"
    hoja(ws, [["Escenario", "Dotacion L/hab/d", "K2", "Poblacion hab", "Vol vivienda+comercial m3/d", "de ello comercial m3/d", "Vol riego potable m3/d", "Vol total m3/d",
               "Qp L/s", "Qmd L/s", "Qmh L/s", "Regulacion 25% m3", "Reserva 7% Qmd m3", "Incendio m3", "Reservorio total m3",
               "Llenado 24h L/s", "Llenado 12h L/s", "Llenado 6h L/s"]] +
         [[k, e["dot"], e["k2"], e["pob"], round(e["vol_dom"]), round(e["vol_com"]), round(e["vol_riego"]), round(e["vol_total"]), round(e["qp"], 2),
           round(e["qmd"], 2), round(e["qmh"], 2), round(e["regulacion"]), round(e["reserva7"]), e["incendio"],
           round(e["v_reservorio"]), round(e["llenado_24h"], 2), round(e["llenado_12h"], 2), round(e["llenado_6h"], 2)] for k, e in esc.items()],
         [54] + [14] * 17)
    ws = wb.create_sheet("Supuestos")
    hoja(ws, [["Parametro", "Valor", "Origen", "Estado"],
      ["Lotes atendidos", "1,341 (todos)", "Usuario 2026-10-31", "CONFIRMADO"],
      ["Viviendas por lote ordinario", 1, "Usuario 2026-10-31", "CONFIRMADO"],
      ["Pisos del multifamiliar", 7, "Usuario 2026-10-31 (promedio)", "CONFIRMADO"],
      ["Habitantes por vivienda", 6, "Usuario; OS.100 1.3 b) N-073", "CONFIRMADO"],
      ["Umbral multifamiliar (area lote)", ">= 300 m2", "S-011", "CONFIRMADO"],
      ["Viviendas por piso en multifamiliar", 2, "Asistente (igual a T-12)", "SUPUESTO A VALIDAR"],
      ["Dotacion base", "169 L/hab/d (cálido); alt. 155", "IS.010 mod. RM 0107-2025; S-004", "PENDIENTE clima SENAMHI"],
      ["K1", 1.3, "OS.100 1.5 / OS.070 (CTPS: 1.2)", "ELEGIDO por asistente"],
      ["K2", "2.5 (base); 2.0 alt.", "OS.100 1.5 rango 1.8-2.5; localidad pequeña", "ELEGIDO por asistente"],
      ["Riego de jardines y recreacion", "FUERA de la demanda potable: red propia con agua tratada de la PTAR (referencia 108 m3/d a 2 L/m2/d)", "Usuario 2026-10-31", "CONFIRMADO; falta verificar los 2 L/m2/d"],
      ["Manzana Z (E04MZZ001-006)", "Grifo y zonas comerciales; no se sabe cual lote es grifo", "Usuario 2026-10-31", "CONFIRMADO uso; PENDIENTE identificar grifo"],
      ["Dotacion comercial", "6 L/m2/d sobre 60 % del lote (area util)", "Valor usual de IS.010 anterior; NO esta en los textos del libro de normas", "NO VERIFICADO"],
      ["Contra incendio", "0 si pob < 10,000; 100 m3 si >= 10,000", "CTPS 4.4.1 / OS.100 1.6 (N-076, N-034)", "VERIFICADO"],
      ["PTAR (E03MZD049P)", "Sin poblacion ni consumo (expediente independiente)", "S-017", "PENDIENTE"],
      ["Fuente", "Santa Maria abastece todo", "Usuario 2026-10-31", "ASUNCION del usuario, sin factibilidad"],
      ["Entradas (hash)", json.dumps(res["entradas_sha256_16"]), "datos/v3_48calles", ""]], [38, 34, 52, 30])
    ws = wb.create_sheet("Por manzana")
    mz = collections.OrderedDict()
    for l in lotes:
        r = mz.setdefault(l["manzana"], dict(n=0, mf=0, nr=0, pob=0, area=0.0))
        r["n"] += 1; r["mf"] += l["clase"] == "Multifamiliar"; r["nr"] += l["clase"].startswith(("Manzana Z", "PTAR")); r["pob"] += poblacion(l); r["area"] += l["area"]
    hoja(ws, [["Manzana", "Lotes", "Multifamiliares", "Sin poblacion", "Poblacion", "Area lotes m2", "Demanda base m3/d (169 L)"]] +
         [[k, v["n"], v["mf"], v["nr"], v["pob"], round(v["area"]), round(v["pob"] * 169 / 1000, 1)] for k, v in mz.items()], [14, 10, 16, 14, 12, 14, 24])
    ws = wb.create_sheet("Lotes")
    hoja(ws, [["Lote", "Etapa", "Manzana", "Area m2", "Clase", "Poblacion", "Demanda base m3/d (169 L)"]] +
         [[l["cod"], l["etapa"], l["manzana"], round(l["area"], 1), l["clase"], poblacion(l), round(poblacion(l) * 169 / 1000, 3)] for l in lotes], [14, 8, 10, 10, 30, 11, 22])
    wb.save(os.path.join(OUT, "demanda_agua_1341_v1.xlsx")); print("xlsx ok")
