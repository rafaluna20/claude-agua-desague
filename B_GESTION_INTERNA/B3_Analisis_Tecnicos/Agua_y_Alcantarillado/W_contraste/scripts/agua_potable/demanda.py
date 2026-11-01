# -*- coding: utf-8 -*-
"""Demanda de agua potable de toda la habilitacion. PRELIMINAR. Todos los valores salen de parametros_agua_potable_v1.json."""
import json, os, re, collections
from comun import escribir_json, sha256


def area(poly):
    s = 0.0
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def clasificar(cod, a, P):
    m = re.match(r"^(E\d\d)MZ([A-Z])", cod)
    et, mz = m.group(1), m.group(2)
    if cod == P("demanda.lote_ptar"):
        return et, mz, "PTAR (sin poblacion)"
    if mz == P("demanda.manzana_no_residencial"):
        return et, mz, "Comercial / grifo (manzana Z)"
    if a >= P("demanda.umbral_multifamiliar_area_m2"):
        return et, mz, "Multifamiliar"
    return et, mz, "Vivienda ordinaria"


def cargar_lotes(P):
    parcels = json.load(open(P.archivo("parcels"), encoding="utf-8"))
    lotes = []
    for cod, v in sorted(parcels.items()):
        a = area(v)
        et, mz, cl = clasificar(cod, a, P)
        lotes.append(dict(cod=cod, etapa=et, manzana=et + "-" + mz, area=a, clase=cl))
    return lotes


def poblacion(l, P, regla_area=False):
    hv = P("demanda.hab_por_vivienda")
    if l["clase"] == "Vivienda ordinaria":
        return hv * P("demanda.viviendas_por_lote_ordinario")
    if l["clase"] == "Multifamiliar":
        vp = max(1, round(l["area"] * 0.6 / 80)) if regla_area else P("demanda.viviendas_por_piso_multifamiliar")
        return P("demanda.pisos_multifamiliar") * vp * hv
    return 0


def vol_lote_m3d(l, P, dot=None):
    """Volumen diario promedio del lote (vivienda + comercial) en m3/d."""
    dot = P("demanda.dotacion_l_hab_d") if dot is None else dot
    v = poblacion(l, P) * dot / 1000.0
    if l["clase"].startswith("Comercial"):
        v += l["area"] * P("demanda.comercial_cobertura_lote") * P("demanda.comercial_l_m2_d") / 1000.0
    return v


def _suma_areas(path):
    d = json.load(open(path, encoding="utf-8"))
    return sum(area(v["coordinates"]) for v in d.values())


def escenario(lotes, P, dot=None, k2=None, regla_area=False, cobertura=None, com=True):
    dot = P("demanda.dotacion_l_hab_d") if dot is None else dot
    k2 = P("demanda.k2") if k2 is None else k2
    cobertura = P("demanda.comercial_cobertura_lote") if cobertura is None else cobertura
    pob = sum(poblacion(l, P, regla_area) for l in lotes)
    a_com = sum(l["area"] for l in lotes if l["clase"].startswith("Comercial")) if com else 0.0
    vol_com = a_com * cobertura * P("demanda.comercial_l_m2_d") / 1000.0
    vol = pob * dot / 1000.0 + vol_com
    qp = vol * 1000 / 86400
    qmd = P("demanda.k1") * qp
    qmh = k2 * qp
    reg = P("demanda.regulacion_fraccion") * vol
    res7 = P("demanda.reserva_fraccion_qmd") * qmd * 86.4
    n_res = len(P("reservorios.grupos")) if P("demanda.incendio_reparto") == "por_reservorio" else 1
    exigido = pob >= P("demanda.incendio_umbral_hab")
    inc = P("demanda.incendio_volumen_m3") * n_res if (P("demanda.incendio_incluir") or exigido) else 0
    return dict(dot=dot, k2=k2, pob=pob, vol_comercial=vol_com, vol_total=vol, qp=qp, qmd=qmd, qmh=qmh,
                regulacion=reg, reserva=res7, incendio=inc, v_reservorio=reg + res7 + inc)


def correr(P, outdir):
    lotes = cargar_lotes(P)
    for l in lotes:
        l["pob"] = poblacion(l, P)
        l["vol_m3d"] = vol_lote_m3d(l, P)
    esc = collections.OrderedDict([
        ("BASE", escenario(lotes, P)),
        ("K2 = 2.0", escenario(lotes, P, k2=2.0)),
        ("Clima templado (155 L)", escenario(lotes, P, dot=155)),
        ("Multifamiliar por area (60 % cobertura, 80 m2/viv)", escenario(lotes, P, regla_area=True)),
        ("Comercial al 100 % del lote", escenario(lotes, P, cobertura=1.0)),
        ("Sin comercial (referencia)", escenario(lotes, P, com=False)),
    ])
    a_riego = _suma_areas(P.archivo("jardin")) + _suma_areas(P.archivo("aporte_recreacion"))
    res = dict(conteo=dict(collections.Counter(l["clase"] for l in lotes)), total_lotes=len(lotes),
               riego_referencia_m3d=a_riego * P("demanda.riego_l_m2_d") / 1000.0, area_riego_m2=a_riego,
               escenarios=esc,
               entradas_sha256_16={k: sha256(P.archivo(k), 16) for k in ("parcels", "jardin", "aporte_recreacion")})
    escribir_json(os.path.join(outdir, "demanda.json"), res)
    escribir_json(os.path.join(outdir, "lotes_clasificados.json"), lotes)
    return lotes, res
