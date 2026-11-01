#!/usr/bin/env python3
"""Convierte una grilla .f32 de Civil 3D en cotas trazables por lote.

Entrada esperada
---------------
El archivo proviene exclusivamente de `civil3d_sample_surface_grid`:
- float32 little-endian;
- filas de norte a sur y columnas de oeste a este;
- valor -9999 para nodos fuera de la TIN.

No calcula rasantes, redes ni modifica un DWG. Es el adaptador reproducible entre
la superficie TIN de Civil 3D y los cálculos sanitarios posteriores.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import struct
import sys
from pathlib import Path
from typing import Iterable


NO_DATA = -9999.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def polygon_centroid(vertices: list[list[float]]) -> tuple[float, float]:
    """Centroide por fórmula de área; usa promedio si la geometría es degenerada."""
    if len(vertices) < 3:
        raise ValueError("Un lote requiere al menos tres vértices.")
    # Trasladar el polígono evita cancelación numérica con coordenadas UTM
    # de millones de unidades y lotes de algunas centenas de m².
    origin_x, origin_y = vertices[0]
    local_vertices = [[point[0] - origin_x, point[1] - origin_y] for point in vertices]
    twice_area = 0.0
    cx = 0.0
    cy = 0.0
    pairs: Iterable[tuple[list[float], list[float]]] = zip(
        local_vertices, local_vertices[1:] + local_vertices[:1]
    )
    for first, second in pairs:
        cross = first[0] * second[1] - second[0] * first[1]
        twice_area += cross
        cx += (first[0] + second[0]) * cross
        cy += (first[1] + second[1]) * cross
    if abs(twice_area) < 1e-9:
        return (
            sum(point[0] for point in vertices) / len(vertices),
            sum(point[1] for point in vertices) / len(vertices),
        )
    return (
        origin_x + cx / (3.0 * twice_area),
        origin_y + cy / (3.0 * twice_area),
    )


class TerrainGrid:
    def __init__(self, *, values: tuple[float, ...], min_x: float, min_y: float,
                 cell_size: float, nx: int, ny: int) -> None:
        self.values = values
        self.min_x = min_x
        self.min_y = min_y
        self.cell_size = cell_size
        self.nx = nx
        self.ny = ny
        self.max_x = min_x + (nx - 1) * cell_size
        self.max_y = min_y + (ny - 1) * cell_size

    def value(self, row: int, col: int) -> float:
        return self.values[row * self.nx + col]

    def sample(self, x: float, y: float) -> tuple[float | None, str]:
        """Interpolación bilineal; si un nodo es NoData no inventa una cota."""
        col_float = (x - self.min_x) / self.cell_size
        row_float = (self.max_y - y) / self.cell_size
        tolerance = 1e-8
        if col_float < -tolerance or row_float < -tolerance or col_float > self.nx - 1 + tolerance or row_float > self.ny - 1 + tolerance:
            return None, "FUERA_GRILLA"

        col_float = min(max(col_float, 0.0), self.nx - 1.0)
        row_float = min(max(row_float, 0.0), self.ny - 1.0)
        col0 = min(max(math.floor(col_float), 0), self.nx - 2)
        row0 = min(max(math.floor(row_float), 0), self.ny - 2)
        dx = col_float - col0
        dy = row_float - row0
        samples = (
            self.value(row0, col0),
            self.value(row0, col0 + 1),
            self.value(row0 + 1, col0),
            self.value(row0 + 1, col0 + 1),
        )
        if any(value == NO_DATA for value in samples):
            return None, "NODATA_TIN"
        south_weight = dy
        z = (
            samples[0] * (1.0 - dx) * (1.0 - south_weight)
            + samples[1] * dx * (1.0 - south_weight)
            + samples[2] * (1.0 - dx) * south_weight
            + samples[3] * dx * south_weight
        )
        return z, "BILINEAL_F32_TIN"


def read_grid(path: Path, nx: int, ny: int) -> tuple[float, ...]:
    expected_values = nx * ny
    raw = path.read_bytes()
    expected_bytes = expected_values * 4
    if len(raw) != expected_bytes:
        raise ValueError(
            f"Tamaño inesperado para la grilla: {len(raw)} bytes; "
            f"se esperaban {expected_bytes} (= {nx} x {ny} x 4)."
        )
    return struct.unpack(f"<{expected_values}f", raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid", required=True, type=Path, help="Archivo .f32 generado por Civil 3D")
    parser.add_argument("--parcels", required=True, type=Path, help="parcels_primera_expediente.json")
    parser.add_argument("--output", required=True, type=Path, help="JSON de cotas por lote a crear")
    parser.add_argument("--min-x", required=True, type=float)
    parser.add_argument("--min-y", required=True, type=float)
    parser.add_argument("--cell-size", required=True, type=float)
    parser.add_argument("--nx", required=True, type=int)
    parser.add_argument("--ny", required=True, type=int)
    parser.add_argument("--surface-name", default="terreno natural")
    parser.add_argument("--coordinate-reference", default="WGS84; zona UTM y datum vertical por documentar")
    args = parser.parse_args()

    if args.cell_size <= 0 or args.nx < 2 or args.ny < 2:
        parser.error("cell-size debe ser positivo y nx/ny deben ser al menos 2.")
    if not args.grid.is_file() or not args.parcels.is_file():
        parser.error("No se encontró la grilla o el archivo de lotes indicado.")

    parcels = json.loads(args.parcels.read_text(encoding="utf-8"))
    if not isinstance(parcels, dict):
        raise ValueError("El JSON de lotes debe ser un objeto {codigo: vertices}.")

    grid = TerrainGrid(
        values=read_grid(args.grid, args.nx, args.ny),
        min_x=args.min_x,
        min_y=args.min_y,
        cell_size=args.cell_size,
        nx=args.nx,
        ny=args.ny,
    )
    records = []
    for code in sorted(parcels):
        x, y = polygon_centroid(parcels[code])
        elevation, status = grid.sample(x, y)
        records.append(
            {
                "codigo": code,
                "centroide": [round(x, 3), round(y, 3)],
                "cota_terreno": None if elevation is None else round(elevation, 3),
                "metodo": status,
            }
        )

    valid = [record["cota_terreno"] for record in records if record["cota_terreno"] is not None]
    result = {
        "purpose": "Cotas preliminares de terreno por centroide de lote; no sustituye cotas de estructuras ni perfiles de eje.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "source": {
            "surfaceName": args.surface_name,
            "gridFile": args.grid.name,
            "gridSha256": sha256(args.grid),
            "orientation": "Filas norte-sur; columnas oeste-este; float32 little-endian; -9999 = fuera de TIN.",
            "coordinateReference": args.coordinate_reference,
            "grid": {
                "minX": args.min_x,
                "minY": args.min_y,
                "maxX": grid.max_x,
                "maxY": grid.max_y,
                "cellSize": args.cell_size,
                "nx": args.nx,
                "ny": args.ny,
                "unitsNote": "La grilla se generó asumiendo que una unidad del DWG equivale a un metro; confirmar en documentación topográfica.",
            },
        },
        "quality": {
            "totalParcels": len(records),
            "sampled": len(valid),
            "withoutElevation": len(records) - len(valid),
            "minimumElevation": None if not valid else min(valid),
            "maximumElevation": None if not valid else max(valid),
        },
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["quality"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(2)
