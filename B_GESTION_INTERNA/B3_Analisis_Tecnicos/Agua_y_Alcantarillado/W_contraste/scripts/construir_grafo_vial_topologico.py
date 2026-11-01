#!/usr/bin/env python3
"""Construye un grafo vial con nodos topológicos explícitos.

A diferencia de una unión geométrica implícita, cada conexión inferida se
proyecta exactamente sobre ambos ejes y los divide en subtramos. Así, la
conectividad del grafo no depende de redondeos de coordenadas ni de que un
motor GIS node automáticamente líneas casi coincidentes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

from shapely.geometry import LineString, Polygon
from shapely.ops import nearest_points, substring


EPS = 1e-6


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def polygon(vertices: list[list[float]], label: str) -> Polygon:
    result = Polygon(vertices)
    if not result.is_valid:
        result = result.buffer(0)
    if result.is_empty:
        raise ValueError(f"Geometría vial inválida: {label}")
    return result


def node_key(point: object) -> tuple[float, float]:
    return round(point.x, 6), round(point.y, 6)


def display_coordinates(line: LineString) -> list[list[float]]:
    return [[round(x, 3), round(y, 3)] for x, y in line.coords]


def unique_positions(values: list[float]) -> list[float]:
    result = []
    for value in sorted(values):
        if not result or abs(value - result[-1]) > EPS:
            result.append(value)
    return result


def component_sizes(adjacency: dict[str, set[str]]) -> list[int]:
    unseen = set(adjacency)
    sizes = []
    while unseen:
        start = unseen.pop()
        queue: deque[str] = deque([start])
        members = {start}
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in members:
                    members.add(neighbor)
                    unseen.discard(neighbor)
                    queue.append(neighbor)
        sizes.append(len(members))
    return sorted(sizes, reverse=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roads", type=Path, required=True)
    parser.add_argument("--axes", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--polygon-tolerance", type=float, default=0.05)
    parser.add_argument("--max-axis-gap", type=float, default=25.0)
    args = parser.parse_args()
    if args.polygon_tolerance < 0 or args.max_axis_gap <= 0:
        parser.error("Tolerancias inválidas.")
    for source in (args.roads, args.axes):
        if not source.is_file():
            parser.error(f"No se encontró: {source}")
    if args.output.exists():
        parser.error(f"La salida ya existe; no se sobrescribe: {args.output}")

    road_doc = json.loads(args.roads.read_text(encoding="utf-8"))
    axes_doc = json.loads(args.axes.read_text(encoding="utf-8"))
    roads: dict[str, dict[str, object]] = {}
    for category in ("streets", "passages"):
        for code, row in road_doc[category].items():
            roads[code] = {"name": row.get("nombre", code), "type": category, "geometry": polygon(row["coordinates"], code)}
    axes = {row["source"]["codigo"]: LineString(row["coordinates"]) for row in axes_doc["axes"]}
    missing = sorted(set(roads) - set(axes))
    if missing:
        raise ValueError("Vías sin eje: " + ", ".join(missing))
    if len(axes) != len(axes_doc["axes"]):
        raise ValueError("El archivo de ejes debe tener un eje principal único por vía.")

    anchors: dict[str, list[float]] = {code: [0.0, line.length] for code, line in axes.items()}
    connectors = []
    deferred = []
    codes = sorted(roads)
    for index, left_code in enumerate(codes):
        for right_code in codes[index + 1:]:
            left_road, right_road = roads[left_code], roads[right_code]
            polygon_distance = left_road["geometry"].distance(right_road["geometry"])
            if polygon_distance > args.polygon_tolerance:
                continue
            left_point, right_point = nearest_points(axes[left_code], axes[right_code])
            gap = left_point.distance(right_point)
            row = {
                "id": f"CX-{len(connectors) + len(deferred) + 1:03d}", "from": left_code, "to": right_code,
                "polygonDistance": round(polygon_distance, 3), "axisGap": round(gap, 3),
                "fromPoint": [round(left_point.x, 3), round(left_point.y, 3)],
                "toPoint": [round(right_point.x, 3), round(right_point.y, 3)],
                "status": "INFERIDA_POR_CONTIGUIDAD_VIAL",
            }
            if gap > args.max_axis_gap:
                row["status"] = "REVISAR_GAP_MAYOR_AL_MAXIMO"
                deferred.append(row)
                continue
            row["fromPosition"] = axes[left_code].project(left_point)
            row["toPosition"] = axes[right_code].project(right_point)
            connectors.append(row)
            anchors[left_code].append(row["fromPosition"])
            anchors[right_code].append(row["toPosition"])

    nodes: dict[tuple[float, float], str] = {}
    adjacency: defaultdict[str, set[str]] = defaultdict(set)
    edges = []

    def node_for(point: object) -> str:
        key = node_key(point)
        if key not in nodes:
            nodes[key] = f"NV-{len(nodes) + 1:04d}"
        return nodes[key]

    def append_edge(line: LineString, origin: str, source: dict[str, object]) -> None:
        if line.is_empty or line.length <= EPS:
            return
        start_point, end_point = line.boundary.geoms
        start_node, end_node = node_for(start_point), node_for(end_point)
        if start_node == end_node:
            return
        edge_id = f"TV-{len(edges) + 1:04d}"
        edges.append({"id": edge_id, "fromNode": start_node, "toNode": end_node, "length": round(line.length, 3), "origin": origin, "source": source, "coordinates": display_coordinates(line)})
        adjacency[start_node].add(end_node)
        adjacency[end_node].add(start_node)

    for code, line in sorted(axes.items()):
        positions = unique_positions(anchors[code])
        for first, second in zip(positions, positions[1:]):
            append_edge(substring(line, first, second), "EJE_VIAL", {"codigo": code, "nombre": roads[code]["name"], "tipo": roads[code]["type"]})

    for connector in connectors:
        left = axes[connector["from"]].interpolate(connector["fromPosition"])
        right = axes[connector["to"]].interpolate(connector["toPosition"])
        append_edge(LineString([left, right]), "CONEXION_INFERIDA", {"id": connector["id"], "from": connector["from"], "to": connector["to"]})

    node_rows = [{"id": node_id, "coordinate": [key[0], key[1]], "degree": len(adjacency[node_id])} for key, node_id in sorted(nodes.items(), key=lambda item: item[1])]
    sizes = component_sizes(adjacency) if adjacency else []
    result = {
        "version": "v4_primera_expediente_grafo_vial_v3",
        "purpose": "Grafo vial topológico preliminar para evaluar alternativas de red; no representa infraestructura existente ni diseño hidráulico.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {"roadsFile": args.roads.name, "roadsSha256": sha256(args.roads), "axesFile": args.axes.name, "axesSha256": sha256(args.axes)},
        "method": {"connectorRule": "Solo se enlazan polígonos viales contiguos dentro de polygonTolerance. Los puntos de enlace se proyectan sobre ambos ejes y los dividen explícitamente.", "polygonTolerance": args.polygon_tolerance, "maxAxisGap": args.max_axis_gap, "unitsNote": "Unidades interpretadas provisionalmente como metros por geometría UTM; validar documentación topográfica."},
        "summary": {"roadAxes": len(axes), "inferredConnectors": len(connectors), "deferredConnectors": len(deferred), "nodes": len(node_rows), "edges": len(edges), "components": len(sizes), "componentNodeCounts": sizes},
        "connectors": [{key: value for key, value in row.items() if key not in ("fromPosition", "toPosition")} for row in connectors],
        "deferredConnectors": deferred,
        "nodes": node_rows,
        "edges": edges,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
