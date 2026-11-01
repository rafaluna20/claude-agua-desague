#!/usr/bin/env python3
"""Exporta un plano PNG de control del prediseño sanitario de Primera Expediente.

El dibujo visualiza la base geométrica, no tuberías, diámetros, buzones ni
caudales definitivos. Está pensado para revisión interna del trazado base.
"""

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Patch, Polygon as MplPolygon


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def polygon_patch(coords, **kwargs):
    return MplPolygon(coords, closed=True, **kwargs)


def add_scale_bar(ax, min_x, min_y, width):
    preferred = [25, 50, 100, 200]
    length = max(value for value in preferred if value <= width * 0.24)
    x0 = min_x + width * 0.055
    y0 = min_y + width * 0.018
    ax.plot([x0, x0 + length], [y0, y0], color="#202830", lw=3, solid_capstyle="butt", zorder=20)
    ax.plot([x0, x0], [y0 - 2, y0 + 2], color="#202830", lw=1, zorder=20)
    ax.plot([x0 + length, x0 + length], [y0 - 2, y0 + 2], color="#202830", lw=1, zorder=20)
    ax.text(x0 + length / 2, y0 + 5, f"{length} m", ha="center", va="bottom", fontsize=8, color="#202830", zorder=20)


def add_north_arrow(ax, min_x, min_y, width, height):
    x = min_x + width * 0.93
    y = min_y + height * 0.12
    arrow = FancyArrowPatch((x, y), (x, y + height * 0.12), arrowstyle="simple", mutation_scale=18,
                            color="#202830", zorder=20)
    ax.add_patch(arrow)
    ax.text(x, y + height * 0.135, "N", ha="center", va="bottom", fontsize=10, weight="bold", color="#202830", zorder=20)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parcels", required=True)
    parser.add_argument("--roads", required=True)
    parser.add_argument("--boundary", required=True)
    parser.add_argument("--program", required=True)
    parser.add_argument("--graph", required=True)
    parser.add_argument("--interfaces", required=True)
    parser.add_argument("--water-condition", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    paths = {name: Path(getattr(args, name)) for name in (
        "parcels", "roads", "boundary", "program", "graph", "interfaces", "water_condition", "output", "manifest"
    )}
    if paths["output"].exists() or paths["manifest"].exists():
        raise SystemExit("La salida PNG o su manifiesto ya existe; use un nombre de versión nuevo.")

    parcels = json.loads(paths["parcels"].read_text(encoding="utf-8-sig"))
    roads = json.loads(paths["roads"].read_text(encoding="utf-8-sig"))
    boundary = json.loads(paths["boundary"].read_text(encoding="utf-8-sig"))["coordinates"]
    program = json.loads(paths["program"].read_text(encoding="utf-8-sig"))
    graph = json.loads(paths["graph"].read_text(encoding="utf-8-sig"))
    interfaces = json.loads(paths["interfaces"].read_text(encoding="utf-8-sig"))
    water_condition = json.loads(paths["water_condition"].read_text(encoding="utf-8-sig"))
    by_code = {item["codigo"]: item for item in program["records"]}

    fig = plt.figure(figsize=(16, 13), dpi=200, facecolor="white")
    ax = fig.add_axes((0.055, 0.135, 0.91, 0.79))
    ax.set_facecolor("#eef2f3")

    # Lotes base y categorías singulares.
    for code, coordinates in parcels.items():
        info = by_code[code]
        category = info["categoriaPrograma"]
        style = {"facecolor": "#fbfcfd", "edgecolor": "#a9b1b5", "linewidth": 0.28, "zorder": 2}
        if info["estadoAccesoRed"] == "PENDIENTE_SERVIDUMBRE":
            style.update({"facecolor": "#ffd36e", "edgecolor": "#a85d00", "linewidth": 0.8, "hatch": "///", "zorder": 4})
        elif category == "MULTIFAMILIAR_CONDICIONAL":
            style.update({"facecolor": "#d7c4f0", "edgecolor": "#6950a1", "linewidth": 0.8, "zorder": 4})
        elif category == "MULTIFAMILIAR_CONDICIONAL_USO_PENDIENTE":
            style.update({"facecolor": "#bcdcf4", "edgecolor": "#1573ae", "linewidth": 0.9, "zorder": 4})
        elif category == "INFRAESTRUCTURA_PTAR_EXCLUIDA_DE_DEMANDA_RESIDENCIAL":
            style.update({"facecolor": "#f5b7b1", "edgecolor": "#ba2a1f", "linewidth": 1.0, "zorder": 5})
        ax.add_patch(polygon_patch(coordinates, **style))

    # Polígonos viales sobre la base de lotes.
    for collection, color in ((roads["streets"], "#cfd5d8"), (roads["passages"], "#e5d8af")):
        for feature in collection.values():
            ax.add_patch(polygon_patch(feature["coordinates"], facecolor=color, edgecolor="none", alpha=0.9, zorder=3))

    # Corredores de red geométricos: ejes y enlaces inferidos.
    for edge in graph["edges"]:
        xs = [point[0] for point in edge["coordinates"]]
        ys = [point[1] for point in edge["coordinates"]]
        if edge["origin"] == "EJE_VIAL":
            ax.plot(xs, ys, color="#008c95", lw=1.15, alpha=0.95, zorder=7)
        else:
            ax.plot(xs, ys, color="#008c95", lw=0.9, alpha=0.9, linestyle=(0, (3, 2)), zorder=7)

    # Límite de alcance.
    bx = [point[0] for point in boundary] + [boundary[0][0]]
    by = [point[1] for point in boundary] + [boundary[0][1]]
    ax.plot(bx, by, color="#17212b", lw=1.4, zorder=10)

    # Alternativas de interfaz; se dibujan todas para no elegir una sin campo.
    label_offsets = {
        "E01MZD155P": (10, 12, "Santa María\n(predio de referencia)"),
        "E03MZD049P": (10, -22, "PTAR\n(predio de referencia)"),
    }
    for reference in interfaces["references"]:
        is_water = reference["predioReferencia"] == "E01MZD155P"
        if is_water:
            continue
        color = "#0868ac" if is_water else "#c03221"
        marker = "^" if is_water else "*"
        for item in reference["alternativasGeometricas"]:
            x, y = item["puntoEjeProvisional"]
            ax.plot(x, y, marker=marker, color=color, markeredgecolor="white", markeredgewidth=0.55,
                    markersize=7 if is_water else 9, linestyle="None", zorder=15)
        cx, cy = reference["centroidePredio"]
        dx, dy, text = label_offsets[reference["predioReferencia"]]
        ax.annotate(text, (cx, cy), xytext=(dx, dy), textcoords="offset points", fontsize=8.2,
                    color=color, weight="bold", bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": color, "alpha": 0.92}, zorder=18)

    # Medidor y reservorio definidos por el usuario. La recta es referencia
    # geométrica; no adopta el trazado de aducción ni la condición hidráulica.
    meter_x, meter_y = water_condition["meterGeneralSantaMaria"]["coordinate"]
    reservoir_x, reservoir_y = water_condition["reservoirProject"]["coordinate"]
    ax.plot([meter_x, reservoir_x], [meter_y, reservoir_y], color="#0868ac", lw=1.15,
            linestyle=(0, (6, 3)), alpha=0.9, zorder=12)
    ax.plot(meter_x, meter_y, marker="o", color="#0868ac", markeredgecolor="white", markeredgewidth=0.7,
            markersize=7.5, linestyle="None", zorder=16)
    ax.plot(reservoir_x, reservoir_y, marker="s", color="#053b70", markeredgecolor="white", markeredgewidth=0.7,
            markersize=7.5, linestyle="None", zorder=16)
    ax.annotate("Medidor general\nSanta María", (meter_x, meter_y), xytext=(9, 10), textcoords="offset points",
                fontsize=8.1, color="#0868ac", weight="bold",
                bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#0868ac", "alpha": 0.92}, zorder=18)
    ax.annotate("Reservorio\nproyectado", (reservoir_x, reservoir_y), xytext=(-10, 12), textcoords="offset points",
                ha="right", fontsize=8.1, color="#053b70", weight="bold",
                bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#053b70", "alpha": 0.92}, zorder=18)

    all_x = [point[0] for points in parcels.values() for point in points]
    all_y = [point[1] for points in parcels.values() for point in points]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    width, height = max_x - min_x, max_y - min_y
    margin_x, margin_y = width * 0.045, height * 0.10
    ax.set_xlim(min_x - margin_x, max_x + margin_x)
    ax.set_ylim(min_y - margin_y, max_y + margin_y)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)
        spine.set_color("#56616b")
    add_scale_bar(ax, min_x - margin_x, min_y - margin_y, width + 2 * margin_x)
    add_north_arrow(ax, min_x - margin_x, min_y - margin_y, width + 2 * margin_x, height + 2 * margin_y)

    fig.text(0.055, 0.962, "PL-00 · ESQUEMA BASE DE AGUA Y ALCANTARILLADO", fontsize=16, weight="bold", color="#17212b")
    fig.text(0.055, 0.938, "Terra Lima · Primera Expediente · control geométrico preliminar · 10 oct 2026", fontsize=9.5, color="#4f5d67")
    fig.text(0.055, 0.037,
             "NOTA: líneas turquesa = corredores viales candidatos para red; no representan tuberías, diámetros, buzones ni perfiles aprobados. "
             "La línea azul es referencia geométrica entre medidor y reservorio, no trazado de aducción. Las marcas rojas de PTAR son alternativas hasta validar campo.",
             fontsize=7.6, color="#394650")

    legend_items = [
        Patch(facecolor="#fbfcfd", edgecolor="#a9b1b5", label="Lote ordinario (paramétrico)"),
        Patch(facecolor="#d7c4f0", edgecolor="#6950a1", label="Multifamiliar condicional"),
        Patch(facecolor="#bcdcf4", edgecolor="#1573ae", label="Predio referencia Santa María"),
        Patch(facecolor="#f5b7b1", edgecolor="#ba2a1f", label="Predio PTAR"),
        Patch(facecolor="#ffd36e", edgecolor="#a85d00", hatch="///", label="Pendiente servidumbre"),
        Patch(facecolor="#cfd5d8", edgecolor="none", label="Calles"),
        Patch(facecolor="#e5d8af", edgecolor="none", label="Pasajes inferidos"),
        Line2D([0], [0], color="#008c95", lw=1.4, label="Eje vial / corredor candidato"),
        Line2D([0], [0], color="#008c95", lw=1, linestyle=(0, (3, 2)), label="Enlace vial inferido"),
        Line2D([0], [0], marker="o", color="#0868ac", markersize=7, linestyle="None", label="Medidor Santa María"),
        Line2D([0], [0], marker="s", color="#053b70", markersize=7, linestyle="None", label="Reservorio proyectado"),
        Line2D([0], [0], color="#0868ac", lw=1.1, linestyle=(0, (6, 3)), label="Referencia medidor–reservorio"),
        Line2D([0], [0], marker="*", color="#c03221", markersize=9, linestyle="None", label="Alternativas llegada PTAR"),
    ]
    fig.legend(handles=legend_items, loc="lower center", bbox_to_anchor=(0.51, 0.06), ncol=4,
               frameon=False, fontsize=7.4, handlelength=2.2, columnspacing=1.5)

    paths["output"].parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(paths["output"], dpi=200, facecolor=fig.get_facecolor())
    plt.close(fig)
    manifest = {
        "version": "PL-00_esquema_base_agua_desague_v1",
        "purpose": "Plano PNG de control geométrico preliminar; no es plano de red final.",
        "generatedAtUtc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "outputFile": paths["output"].name,
        "outputSha256": sha256(paths["output"]),
        "sources": {name: {"file": path.name, "sha256": sha256(path)} for name, path in paths.items()
                    if name not in {"output", "manifest"}},
        "limitations": [
            "No se ha definido población, caudales, diámetros, buzones ni perfiles hidráulicos.",
            "La interfaz física de Santa María y la cota/punto de llegada a PTAR siguen pendientes.",
            "Los enlaces discontinuos y pasajes son inferencias geométricas de trabajo.",
        ],
    }
    paths["manifest"].parent.mkdir(parents=True, exist_ok=True)
    paths["manifest"].write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"png": str(paths["output"]), "sha256": manifest["outputSha256"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
