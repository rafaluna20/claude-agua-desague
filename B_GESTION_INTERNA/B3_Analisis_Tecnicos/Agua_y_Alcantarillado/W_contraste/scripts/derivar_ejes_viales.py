#!/usr/bin/env python3
"""Deriva ejes provisionales de polígonos de vías mediante esqueletización Zhang-Suen.

El resultado es una red de referencia para revisar y muestrear perfiles; no es
un trazo de tubería ni reemplaza ejes aprobados de vialidad. Todas las aristas
cortas se conservan marcadas para revisión, nunca se eliminan silenciosamente.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
from collections import deque
from pathlib import Path

import numpy as np
from shapely import contains_xy
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from filtrar_primera_expediente import same_point


NEIGHBOR_OFFSETS = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def as_polygon(vertices: list[list[float]], label: str) -> Polygon:
    geometry = Polygon(vertices)
    if not geometry.is_valid:
        geometry = geometry.buffer(0)
    if geometry.is_empty:
        raise ValueError(f"Geometría vacía o inválida: {label}")
    return geometry


def neighbours(image: np.ndarray) -> tuple[np.ndarray, ...]:
    padded = np.pad(image.astype(np.uint8), 1, constant_values=0)
    # P2..P9, en sentido horario desde el norte.
    return (
        padded[:-2, 1:-1], padded[:-2, 2:], padded[1:-1, 2:], padded[2:, 2:],
        padded[2:, 1:-1], padded[2:, :-2], padded[1:-1, :-2], padded[:-2, :-2],
    )


def zhang_suen(image: np.ndarray, max_iterations: int = 500) -> tuple[np.ndarray, int]:
    """Adelgazamiento binario vectorizado; bordes se interpretan como fondo."""
    result = image.astype(bool).copy()
    for iteration in range(1, max_iterations + 1):
        removed = False
        for phase in (1, 2):
            p2, p3, p4, p5, p6, p7, p8, p9 = neighbours(result)
            total = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9
            ring = (p2, p3, p4, p5, p6, p7, p8, p9, p2)
            transitions = sum((ring[index] == 0) & (ring[index + 1] == 1) for index in range(8))
            if phase == 1:
                condition_a = (p2 * p4 * p6) == 0
                condition_b = (p4 * p6 * p8) == 0
            else:
                condition_a = (p2 * p4 * p8) == 0
                condition_b = (p2 * p6 * p8) == 0
            delete = result & (total >= 2) & (total <= 6) & (transitions == 1) & condition_a & condition_b
            if delete.any():
                result[delete] = False
                removed = True
        if not removed:
            return result, iteration
    raise RuntimeError(f"Zhang-Suen no convergió en {max_iterations} iteraciones.")


def rdp(points: list[tuple[int, int]], tolerance: float) -> list[tuple[int, int]]:
    if len(points) <= 2:
        return points
    first, last = points[0], points[-1]
    dx, dy = last[0] - first[0], last[1] - first[1]
    denominator = math.hypot(dx, dy)
    if denominator == 0:
        distances = [math.hypot(point[0] - first[0], point[1] - first[1]) for point in points[1:-1]]
    else:
        distances = [abs(dy * point[0] - dx * point[1] + last[0] * first[1] - last[1] * first[0]) / denominator for point in points[1:-1]]
    if not distances:
        return [first, last]
    maximum = max(distances)
    index = distances.index(maximum) + 1
    if maximum <= tolerance:
        return [first, last]
    return rdp(points[:index + 1], tolerance)[:-1] + rdp(points[index:], tolerance)


def polyline_length(points: list[tuple[int, int]], cell_size: float) -> float:
    return sum(math.hypot(second[0] - first[0], second[1] - first[1]) * cell_size for first, second in zip(points, points[1:]))


def connected_components(pixels: set[tuple[int, int]]) -> list[set[tuple[int, int]]]:
    components = []
    unseen = set(pixels)
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
        components.append(component)
    return components


def extract_edges(skeleton: np.ndarray, cell_size: float) -> list[list[tuple[int, int]]]:
    pixels = {tuple(point) for point in np.argwhere(skeleton)}
    if not pixels:
        return []
    adjacent = {
        pixel: [(pixel[0] + dr, pixel[1] + dc) for dr, dc in NEIGHBOR_OFFSETS if (pixel[0] + dr, pixel[1] + dc) in pixels]
        for pixel in pixels
    }
    keys = {pixel for pixel, values in adjacent.items() if len(values) != 2}
    for component in connected_components(pixels):
        if not (keys & component):
            keys.add(min(component))  # anillo: se fuerza un único nodo de inicio para no perderlo

    visited_links: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    edges: list[list[tuple[int, int]]] = []
    for start in sorted(keys):
        for neighbor in adjacent[start]:
            link = tuple(sorted((start, neighbor)))
            if link in visited_links:
                continue
            chain = [start]
            previous, current = start, neighbor
            while True:
                visited_links.add(tuple(sorted((previous, current))))
                chain.append(current)
                if current in keys:
                    break
                options = [candidate for candidate in adjacent[current] if candidate != previous]
                if len(options) != 1:
                    break
                previous, current = current, options[0]
            if len(chain) > 1 and polyline_length(chain, cell_size) > 0:
                edges.append(chain)
    return edges


def pixel_coordinate(pixel: tuple[int, int], min_x: float, max_y: float, cell_size: float) -> list[float]:
    row, col = pixel
    return [round(min_x + (col + 0.5) * cell_size, 3), round(max_y - (row + 0.5) * cell_size, 3)]


def nearest_source(point: list[float], sources: list[tuple[str, str, str, object]]) -> tuple[str, str, str]:
    probe = Point(point)
    code, name, category, _ = min(sources, key=lambda item: probe.distance(item[3]))
    return code, name, category


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--roads", type=Path, required=True, help="vias_primera_expediente_v1.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cell-size", type=float, default=0.5)
    parser.add_argument("--boundary-buffer", type=float, default=5.0, help="Metros/unidades retenidos fuera del límite")
    parser.add_argument("--min-edge-length", type=float, default=6.0)
    args = parser.parse_args()
    if args.cell_size <= 0 or args.boundary_buffer < 0 or args.min_edge_length < 0:
        parser.error("cell-size debe ser positivo; boundary-buffer y min-edge-length no negativos.")
    if args.output.exists():
        parser.error(f"La salida ya existe; no se sobrescribe: {args.output}")
    for source in (args.boundary, args.roads):
        if not source.is_file():
            parser.error(f"No se encontró: {source}")

    boundary_doc = json.loads(args.boundary.read_text(encoding="utf-8"))
    boundary_points = boundary_doc["coordinates"]
    if len(boundary_points) > 2 and same_point(boundary_points[0], boundary_points[-1]):
        boundary_points = boundary_points[:-1]
    scope = as_polygon(boundary_points, "00_primera_expediente").buffer(args.boundary_buffer)
    road_doc = json.loads(args.roads.read_text(encoding="utf-8"))
    sources: list[tuple[str, str, str, object]] = []
    for category in ("streets", "passages"):
        for code, row in road_doc[category].items():
            geometry = as_polygon(row["coordinates"], code).intersection(scope)
            if not geometry.is_empty:
                sources.append((code, str(row.get("nombre", code)), category, geometry))
    if not sources:
        raise ValueError("No quedaron vías dentro del límite/buffer.")
    road_union = unary_union([item[3] for item in sources])
    min_x, min_y, max_x, max_y = scope.bounds
    nx = max(2, math.ceil((max_x - min_x) / args.cell_size))
    ny = max(2, math.ceil((max_y - min_y) / args.cell_size))
    xs = min_x + (np.arange(nx) + 0.5) * args.cell_size
    ys = max_y - (np.arange(ny) + 0.5) * args.cell_size
    x_grid, y_grid = np.meshgrid(xs, ys)
    mask = contains_xy(road_union, x_grid, y_grid)
    skeleton, iterations = zhang_suen(mask)
    raw_edges = extract_edges(skeleton, args.cell_size)
    edges = []
    for index, raw in enumerate(raw_edges, start=1):
        simplified = rdp(raw, tolerance=0.75)
        coordinates = [pixel_coordinate(pixel, min_x, max_y, args.cell_size) for pixel in simplified]
        midpoint = coordinates[len(coordinates) // 2]
        source_code, source_name, source_type = nearest_source(midpoint, sources)
        length = round(polyline_length(raw, args.cell_size), 3)
        edges.append({
            "id": f"EJE-{index:04d}",
            "source": {"codigo": source_code, "nombre": source_name, "tipo": source_type},
            "coordinates": coordinates,
            "length": length,
            "skeletonPixels": len(raw),
            "status": "CANDIDATA" if length >= args.min_edge_length else "REVISAR_CORTA",
        })
    result = {
        "version": "v4_primera_expediente_ejes_v1",
        "purpose": "Ejes provisionales de vías para revisión y muestreo topográfico; no son trazos de red ni eje vial aprobado.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "boundaryFile": args.boundary.name,
            "boundarySha256": sha256(args.boundary),
            "roadsFile": args.roads.name,
            "roadsSha256": sha256(args.roads),
        },
        "method": {
            "rasterization": "contains_xy de Shapely sobre unión de polígonos viales recortada al límite + buffer",
            "skeleton": "Zhang-Suen vectorizado",
            "cellSize": args.cell_size,
            "boundaryBuffer": args.boundary_buffer,
            "rdpTolerancePixels": 0.75,
            "minimumCandidateLength": args.min_edge_length,
            "unitsNote": "Las unidades se interpretan provisionalmente como metros por la geometría UTM; validar en documentación topográfica.",
        },
        "raster": {"minX": min_x, "minY": min_y, "maxX": max_x, "maxY": max_y, "nx": nx, "ny": ny, "roadCells": int(mask.sum()), "skeletonCells": int(skeleton.sum()), "iterations": iterations},
        "summary": {"allEdges": len(edges), "candidateEdges": sum(edge["status"] == "CANDIDATA" for edge in edges), "shortReviewEdges": sum(edge["status"] == "REVISAR_CORTA" for edge in edges)},
        "edges": edges,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
