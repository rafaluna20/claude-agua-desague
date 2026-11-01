#!/usr/bin/env python3
"""Muestrea terreno en nodos y aristas de un grafo vial preliminar.

El resultado caracteriza el terreno natural. No asigna sentido de flujo,
profundidades, rasantes, buzones ni diámetros de una red sanitaria.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from procesar_grid_terreno import TerrainGrid, read_grid


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", required=True)
    parser.add_argument("--grid", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--min-x", required=True, type=float)
    parser.add_argument("--min-y", required=True, type=float)
    parser.add_argument("--cell-size", required=True, type=float)
    parser.add_argument("--nx", required=True, type=int)
    parser.add_argument("--ny", required=True, type=int)
    parser.add_argument("--flat-slope-threshold", type=float, default=0.002)
    args = parser.parse_args()

    if args.flat_slope_threshold < 0:
        parser.error("flat-slope-threshold no puede ser negativo")
    graph_path = Path(args.graph)
    grid_path = Path(args.grid)
    output_path = Path(args.output)
    if output_path.exists():
        raise SystemExit(f"El archivo de salida ya existe: {output_path}")

    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    grid = TerrainGrid(
        values=read_grid(grid_path, args.nx, args.ny),
        min_x=args.min_x,
        min_y=args.min_y,
        cell_size=args.cell_size,
        nx=args.nx,
        ny=args.ny,
    )
    node_elevation = {}
    node_records = []
    for node in graph["nodes"]:
        x, y = node["coordinate"]
        z, method = grid.sample(x, y)
        node_elevation[node["id"]] = z
        node_records.append({
            "id": node["id"],
            "coordinate": [round(x, 3), round(y, 3)],
            "degree": node["degree"],
            "cotaTerreno": None if z is None else round(z, 3),
            "metodo": method,
        })

    edge_records = []
    valid_slopes = []
    for edge in graph["edges"]:
        z_from = node_elevation[edge["fromNode"]]
        z_to = node_elevation[edge["toNode"]]
        length = edge["length"]
        if z_from is None or z_to is None or length <= 0:
            slope = None
            classification = "SIN_COTA_TIN"
        else:
            slope = (z_from - z_to) / length
            valid_slopes.append(slope)
            if abs(slope) <= args.flat_slope_threshold:
                classification = "TERRENO_CASI_PLANO"
            elif slope > 0:
                classification = "TERRENO_DESCIENDE_DE_DESDE_A_HASTA"
            else:
                classification = "TERRENO_DESCIENDE_DE_HASTA_A_DESDE"
        item = {
            "id": edge["id"],
            "origen": edge["origin"],
            "nodoDesde": edge["fromNode"],
            "nodoHasta": edge["toNode"],
            "longitud": length,
            "cotaTerrenoDesde": None if z_from is None else round(z_from, 3),
            "cotaTerrenoHasta": None if z_to is None else round(z_to, 3),
            "pendienteTerrenoDesdeAHasta": None if slope is None else round(slope, 6),
            "clasificacion": classification,
        }
        if edge.get("source"):
            source = edge["source"]
            if "codigo" in source:
                item["via"] = source["codigo"]
            else:
                item["conexionVial"] = source["id"]
                item["viasConectadas"] = [source["from"], source["to"]]
        edge_records.append(item)

    result = {
        "version": "v4_primera_expediente_grafo_topografico_v1",
        "purpose": "Caracterización de cotas y pendientes de terreno natural sobre el grafo vial preliminar; no constituye perfil hidráulico ni define sentido de flujo.",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "graphFile": graph_path.name,
            "graphSha256": sha256(graph_path),
            "gridFile": grid_path.name,
            "gridSha256": sha256(grid_path),
        },
        "method": {
            "surface": "terreno natural de Civil 3D exportada a grilla de 1 m",
            "sampling": "interpolación bilineal en nodos del grafo",
            "flatSlopeThreshold": args.flat_slope_threshold,
            "unitsNote": "Coordenadas y distancias interpretadas provisionalmente como metros; datum vertical y documentación topográfica continúan pendientes.",
        },
        "summary": {
            "nodes": len(node_records),
            "nodesWithoutElevation": sum(item["cotaTerreno"] is None for item in node_records),
            "edges": len(edge_records),
            "edgesWithoutSlope": sum(item["pendienteTerrenoDesdeAHasta"] is None for item in edge_records),
            "terrainSlopeMinimum": None if not valid_slopes else round(min(valid_slopes), 6),
            "terrainSlopeMaximum": None if not valid_slopes else round(max(valid_slopes), 6),
            "terrainNearlyFlat": sum(item["clasificacion"] == "TERRENO_CASI_PLANO" for item in edge_records),
        },
        "nodes": node_records,
        "edges": edge_records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
