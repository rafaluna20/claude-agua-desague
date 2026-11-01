#!/usr/bin/env python3
"""Relaciona lotes del expediente con aristas del grafo vial preliminar.

No calcula caudales, no dibuja conexiones domiciliarias y no sustituye la
verificación de frente, servidumbre ni la definición de rasante.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from shapely.geometry import LineString, Polygon
from shapely.ops import nearest_points


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def point_pair(point):
    return [round(point.x, 3), round(point.y, 3)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcels", required=True)
    parser.add_argument("--audit", required=True)
    parser.add_argument("--graph", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    parcels_path = Path(args.parcels)
    audit_path = Path(args.audit)
    graph_path = Path(args.graph)
    output_path = Path(args.output)
    if output_path.exists():
        raise SystemExit(f"El archivo de salida ya existe: {output_path}")

    parcels = json.loads(parcels_path.read_text(encoding="utf-8-sig"))
    audit = json.loads(audit_path.read_text(encoding="utf-8-sig"))
    graph = json.loads(graph_path.read_text(encoding="utf-8-sig"))
    audit_by_code = {item["codigo"]: item for item in audit["records"]}

    by_source = {}
    for edge in graph["edges"]:
        if edge["origin"] != "EJE_VIAL":
            continue
        source_code = edge["source"]["codigo"]
        by_source.setdefault(source_code, []).append((edge, LineString(edge["coordinates"])))

    records = []
    source_counts = {}
    no_front = []
    for code in sorted(parcels):
        polygon = Polygon(parcels[code])
        if not polygon.is_valid or polygon.area <= 0:
            raise ValueError(f"Lote inválido: {code}")
        front = audit_by_code.get(code)
        if front is None:
            raise ValueError(f"Lote sin auditoría de frente: {code}")

        state = front["estado"]
        front_roads = sorted(
            front["viasEnTolerancia"],
            key=lambda item: (item["distancia"], item["codigo"]),
        )
        if state == "SIN_FRENTE_GEOMETRICO":
            no_front.append(code)
            records.append({
                "codigo": code,
                "estadoFrente": state,
                "estadoAsignacion": "PENDIENTE_SERVIDUMBRE",
                "viasDeFrente": [],
                "nota": "No se asigna tramo de red hasta validar la vereda perimetral y la servidumbre del parque (S-019).",
            })
            continue

        options = []
        for road in front_roads:
            source_code = road["codigo"]
            for edge, line in by_source.get(source_code, []):
                lot_point, network_point = nearest_points(polygon.boundary, line)
                options.append((lot_point.distance(network_point), source_code, edge["id"], edge, lot_point, network_point))
        if not options:
            raise ValueError(f"No hay arista vial para lote con frente: {code}")

        distance, source_code, edge_id, edge, lot_point, network_point = min(
            options, key=lambda item: (item[0], item[1], item[2])
        )
        source_counts[source_code] = source_counts.get(source_code, 0) + 1
        records.append({
            "codigo": code,
            "estadoFrente": state,
            "estadoAsignacion": "ASOCIADO_GEOMETRICAMENTE",
            "viasDeFrente": [
                {"codigo": item["codigo"], "tipo": item["tipo"], "distanciaAlPoligonoVial": item["distancia"]}
                for item in front_roads
            ],
            "viaSeleccionada": source_code,
            "tramoVial": edge_id,
            "nodoDesde": edge["fromNode"],
            "nodoHasta": edge["toNode"],
            "puntoLoteProvisional": point_pair(lot_point),
            "puntoEjeProvisional": point_pair(network_point),
            "distanciaLoteAEje": round(distance, 3),
            "nota": "Asociación geométrica al eje vial; no equivale a ubicación de conexión domiciliaria ni a diseño de red.",
        })

    associated = [item for item in records if item["estadoAsignacion"] == "ASOCIADO_GEOMETRICAMENTE"]
    result = {
        "version": "v4_primera_expediente_asignacion_lotes_grafo_v1",
        "purpose": "Asignación geométrica preliminar de lotes a tramos viales para estructurar alternativas de agua y desagüe; no es diseño hidráulico ni conexión domiciliaria.",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "parcelsFile": parcels_path.name,
            "parcelsSha256": sha256(parcels_path),
            "auditFile": audit_path.name,
            "auditSha256": sha256(audit_path),
            "graphFile": graph_path.name,
            "graphSha256": sha256(graph_path),
        },
        "method": {
            "frontRule": "Solo se asignan lotes con frente geométrico a la vía según la auditoría de 1.0 m.",
            "edgeRule": "Se elige la arista de eje vial de una vía de frente con menor distancia entre límite de lote y eje; desempate por código vial y tramo.",
            "unitsNote": "Distancias en unidades del DWG, interpretadas provisionalmente como metros; falta validación documental topográfica.",
        },
        "summary": {
            "totalParcels": len(records),
            "associated": len(associated),
            "pendingServitude": len(no_front),
            "frontStreet": sum(item["estadoFrente"] == "FRENTE_CALLE" for item in records),
            "frontPassageOnly": sum(item["estadoFrente"] == "FRENTE_PASAJE" for item in records),
            "maxLotToAxisDistance": round(max((item["distanciaLoteAEje"] for item in associated), default=0), 3),
            "meanLotToAxisDistance": round(sum(item["distanciaLoteAEje"] for item in associated) / len(associated), 3) if associated else 0,
        },
        "lotsPerSelectedRoad": dict(sorted(source_counts.items())),
        "pendingServitudeLots": no_front,
        "records": records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
