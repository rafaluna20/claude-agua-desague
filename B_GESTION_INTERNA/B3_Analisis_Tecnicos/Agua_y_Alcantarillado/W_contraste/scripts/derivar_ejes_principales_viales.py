#!/usr/bin/env python3
"""Obtiene el eje principal de cada calle/pasaje mediante su esqueleto raster.

Cada polígono se procesa de forma independiente. Esto evita que una
intersección entre calles fragmente la red de ejes en cientos de aristas cortas.
El eje elegido es el diámetro de cada componente del esqueleto; se conservan
todos los componentes y se informa si una vía no pudo producir eje.
"""

from __future__ import annotations

import argparse
import datetime as dt
import heapq
import json
import math
from collections import deque
from pathlib import Path

import numpy as np
from shapely import contains_xy
from shapely.geometry import Polygon

from derivar_ejes_viales import NEIGHBOR_OFFSETS, as_polygon, pixel_coordinate, polyline_length, rdp, sha256, zhang_suen
from filtrar_primera_expediente import same_point


def components(pixels: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    unseen = set(pixels)
    result = []
    while unseen:
        start = unseen.pop()
        component = {start}
        queue: deque[tuple[int, int]] = deque([start])
        while queue:
            row, col = queue.popleft()
            for dr, dc in NEIGHBOR_OFFSETS:
                neighbor = (row + dr, col + dc)
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        result.append(component)
    return result


def adjacency(component: set[tuple[int, int]]) -> dict[tuple[int, int], list[tuple[int, int]]]:
    return {
        node: [(node[0] + dr, node[1] + dc) for dr, dc in NEIGHBOR_OFFSETS if (node[0] + dr, node[1] + dc) in component]
        for node in component
    }


def dijkstra(graph: dict[tuple[int, int], list[tuple[int, int]]], source: tuple[int, int]) -> tuple[tuple[int, int], dict[tuple[int, int], float], dict[tuple[int, int], tuple[int, int] | None]]:
    distances = {source: 0.0}
    previous: dict[tuple[int, int], tuple[int, int] | None] = {source: None}
    queue = [(0.0, source)]
    while queue:
        current_distance, node = heapq.heappop(queue)
        if current_distance != distances.get(node):
            continue
        for neighbor in graph[node]:
            weight = math.hypot(neighbor[0] - node[0], neighbor[1] - node[1])
            next_distance = current_distance + weight
            if next_distance < distances.get(neighbor, math.inf):
                distances[neighbor] = next_distance
                previous[neighbor] = node
                heapq.heappush(queue, (next_distance, neighbor))
    farthest = max(distances, key=distances.get)
    return farthest, distances, previous


def component_axis(component: set[tuple[int, int]]) -> list[tuple[int, int]]:
    graph = adjacency(component)
    endpoints = sorted(node for node, neighbors in graph.items() if len(neighbors) == 1)
    start = endpoints[0] if endpoints else min(component)
    first, _, _ = dijkstra(graph, start)
    last, _, previous = dijkstra(graph, first)
    path = []
    current: tuple[int, int] | None = last
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path


def process_geometry(geometry: object, cell_size: float) -> tuple[list[list[tuple[int, int]]], dict[str, int | float]]:
    min_x, min_y, max_x, max_y = geometry.bounds
    nx = max(2, math.ceil((max_x - min_x) / cell_size))
    ny = max(2, math.ceil((max_y - min_y) / cell_size))
    xs = min_x + (np.arange(nx) + 0.5) * cell_size
    ys = max_y - (np.arange(ny) + 0.5) * cell_size
    grid_x, grid_y = np.meshgrid(xs, ys)
    mask = contains_xy(geometry, grid_x, grid_y)
    skeleton, iterations = zhang_suen(mask)
    pixels = {tuple(item) for item in np.argwhere(skeleton)}
    paths = [component_axis(component) for component in components(pixels)] if pixels else []
    metadata: dict[str, int | float] = {
        "minX": min_x, "minY": min_y, "maxX": max_x, "maxY": max_y,
        "nx": nx, "ny": ny, "roadCells": int(mask.sum()), "skeletonCells": int(skeleton.sum()),
        "iterations": iterations, "components": len(paths),
    }
    return paths, metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--roads", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cell-size", type=float, default=0.5)
    parser.add_argument("--boundary-buffer", type=float, default=5.0)
    parser.add_argument("--min-axis-length", type=float, default=6.0)
    args = parser.parse_args()
    if args.cell_size <= 0 or args.boundary_buffer < 0 or args.min_axis_length < 0:
        parser.error("Parámetros de longitud inválidos.")
    if args.output.exists():
        parser.error(f"La salida ya existe; no se sobrescribe: {args.output}")
    for source in (args.boundary, args.roads):
        if not source.is_file():
            parser.error(f"No se encontró: {source}")

    boundary_doc = json.loads(args.boundary.read_text(encoding="utf-8"))
    points = boundary_doc["coordinates"]
    if len(points) > 2 and same_point(points[0], points[-1]):
        points = points[:-1]
    scope = as_polygon(points, "00_primera_expediente").buffer(args.boundary_buffer)
    road_doc = json.loads(args.roads.read_text(encoding="utf-8"))
    axes = []
    source_reports = []
    for category in ("streets", "passages"):
        for code, row in sorted(road_doc[category].items()):
            geometry = as_polygon(row["coordinates"], code).intersection(scope)
            if geometry.is_empty:
                source_reports.append({"codigo": code, "tipo": category, "estado": "FUERA_BUFFER", "axes": 0})
                continue
            paths, raster = process_geometry(geometry, args.cell_size)
            created = 0
            for sequence, path in enumerate(paths, start=1):
                length = polyline_length(path, args.cell_size)
                if length == 0:
                    continue
                simplified = rdp(path, tolerance=0.75)
                coordinates = [pixel_coordinate(pixel, raster["minX"], raster["maxY"], args.cell_size) for pixel in simplified]
                axes.append({
                    "id": f"EJE-{code.replace(' ', '_')}-{sequence:02d}",
                    "source": {"codigo": code, "nombre": row.get("nombre", code), "tipo": category},
                    "coordinates": coordinates,
                    "length": round(length, 3),
                    "skeletonPixels": len(path),
                    "status": "CANDIDATA" if length >= args.min_axis_length else "REVISAR_CORTA",
                })
                created += 1
            source_reports.append({"codigo": code, "tipo": category, "estado": "EJE_GENERADO" if created else "SIN_EJE_RASTER", "axes": created, "raster": raster})

    result = {
        "version": "v4_primera_expediente_ejes_v2",
        "purpose": "Ejes principales provisionales de vías/pasajes para muestreo topográfico y revisión; no son trazos de red ni ejes viales aprobados.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {"boundaryFile": args.boundary.name, "boundarySha256": sha256(args.boundary), "roadsFile": args.roads.name, "roadsSha256": sha256(args.roads)},
        "method": {"rasterization": "Cada polígono vial, recortado al límite + buffer, se rasteriza y adelgaza con Zhang-Suen; se conserva el diámetro de cada componente.", "cellSize": args.cell_size, "boundaryBuffer": args.boundary_buffer, "minimumAxisLength": args.min_axis_length, "unitsNote": "Unidades interpretadas provisionalmente como metros por la geometría UTM; validar en documentación topográfica."},
        "summary": {"sourcePolygons": len(source_reports), "sourcesWithAxis": sum(row["axes"] > 0 for row in source_reports), "sourcesWithoutAxis": sum(row["axes"] == 0 for row in source_reports), "allAxes": len(axes), "candidateAxes": sum(axis["status"] == "CANDIDATA" for axis in axes), "shortReviewAxes": sum(axis["status"] == "REVISAR_CORTA" for axis in axes)},
        "sourceReports": source_reports,
        "axes": axes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
