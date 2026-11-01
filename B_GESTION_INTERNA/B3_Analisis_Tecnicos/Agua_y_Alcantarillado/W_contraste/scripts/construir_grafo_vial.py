#!/usr/bin/env python3
"""Construye un grafo vial revisable a partir de ejes y polígonos contiguos.

Una calle/pasaje se conecta solo cuando sus polígonos viales están contiguos
dentro de `polygon-tolerance`. El enlace entre sus ejes centrales se incorpora
como `INFERIDA_POR_CONTIGUIDAD_VIAL`, con distancia y pares fuente explícitos.
No representa colectores, agua ni obras existentes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

from shapely.geometry import LineString, Polygon
from shapely.ops import nearest_points, unary_union


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def geometry(vertices: list[list[float]], label: str) -> Polygon:
    result = Polygon(vertices)
    if not result.is_valid:
        result = result.buffer(0)
    if result.is_empty:
        raise ValueError(f"Geometría vial inválida: {label}")
    return result


def flatten_lines(value: object) -> list[LineString]:
    if value.is_empty:
        return []
    if value.geom_type == "LineString":
        return [value]
    result: list[LineString] = []
    for child in value.geoms:
        result.extend(flatten_lines(child))
    return result


def coordinate(point: object) -> list[float]:
    return [round(point.x, 3), round(point.y, 3)]


def node_key(point: object) -> tuple[float, float]:
    return (round(point.x, 3), round(point.y, 3))


def component_sizes(adjacency: dict[str, set[str]]) -> list[int]:
    unseen = set(adjacency)
    sizes = []
    while unseen:
        start = unseen.pop()
        queue: deque[str] = deque([start])
        component = {start}
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor not in component:
                    component.add(neighbor)
                    unseen.discard(neighbor)
                    queue.append(neighbor)
        sizes.append(len(component))
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
            roads[code] = {"code": code, "name": row.get("nombre", code), "type": category, "geometry": geometry(row["coordinates"], code)}
    axes: dict[str, LineString] = {}
    for row in axes_doc["axes"]:
        code = row["source"]["codigo"]
        if code in axes:
            raise ValueError(f"Hay más de un eje para {code}; usar primero un archivo con eje principal único.")
        axes[code] = LineString(row["coordinates"])
    missing_axes = sorted(set(roads) - set(axes))
    if missing_axes:
        raise ValueError("Vías sin eje: " + ", ".join(missing_axes))

    connectors = []
    connector_geometries: dict[str, LineString] = {}
    deferred = []
    codes = sorted(roads)
    for index, left_code in enumerate(codes):
        for right_code in codes[index + 1:]:
            left, right = roads[left_code], roads[right_code]
            polygon_distance = left["geometry"].distance(right["geometry"])
            if polygon_distance > args.polygon_tolerance:
                continue
            left_point, right_point = nearest_points(axes[left_code], axes[right_code])
            axis_gap = left_point.distance(right_point)
            item = {
                "id": f"CX-{len(connectors) + len(deferred) + 1:03d}",
                "from": left_code,
                "to": right_code,
                "polygonDistance": round(polygon_distance, 3),
                "axisGap": round(axis_gap, 3),
                "fromPoint": coordinate(left_point),
                "toPoint": coordinate(right_point),
                "status": "INFERIDA_POR_CONTIGUIDAD_VIAL",
            }
            if axis_gap <= 0.001:
                item["status"] = "EJES_YA_CONECTADOS"
                connectors.append(item)
            elif axis_gap <= args.max_axis_gap:
                connectors.append(item)
                # Se conserva precisión completa para nodificar; los puntos del JSON son solo presentación.
                connector_geometries[item["id"]] = LineString([left_point, right_point])
            else:
                item["status"] = "REVISAR_GAP_MAYOR_AL_MAXIMO"
                deferred.append(item)

    source_lines: list[tuple[str, dict[str, object], LineString]] = []
    for code, line in axes.items():
        source_lines.append(("EJE_VIAL", {"codigo": code, "nombre": roads[code]["name"], "tipo": roads[code]["type"]}, line))
    link_lines = []
    for connector in connectors:
        if connector["axisGap"] > 0.001:
            line = connector_geometries[connector["id"]]
            source_lines.append(("CONEXION_INFERIDA", {"id": connector["id"], "from": connector["from"], "to": connector["to"]}, line))
            link_lines.append(line)
    noded = unary_union([line for _, _, line in source_lines])
    segments = flatten_lines(noded)

    nodes: dict[tuple[float, float], str] = {}
    edge_rows = []
    node_edges: defaultdict[str, set[str]] = defaultdict(set)
    for index, line in enumerate(segments, start=1):
        start, end = line.boundary.geoms
        start_key, end_key = node_key(start), node_key(end)
        if start_key == end_key or line.length <= 0.001:
            continue
        for key in (start_key, end_key):
            nodes.setdefault(key, f"NV-{len(nodes) + 1:04d}")
        midpoint = line.interpolate(0.5, normalized=True)
        kind, source, _ = min(source_lines, key=lambda item: midpoint.distance(item[2]))
        edge_id = f"TV-{len(edge_rows) + 1:04d}"
        start_id, end_id = nodes[start_key], nodes[end_key]
        node_edges[start_id].add(end_id)
        node_edges[end_id].add(start_id)
        edge_rows.append({
            "id": edge_id,
            "fromNode": start_id,
            "toNode": end_id,
            "length": round(line.length, 3),
            "origin": kind,
            "source": source,
            "coordinates": [[round(x, 3), round(y, 3)] for x, y in line.coords],
        })
    node_rows = [
        {"id": node_id, "coordinate": [key[0], key[1]], "degree": len(node_edges[node_id])}
        for key, node_id in sorted(nodes.items(), key=lambda item: item[1])
    ]
    sizes = component_sizes(node_edges) if node_edges else []
    result = {
        "version": "v4_primera_expediente_grafo_vial_v1",
        "purpose": "Grafo vial preliminar para evaluar alternativas de red; no representa infraestructura existente ni diseño hidráulico.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {"roadsFile": args.roads.name, "roadsSha256": sha256(args.roads), "axesFile": args.axes.name, "axesSha256": sha256(args.axes)},
        "method": {"connectorRule": "Solo se conectan ejes de polígonos viales contiguos dentro de polygonTolerance; cada enlace se etiqueta como inferido.", "polygonTolerance": args.polygon_tolerance, "maxAxisGap": args.max_axis_gap, "unitsNote": "Unidades interpretadas provisionalmente como metros por geometría UTM; validar en la documentación topográfica."},
        "summary": {"roadAxes": len(axes), "inferredConnectors": sum(row["axisGap"] > 0.001 for row in connectors), "alreadyConnectedPairs": sum(row["axisGap"] <= 0.001 for row in connectors), "deferredConnectors": len(deferred), "nodes": len(node_rows), "edges": len(edge_rows), "components": len(sizes), "componentNodeCounts": sizes},
        "connectors": connectors,
        "deferredConnectors": deferred,
        "nodes": node_rows,
        "edges": edge_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
