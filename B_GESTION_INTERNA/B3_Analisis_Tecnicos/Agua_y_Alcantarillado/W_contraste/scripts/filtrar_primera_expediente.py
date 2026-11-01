"""Clasifica lotes de Civil 3D contra el limite 00_primera_expediente.

No modifica el DWG. Un lote entra a la salida principal solo si todos sus
vertices caen dentro/sobre el limite y ninguno de sus lados lo cruza.
Los casos de borde se conservan separados para revision humana.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EPS = 1e-6


def same_point(a: list[float], b: list[float]) -> bool:
    return abs(a[0] - b[0]) <= EPS and abs(a[1] - b[1]) <= EPS


def point_on_segment(point: list[float], a: list[float], b: list[float]) -> bool:
    cross = (point[0] - a[0]) * (b[1] - a[1]) - (point[1] - a[1]) * (b[0] - a[0])
    if abs(cross) > EPS:
        return False
    return (point[0] - a[0]) * (point[0] - b[0]) + (point[1] - a[1]) * (point[1] - b[1]) <= EPS


def point_in_polygon(point: list[float], polygon: list[list[float]]) -> bool:
    inside = False
    for index, current in enumerate(polygon):
        previous = polygon[index - 1]
        if point_on_segment(point, previous, current):
            return True
        if (current[1] > point[1]) != (previous[1] > point[1]):
            crossing_x = (previous[0] - current[0]) * (point[1] - current[1]) / (previous[1] - current[1]) + current[0]
            if point[0] < crossing_x:
                inside = not inside
    return inside


def orientation(a: list[float], b: list[float], c: list[float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_intersect(a: list[float], b: list[float], c: list[float], d: list[float]) -> bool:
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    if ((o1 > EPS and o2 < -EPS) or (o1 < -EPS and o2 > EPS)) and ((o3 > EPS and o4 < -EPS) or (o3 < -EPS and o4 > EPS)):
        return True
    return (
        abs(o1) <= EPS and point_on_segment(c, a, b)
        or abs(o2) <= EPS and point_on_segment(d, a, b)
        or abs(o3) <= EPS and point_on_segment(a, c, d)
        or abs(o4) <= EPS and point_on_segment(b, c, d)
    )


def polygon_centroid(vertices: list[list[float]]) -> list[float]:
    twice_area = cx = cy = 0.0
    for index, point in enumerate(vertices):
        other = vertices[(index + 1) % len(vertices)]
        cross = point[0] * other[1] - other[0] * point[1]
        twice_area += cross
        cx += (point[0] + other[0]) * cross
        cy += (point[1] + other[1]) * cross
    if abs(twice_area) <= EPS:
        return [sum(point[0] for point in vertices) / len(vertices), sum(point[1] for point in vertices) / len(vertices)]
    return [cx / (3 * twice_area), cy / (3 * twice_area)]


def polygon_crosses_boundary(vertices: list[list[float]], boundary: list[list[float]]) -> bool:
    for index, point in enumerate(vertices):
        next_point = vertices[(index + 1) % len(vertices)]
        for boundary_index, boundary_point in enumerate(boundary):
            next_boundary = boundary[(boundary_index + 1) % len(boundary)]
            if segments_intersect(point, next_point, boundary_point, next_boundary):
                return True
    return False


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--boundary", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    raw = json.loads(args.raw.read_text(encoding="utf-8"))
    boundary_document = json.loads(args.boundary.read_text(encoding="utf-8"))
    boundary = boundary_document["coordinates"]
    if len(boundary) > 2 and same_point(boundary[0], boundary[-1]):
        boundary = boundary[:-1]

    outputs = {
        "inside": args.out_dir / "parcels_primera_expediente.json",
        "review": args.out_dir / "lotes_limite_a_revisar.json",
        "classification": args.out_dir / "clasificacion_lotes_primera_expediente.json",
        "summary": args.out_dir / "resumen_extraccion.json",
    }
    existing = [str(path) for path in outputs.values() if path.exists()]
    if existing:
        raise SystemExit("No se sobrescriben salidas existentes: " + "; ".join(existing))

    inside: dict[str, list[list[float]]] = {}
    review: dict[str, dict[str, object]] = {}
    classification: list[dict[str, object]] = []
    for code, vertices in raw.items():
        all_inside = all(point_in_polygon(point, boundary) for point in vertices)
        crosses = polygon_crosses_boundary(vertices, boundary)
        centroid = polygon_centroid(vertices)
        centroid_inside = point_in_polygon(centroid, boundary)
        if all_inside and not crosses:
            label = "DENTRO"
            inside[code] = vertices
        elif crosses or centroid_inside:
            label = "REVISAR_LIMITE"
            review[code] = {
                "coordinates": vertices,
                "centroid": centroid,
                "centroidInside": centroid_inside,
                "intersectsBoundary": crosses,
            }
        else:
            label = "FUERA"
        classification.append(
            {
                "codigo": code,
                "clasificacion": label,
                "vertices": len(vertices),
                "centroid": centroid,
                "centroideDentro": centroid_inside,
                "intersectaLimite": crosses,
            }
        )

    summary = {
        "version": "v4_primera_expediente",
        "extractionDate": "2026-10-10",
        "sourceDrawingLayer": "00_lotes_terraLima",
        "sourceTextLayer": "01_LT_TXT",
        "boundaryLayer": boundary_document["sourceLayer"],
        "boundaryHandle": boundary_document["sourceHandle"],
        "coordinateSystem": "UTM segun dibujo Civil 3D; zona y datum deben confirmarse con topografia.",
        "rawExportFile": args.raw.name,
        "rawExportSha256": sha256(args.raw),
        "totalLotes": len(raw),
        "dentro": len(inside),
        "revisarLimite": len(review),
        "fuera": sum(1 for row in classification if row["clasificacion"] == "FUERA"),
        "membershipRule": "DENTRO: todos los vertices dentro/sobre el limite y sin interseccion. REVISAR_LIMITE: interseccion o centroide dentro con vertices fuera.",
        "script": "scripts/filtrar_primera_expediente.py",
    }
    write_json(outputs["inside"], inside)
    write_json(outputs["review"], review)
    write_json(outputs["classification"], classification)
    write_json(outputs["summary"], summary)
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
