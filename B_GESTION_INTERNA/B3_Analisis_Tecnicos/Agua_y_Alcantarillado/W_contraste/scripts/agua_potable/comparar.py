# -*- coding: utf-8 -*-
"""Compara dos corridas (carpetas de resultados/v3_agua): resultados por red, puntos a revisar y parametros.
Uso: python comparar.py c01_2026-10-31 c02_2026-11-05"""
import collections, json, os, sys

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def cargar(nombre):
    d = os.path.join(BASE, "resultados", "v3_agua", nombre)
    return (json.load(open(os.path.join(d, "resultados_modelo.json"), encoding="utf-8")),
            json.load(open(os.path.join(d, "revisar.json"), encoding="utf-8")),
            json.load(open(os.path.join(d, "procedencia.json"), encoding="utf-8")))


def main(a, b):
    ra, va, pa = cargar(a)
    rb, vb, pb = cargar(b)
    print("Comparacion %s -> %s\n" % (a, b))
    claves = ["lotes", "longitud_m", "Qmh_Ls", "presion_min_pico", "estatica_max", "v_max", "puntas_muertas", "nodos_menos_15", "DN"]
    for g in sorted(set(ra["resumenes"]) | set(rb["resumenes"])):
        x, y = ra["resumenes"].get(g, {}), rb["resumenes"].get(g, {})
        print("== Red", g)
        for k in claves:
            marca = "" if x.get(k) == y.get(k) else "   <-- cambio"
            print("  %-18s %-40s -> %-40s%s" % (k, x.get(k), y.get(k), marca))
    ca = collections.Counter(i["tipo"] for i in va)
    cb = collections.Counter(i["tipo"] for i in vb)
    print("\n== Puntos a revisar")
    for t in sorted(set(ca) | set(cb)):
        print("  %-22s %3d -> %3d%s" % (t, ca[t], cb[t], "" if ca[t] == cb[t] else "   <-- cambio"))
    print("\n== Entradas")
    for k in sorted(set(pa["entradas"]) | set(pb["entradas"])):
        ea, eb = pa["entradas"].get(k), pb["entradas"].get(k)
        print("  %-45s %s" % (k, "igual" if ea == eb else "CAMBIO"))
    print("  parametros:", "igual" if pa["parametros_sha256_16"] == pb["parametros_sha256_16"] else "CAMBIO",
          "| cambios en la corrida:", list(pb.get("cambios", {})) or "ninguno")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
