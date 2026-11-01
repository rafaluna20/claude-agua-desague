#!/usr/bin/env python3
"""Audita el frente geométrico de lotes contra vías/pasajes seleccionados.

El resultado es un control espacial preliminar. Una distancia menor o igual a
la tolerancia indica cercanía geométrica; no sustituye servidumbres, veredas ni
la comprobación de acceso construible en campo.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

from shapely.geometry import Polygon


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def polygon(vertices: list[list[float]], code: str) -> Polygon:
    geometry = Polygon(vertices)
    if geometry.is_empty:
        raise ValueError(f"{code}: polígono vacío.")
    if not geometry.is_valid:
        geometry = geometry.buffer(0)
    if geometry.is_empty:
        raise ValueError(f"{code}: polígono inválido incluso tras normalización para auditoría.")
    return geometry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parcels", required=True, type=Path)
    parser.add_argument("--roads", required=True, type=Path, help="vias_primera_expediente_v1.json")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--tolerance", default=1.0, type=float, help="Distancia máxima en unidades del DWG (default 1.0)")
    args = parser.parse_args()
    if args.tolerance < 0:
        parser.error("La tolerancia no puede ser negativa.")
    for source in (args.parcels, args.roads):
        if not source.is_file():
            parser.error(f"No se encontró: {source}")
    if args.output.exists():
        parser.error(f"La salida ya existe; no se sobrescribe: {args.output}")

    parcels = json.loads(args.parcels.read_text(encoding="utf-8"))
    road_document = json.loads(args.roads.read_text(encoding="utf-8"))
    roads: list[tuple[str, str, str, Polygon]] = []
    for category in ("streets", "passages"):
        for code, row in road_document[category].items():
            roads.append((code, str(row.get("nombre", code)), category, polygon(row["coordinates"], code)))

    records = []
    count_street = count_passage = count_none = 0
    for code in sorted(parcels):
        lot = polygon(parcels[code], code)
        candidates = []
        nearest = None
        for road_code, road_name, category, road in roads:
            distance = lot.distance(road)
            item = {"codigo": road_code, "nombre": road_name, "tipo": category, "distancia": round(distance, 3)}
            if nearest is None or distance < nearest["distancia"]:
                nearest = item
            if distance <= args.tolerance:
                candidates.append(item)
        types = {item["tipo"] for item in candidates}
        if "streets" in types:
            status = "FRENTE_CALLE"
            count_street += 1
        elif "passages" in types:
            status = "FRENTE_PASAJE"
            count_passage += 1
        else:
            status = "SIN_FRENTE_GEOMETRICO"
            count_none += 1
        records.append({"codigo": code, "estado": status, "viasEnTolerancia": candidates, "viaMasCercana": nearest})

    result = {
        "purpose": "Auditoría geométrica preliminar de acceso de lote a vía para diseño sanitario.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "parcelsFile": args.parcels.name,
            "parcelsSha256": sha256(args.parcels),
            "roadsFile": args.roads.name,
            "roadsSha256": sha256(args.roads),
        },
        "tolerance": args.tolerance,
        "caveat": "La tolerancia se expresa en unidades del DWG, interpretadas provisionalmente como metros. Validar acceso físico, servidumbres y trazo oficial antes de diseñar red.",
        "summary": {
            "totalParcels": len(records),
            "frontStreet": count_street,
            "frontPassageOnly": count_passage,
            "withoutGeometricFront": count_none,
        },
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
