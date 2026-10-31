# -*- coding: utf-8 -*-
"""Convierte el JSON de la herramienta civil3d_export_layer_lines en la red usada por el modelo
(reservorioN {c, r}; matriz y sectorN = lista de trazados [[x, y], ...]). Valida capas, tipos y nombre del DWG."""
import json, os, sys
from comun import Parametros, escribir_json, sha256


def importar(export_json, P, salida=None, permitir_dwg_distinto=False):
    ex = json.load(open(export_json, encoding="utf-8"))
    avisos, errores = [], []
    dwg = ex.get("dwg", "")
    esperado = P("reservorios.dwg_esperado_contiene").lower()
    if esperado not in os.path.basename(dwg).lower():
        (avisos if permitir_dwg_distinto else errores).append(
            "El export viene de '%s', que no contiene '%s'. Active la pestana correcta de Civil 3D y exporte de nuevo." % (dwg, esperado))
    mapa = P("reservorios.capas_dibujo")  # clave -> capa
    capas = ex.get("layers", {})
    red = {}
    for clave, capa in mapa.items():
        info = capas.get(capa)
        if info is None or info.get("count", 0) == 0:
            errores.append("Falta la capa '%s' (%s) o esta vacia en el export." % (capa, clave))
            continue
        ents = info["entities"]
        if clave.startswith("reservorio"):
            circ = [e for e in ents if e["type"] == "Circle"]
            if len(circ) != 1:
                errores.append("La capa %s debe tener exactamente 1 circulo (tiene %d circulos de %d entidades)." % (capa, len(circ), len(ents)))
                continue
            red[clave] = dict(c=[circ[0]["cx"], circ[0]["cy"]], r=circ[0]["radius"])
            continue
        trazos = []
        for e in ents:
            t = e["type"]
            if t == "Polyline":
                v = e["vertices"]
                if e.get("closed"):
                    avisos.append("%s [%s]: polilinea CERRADA en una capa de red (se toma como trazado cerrado)." % (capa, e["handle"]))
                    if (v[0][0], v[0][1]) != (v[-1][0], v[-1][1]):
                        v = v + [v[0]]
                if any(abs(p[2]) > 1e-9 for p in v):
                    avisos.append("%s [%s]: tiene tramos curvos (bulge); exporte con flattenArcs=true o use rectas." % (capa, e["handle"]))
                trazos.append([[p[0], p[1]] for p in v])
            elif t == "Line":
                trazos.append([[e["x1"], e["y1"]], [e["x2"], e["y2"]]])
            elif t in ("DBText", "MText"):
                continue
            else:
                avisos.append("%s [%s]: entidad %s ignorada." % (capa, e["handle"], t))
        if not trazos:
            errores.append("La capa %s no tiene trazados utilizables." % capa)
        red[clave] = trazos
    extra = sorted(set(capas) - set(mapa.values()))
    if extra:
        avisos.append("Capas del export que no se usan: %s" % extra)
    red["_fuente"] = "%s | export_layer_lines %s | sha256 %s" % (dwg, ex.get("exportedUtc", "?"), sha256(export_json, 16))
    res = dict(ok=not errores, errores=errores, avisos=avisos, dwg=dwg, red=red,
               conteos={k: (len(v) if isinstance(v, list) else 1) for k, v in red.items() if k != "_fuente"})
    if res["ok"] and salida:
        escribir_json(salida, red)
    return res


if __name__ == "__main__":
    P = Parametros()
    r = importar(sys.argv[1], P, sys.argv[2] if len(sys.argv) > 2 else None)
    print(json.dumps({k: v for k, v in r.items() if k != "red"}, indent=1, ensure_ascii=False))
    sys.exit(0 if r["ok"] else 1)
