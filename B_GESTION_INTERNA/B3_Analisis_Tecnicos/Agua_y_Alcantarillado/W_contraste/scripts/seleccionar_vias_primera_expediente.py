#!/usr/bin/env python3
"""Selecciona las vías y pasajes que intersectan 00_primera_expediente.

No modifica las fuentes v3 ni el DWG. Conserva la geometría completa de cada
vía seleccionada para permitir después derivar ejes y perfiles con una regla
explícita de recorte/prolongación.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from filtrar_primera_expediente import polygon_crosses_boundary, point_in_polygon, same_point


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def intersects_scope(vertices: list[list[float]], boundary: list[list[float]]) -> bool:
    return (
        any(point_in_polygon(point, boundary) for point in vertices)
        or any(point_in_polygon(point, vertices) for point in boundary)
        or polygon_crosses_boundary(vertices, boundary)
    )


def select(source: dict[str, dict[str, object]], boundary: list[list[float]]) -> dict[str, dict[str, object]]:
    selected: dict[str, dict[str, object]] = {}
    for code, value in source.items():
        vertices = value.get("coordinates")
        if not isinstance(vertices, list) or len(vertices) < 3:
            raise ValueError(f"{code}: geometría inválida o no poligonal.")
        if intersects_scope(vertices, boundary):
            selected[code] = value
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boundary", required=True, type=Path)
    parser.add_argument("--streets", required=True, type=Path)
    parser.add_argument("--passages", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    for source in (args.boundary, args.streets, args.passages):
        if not source.is_file():
            parser.error(f"No se encontró: {source}")
    if args.output.exists():
        parser.error(f"La salida ya existe; no se sobrescribe: {args.output}")

    boundary_document = json.loads(args.boundary.read_text(encoding="utf-8"))
    boundary = boundary_document["coordinates"]
    if len(boundary) > 2 and same_point(boundary[0], boundary[-1]):
        boundary = boundary[:-1]
    streets = json.loads(args.streets.read_text(encoding="utf-8"))
    passages = json.loads(args.passages.read_text(encoding="utf-8"))
    selected_streets = select(streets, boundary)
    selected_passages = select(passages, boundary)
    output = {
        "version": "v4_primera_expediente_vias_v1",
        "purpose": "Base de vías para derivar ejes y redes preliminares; no son ejes hidráulicos ni trazos de tubería.",
        "boundary": {
            "layer": boundary_document.get("sourceLayer"),
            "handle": boundary_document.get("sourceHandle"),
            "sha256": file_hash(args.boundary),
        },
        "sources": {
            "streetsFile": args.streets.name,
            "streetsSha256": file_hash(args.streets),
            "passagesFile": args.passages.name,
            "passagesSha256": file_hash(args.passages),
        },
        "selectionRule": "Seleccionar si un vértice de la vía cae dentro/sobre el límite, un vértice del límite cae dentro/sobre la vía, o sus lados se intersectan.",
        "counts": {"streets": len(selected_streets), "passages": len(selected_passages)},
        "streets": selected_streets,
        "passages": selected_passages,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output["counts"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
