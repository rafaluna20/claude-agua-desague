#!/usr/bin/env python3
"""Muestrea perfiles de terreno sobre ejes viales con una grilla TIN .f32.

No impone rasantes ni cotas de solera. Los puntos fuera de la grilla o en
NoData se conservan con estado explícito, por lo que el resultado solo es una
base de perfil topográfico para la fase de diseño.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

from procesar_grid_terreno import TerrainGrid, read_grid


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def length(points: list[list[float]]) -> float:
    return sum(math.hypot(second[0] - first[0], second[1] - first[1]) for first, second in zip(points, points[1:]))


def resample(points: list[list[float]], step: float) -> list[tuple[float, float, float]]:
    if len(points) < 2:
        raise ValueError("Un eje necesita al menos dos coordenadas.")
    segments = [math.hypot(second[0] - first[0], second[1] - first[1]) for first, second in zip(points, points[1:])]
    total = sum(segments)
    stations = [0.0]
    station = step
    while station < total - 1e-9:
        stations.append(station)
        station += step
    if total > 0:
        stations.append(total)
    values = []
    segment_index = 0
    start_station = 0.0
    for station in stations:
        while segment_index < len(segments) - 1 and station > start_station + segments[segment_index] + 1e-9:
            start_station += segments[segment_index]
            segment_index += 1
        first = points[segment_index]
        second = points[segment_index + 1]
        fraction = 0.0 if segments[segment_index] == 0 else (station - start_station) / segments[segment_index]
        values.append((station, first[0] + fraction * (second[0] - first[0]), first[1] + fraction * (second[1] - first[1])))
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axes", required=True, type=Path)
    parser.add_argument("--grid", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--min-x", required=True, type=float)
    parser.add_argument("--min-y", required=True, type=float)
    parser.add_argument("--cell-size", required=True, type=float)
    parser.add_argument("--nx", required=True, type=int)
    parser.add_argument("--ny", required=True, type=int)
    parser.add_argument("--step", default=1.0, type=float)
    args = parser.parse_args()
    if args.cell_size <= 0 or args.nx < 2 or args.ny < 2 or args.step <= 0:
        parser.error("Parámetros de grilla/perfil inválidos.")
    for source in (args.axes, args.grid):
        if not source.is_file():
            parser.error(f"No se encontró: {source}")
    if args.output.exists():
        parser.error(f"La salida ya existe; no se sobrescribe: {args.output}")

    axes_doc = json.loads(args.axes.read_text(encoding="utf-8"))
    grid = TerrainGrid(values=read_grid(args.grid, args.nx, args.ny), min_x=args.min_x, min_y=args.min_y, cell_size=args.cell_size, nx=args.nx, ny=args.ny)
    profiles = []
    total_samples = valid_samples = 0
    for axis in axes_doc["axes"]:
        samples = []
        for station, x, y in resample(axis["coordinates"], args.step):
            elevation, status = grid.sample(x, y)
            total_samples += 1
            if elevation is not None:
                valid_samples += 1
            samples.append({"station": round(station, 3), "x": round(x, 3), "y": round(y, 3), "terrainElevation": None if elevation is None else round(elevation, 3), "status": status})
        valid = [row for row in samples if row["terrainElevation"] is not None]
        endpoint_slope = None
        if len(valid) >= 2 and valid[0]["station"] != valid[-1]["station"]:
            endpoint_slope = round((valid[-1]["terrainElevation"] - valid[0]["terrainElevation"]) / (valid[-1]["station"] - valid[0]["station"]), 6)
        profiles.append({
            "id": axis["id"],
            "source": axis["source"],
            "axisLength": axis["length"],
            "profileStatus": "COMPLETO" if len(valid) == len(samples) else "REVISAR_NODATA",
            "minimumTerrainElevation": None if not valid else min(row["terrainElevation"] for row in valid),
            "maximumTerrainElevation": None if not valid else max(row["terrainElevation"] for row in valid),
            "endpointSlope": endpoint_slope,
            "samples": samples,
        })

    result = {
        "version": "v4_primera_expediente_perfiles_terreno_v1",
        "purpose": "Perfiles de terreno sobre ejes provisionales; no son rasantes, perfiles hidráulicos ni cotas de diseño.",
        "generatedAtUtc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sources": {"axesFile": args.axes.name, "axesSha256": sha256(args.axes), "gridFile": args.grid.name, "gridSha256": sha256(args.grid)},
        "sampling": {"step": args.step, "grid": {"minX": args.min_x, "minY": args.min_y, "maxX": grid.max_x, "maxY": grid.max_y, "cellSize": args.cell_size, "nx": args.nx, "ny": args.ny}, "unitsNote": "Unidades interpretadas provisionalmente como metros por geometría UTM; validar datum vertical y documentación topográfica."},
        "summary": {"profiles": len(profiles), "completeProfiles": sum(profile["profileStatus"] == "COMPLETO" for profile in profiles), "profilesWithNoData": sum(profile["profileStatus"] != "COMPLETO" for profile in profiles), "totalSamples": total_samples, "validSamples": valid_samples, "noDataSamples": total_samples - valid_samples},
        "profiles": profiles,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
