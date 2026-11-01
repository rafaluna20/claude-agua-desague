#!/usr/bin/env python3
"""Documenta alternativas geométricas de interfaz en lotes de referencia.

Usa el frente de cada lote y el grafo vial preliminar. No localiza un medidor,
una cámara, una tubería existente ni el punto definitivo de ingreso a PTAR.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from shapely.geometry import LineString, Polygon
from shapely.ops import nearest_points

from procesar_grid_terreno import TerrainGrid, read_grid


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def pair(point):
    return [round(point.x, 3), round(point.y, 3)]


def candidates_for_lot(code, role, assignment, parcels, graph, grid):
    lot = Polygon(parcels[code])
    record = next(item for item in assignment["records"] if item["codigo"] == code)
    front_codes = [item["codigo"] for item in record["viasDeFrente"]]
    results = []
    for road_code in front_codes:
        options = []
        for edge in graph["edges"]:
            if edge["origin"] != "EJE_VIAL" or edge["source"]["codigo"] != road_code:
                continue
            line = LineString(edge["coordinates"])
            lot_point, axis_point = nearest_points(lot.boundary, line)
            options.append((lot_point.distance(axis_point), edge, lot_point, axis_point))
        if not options:
            raise ValueError(f"Sin tramo de eje vial para {code}/{road_code}")
        distance, edge, lot_point, axis_point = min(options, key=lambda item: (item[0], item[1]["id"]))
        z, method = grid.sample(axis_point.x, axis_point.y)
        results.append({
            "via": road_code,
            "tramoVial": edge["id"],
            "nodoDesde": edge["fromNode"],
            "nodoHasta": edge["toNode"],
            "puntoLoteProvisional": pair(lot_point),
            "puntoEjeProvisional": pair(axis_point),
            "distanciaLoteAEje": round(distance, 3),
            "cotaTerrenoEje": None if z is None else round(z, 3),
            "metodoCota": method,
        })
    centroid = lot.centroid
    z_centroid, centroid_method = grid.sample(centroid.x, centroid.y)
    return {
        "rol": role,
        "predioReferencia": code,
        "centroidePredio": pair(centroid),
        "cotaTerrenoCentroide": None if z_centroid is None else round(z_centroid, 3),
        "metodoCotaCentroide": centroid_method,
        "alternativasGeometricas": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcels", required=True)
    parser.add_argument("--assignment", required=True)
    parser.add_argument("--graph", required=True)
    parser.add_argument("--grid", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--min-x", required=True, type=float)
    parser.add_argument("--min-y", required=True, type=float)
    parser.add_argument("--cell-size", required=True, type=float)
    parser.add_argument("--nx", required=True, type=int)
    parser.add_argument("--ny", required=True, type=int)
    args = parser.parse_args()

    paths = {key: Path(getattr(args, key)) for key in ("parcels", "assignment", "graph", "grid", "output")}
    if paths["output"].exists():
        raise SystemExit(f"El archivo de salida ya existe: {paths['output']}")
    parcels = json.loads(paths["parcels"].read_text(encoding="utf-8-sig"))
    assignment = json.loads(paths["assignment"].read_text(encoding="utf-8-sig"))
    graph = json.loads(paths["graph"].read_text(encoding="utf-8-sig"))
    grid = TerrainGrid(
        values=read_grid(paths["grid"], args.nx, args.ny),
        min_x=args.min_x, min_y=args.min_y, cell_size=args.cell_size, nx=args.nx, ny=args.ny,
    )
    references = [
        candidates_for_lot("E01MZD155P", "FUENTE_DE_AGUA_REFERENCIAL_SANTA_MARIA", assignment, parcels, graph, grid),
        candidates_for_lot("E03MZD049P", "DESTINO_PTAR_REFERENCIAL", assignment, parcels, graph, grid),
    ]
    result = {
        "version": "v4_primera_expediente_interfaces_referenciales_v1",
        "purpose": "Alternativas geométricas de interfaz junto a los predios de referencia de Santa María y PTAR; no constituye definición de puntos físicos, factibilidad ni diseño de red.",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "parcelsFile": paths["parcels"].name,
            "parcelsSha256": sha256(paths["parcels"]),
            "assignmentFile": paths["assignment"].name,
            "assignmentSha256": sha256(paths["assignment"]),
            "graphFile": paths["graph"].name,
            "graphSha256": sha256(paths["graph"]),
            "gridFile": paths["grid"].name,
            "gridSha256": sha256(paths["grid"]),
        },
        "limitations": [
            "El usuario indicó Santa María a la mano derecha de E01MZD155P y el destino PTAR en E03MZD049P; falta la coordenada física exacta de ambos puntos.",
            "Las cotas provienen de terreno natural interpolado sobre grilla de 1 m, no de estructuras hidráulicas.",
            "La orientación derecha/izquierda no se interpreta sin un eje de referencia y la inspección de campo.",
        ],
        "references": references,
    }
    paths["output"].parent.mkdir(parents=True, exist_ok=True)
    paths["output"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({item["predioReferencia"]: len(item["alternativasGeometricas"]) for item in references}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError, StopIteration) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
