#!/usr/bin/env python3
"""Prepara la base de programa urbano y demanda paramétrica por lote.

No adopta viviendas, habitantes, dotación ni caudales. Es un insumo para que
esas decisiones se registren una única vez antes de modelar agua o desagüe.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from shapely.geometry import Polygon


PTAR_LOT = "E03MZD049P"
WATER_REFERENCE_LOT = "E01MZD155P"
MULTIFAMILY_THRESHOLD = 300.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcels", required=True)
    parser.add_argument("--assignment", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    parcels_path = Path(args.parcels)
    assignment_path = Path(args.assignment)
    output_path = Path(args.output)
    if output_path.exists():
        raise SystemExit(f"El archivo de salida ya existe: {output_path}")

    parcels = json.loads(parcels_path.read_text(encoding="utf-8-sig"))
    assignment = json.loads(assignment_path.read_text(encoding="utf-8-sig"))
    assignment_by_code = {item["codigo"]: item for item in assignment["records"]}
    records = []
    summary = {
        "totalLots": 0,
        "ordinaryResidentialParametric": 0,
        "multifamilyConditional": 0,
        "multifamilyUsePending": 0,
        "ptarExcluded": 0,
        "pendingServitude": 0,
    }
    for code in sorted(parcels):
        polygon = Polygon(parcels[code])
        if not polygon.is_valid or polygon.area <= 0:
            raise ValueError(f"Lote inválido: {code}")
        front = assignment_by_code.get(code)
        if front is None:
            raise ValueError(f"Lote sin asociación vial: {code}")
        area = polygon.area
        if code == PTAR_LOT:
            kind = "INFRAESTRUCTURA_PTAR_EXCLUIDA_DE_DEMANDA_RESIDENCIAL"
            floors = None
            summary["ptarExcluded"] += 1
        elif code == WATER_REFERENCE_LOT:
            kind = "MULTIFAMILIAR_CONDICIONAL_USO_PENDIENTE"
            floors = "5_a_7_si_el_uso_residencial_se_confirma"
            summary["multifamilyUsePending"] += 1
        elif area >= MULTIFAMILY_THRESHOLD:
            kind = "MULTIFAMILIAR_CONDICIONAL"
            floors = "5_a_7"
            summary["multifamilyConditional"] += 1
        else:
            kind = "VIVIENDA_ORDINARIA_PARAMETRICA"
            floors = "hasta_3_mas_azotea"
            summary["ordinaryResidentialParametric"] += 1
        if front["estadoAsignacion"] == "PENDIENTE_SERVIDUMBRE":
            summary["pendingServitude"] += 1
        records.append({
            "codigo": code,
            "areaGeometrica": round(area, 2),
            "categoriaPrograma": kind,
            "alturaRegla": floors,
            "estadoAccesoRed": front["estadoAsignacion"],
            "unidadesVivienda": None,
            "habitantesPorUnidad": None,
            "poblacionDiseno": None,
            "demandaAguaLd": None,
            "aporteDesagueLd": None,
        })
        summary["totalLots"] += 1

    result = {
        "version": "v4_primera_expediente_programa_lotes_parametrico_v1",
        "purpose": "Base por lote para población y demanda de agua/desagüe. No fija caudales ni sustituye la programación arquitectónica o comercial.",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {
            "parcelsFile": parcels_path.name,
            "parcelsSha256": sha256(parcels_path),
            "assignmentFile": assignment_path.name,
            "assignmentSha256": sha256(assignment_path),
        },
        "rulesFromUser": {
            "ordinaryLots": "hasta 3 pisos más azotea",
            "multifamilyLots": "área geométrica >=300 m²; 5 a 7 pisos",
            "ptarLot": PTAR_LOT,
            "waterReferenceLot": WATER_REFERENCE_LOT,
        },
        "requiredParametersBeforeHydraulicCalculation": [
            "unidades de vivienda por lote ordinario, o tipologías por manzana",
            "unidades de vivienda por lote multifamiliar y número de pisos adoptado",
            "habitantes por unidad y ocupación/horizonte de diseño",
            "dotación y coeficientes de variación aprobados",
            "porcentaje de retorno a desagüe y aportes no domésticos si existen",
            "confirmación de uso de E01MZD155P y solución de los cuatro lotes con servidumbre pendiente",
        ],
        "formulasPendingParameters": {
            "poblacionLote": "unidadesVivienda × habitantesPorUnidad",
            "demandaAguaLd": "poblacionDiseno × dotacionLhd",
            "aporteDesagueLd": "demandaAguaLd × factorRetorno + aporteNoDomesticoLd",
        },
        "summary": summary,
        "records": records,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
