#!/usr/bin/env python3
"""Registra una condición de borde preliminar de agua desde una TIN exportada.

Las cotas obtenidas son de terreno natural. No sustituyen la cota del eje de
tubería, el nivel hidráulico del reservorio ni una prueba presión-caudal.
"""

import argparse
import hashlib
import json
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
    parser.add_argument("--grid", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--meter-x", required=True, type=float)
    parser.add_argument("--meter-y", required=True, type=float)
    parser.add_argument("--reservoir-x", required=True, type=float)
    parser.add_argument("--reservoir-y", required=True, type=float)
    parser.add_argument("--pressure-mca", required=True, type=float)
    parser.add_argument("--pipe-diameter-inch", required=True, type=float)
    parser.add_argument("--min-x", required=True, type=float)
    parser.add_argument("--min-y", required=True, type=float)
    parser.add_argument("--cell-size", required=True, type=float)
    parser.add_argument("--nx", required=True, type=int)
    parser.add_argument("--ny", required=True, type=int)
    args = parser.parse_args()

    grid_path = Path(args.grid)
    output_path = Path(args.output)
    if output_path.exists():
        raise SystemExit(f"La salida ya existe: {output_path}")
    grid = TerrainGrid(
        values=read_grid(grid_path, args.nx, args.ny),
        min_x=args.min_x, min_y=args.min_y, cell_size=args.cell_size, nx=args.nx, ny=args.ny,
    )
    meter_z, meter_method = grid.sample(args.meter_x, args.meter_y)
    reservoir_z, reservoir_method = grid.sample(args.reservoir_x, args.reservoir_y)
    if meter_z is None or reservoir_z is None:
        raise ValueError("Uno o ambos puntos no tienen cota válida en la grilla TIN.")
    dx = args.reservoir_x - args.meter_x
    dy = args.reservoir_y - args.meter_y
    plan_distance = (dx * dx + dy * dy) ** 0.5
    terrain_rise = reservoir_z - meter_z
    result = {
        "version": "v4_primera_expediente_condicion_borde_santa_maria_v1",
        "purpose": "Condición de borde preliminar de la fuente Santa María para el modelo de agua; no reemplaza factibilidad ni pruebas de campo.",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": {
            "gridFile": grid_path.name,
            "gridSha256": sha256(grid_path),
            "surface": "terreno natural de Civil 3D, grilla 1 m, interpolación bilineal",
            "unitsNote": "Unidades interpretadas provisionalmente como metros; datum vertical pendiente de documento formal.",
        },
        "meterGeneralSantaMaria": {
            "coordinate": [args.meter_x, args.meter_y],
            "terrainElevation": round(meter_z, 3),
            "terrainMethod": meter_method,
            "existingPipeDiameterInch": args.pipe_diameter_inch,
            "declaredPressureMca": args.pressure_mca,
            "pressureStatus": "DECLARADA_POR_USUARIO; confirmar estática, residual, hora y caudal de ensayo",
        },
        "reservoirProject": {
            "coordinate": [args.reservoir_x, args.reservoir_y],
            "terrainElevation": round(reservoir_z, 3),
            "terrainMethod": reservoir_method,
            "waterLevelElevation": None,
            "status": "UBICACION_CONFIRMADA_POR_USUARIO; pendiente nivel de agua, capacidad y tipología",
        },
        "geometry": {
            "deltaX": round(dx, 3),
            "deltaY": round(dy, 3),
            "planDistance": round(plan_distance, 3),
            "terrainRiseReservoirMinusMeter": round(terrain_rise, 3),
            "terrainReferenceMarginMca": round(args.pressure_mca - terrain_rise, 3),
        },
        "engineeringInterpretation": [
            "El margen de terreno es presión declarada menos desnivel de terreno; no equivale a presión residual garantizada en el reservorio.",
            "Para confirmar llenado por presión directa se requiere cota del eje de tubería en el medidor, nivel máximo de agua del reservorio, material/diámetro interior, accesorios, caudal de llenado y prueba presión-caudal.",
            "La distancia en planta se calculó entre las coordenadas confirmadas; la longitud real de tubería dependerá del trazado autorizado.",
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["geometry"], ensure_ascii=False))


if __name__ == "__main__":
    main()
