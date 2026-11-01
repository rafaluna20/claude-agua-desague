"""Criba reproducible de corredores de desagüe; NO calcula tuberías ni bateas.

Usa solamente el grafo vial v3, cotas de terreno natural y asignación geométrica
de lotes. La penalidad de contrapendiente es heurística de cribado, no un criterio
hidráulico de OS.070. La variante interna de PTAR no autoriza obras en el predio.
"""

from __future__ import annotations

import hashlib
import heapq
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon


BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "datos" / "v4_primera_expediente"
OUT = BASE / "resultados" / "v1_primera_expediente_desague_criba"
ROOT = "NV-0055"  # Interfaz S1, Calle 30.
WEST = "NV-0058"  # Extremo Calle 31 junto al predio PTAR.
PENALTY = 1000.0  # m de costo por 1 m de ascenso de terreno hacia la salida.
RISE_FLAG = 0.05  # m; solo señal para revisión, no umbral de incumplimiento.


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def route(nodes, edges, elevations, root):
    """Árbol de caminos mínimos con penalidad por ascenso hacia el destino."""
    adjacency = defaultdict(list)
    for edge in edges:
        a, b = edge["fromNode"], edge["toNode"]
        adjacency[a].append((b, edge))
        adjacency[b].append((a, edge))

    distance = {node["id"]: math.inf for node in nodes}
    parent = {}
    distance[root] = 0.0
    queue = [(0.0, root)]
    while queue:
        cost, downstream = heapq.heappop(queue)
        if cost != distance[downstream]:
            continue
        for upstream, edge in adjacency[downstream]:
            rise = max(0.0, elevations[downstream] - elevations[upstream])
            candidate = cost + edge["length"] + PENALTY * rise
            if candidate < distance[upstream] - 1e-9:
                distance[upstream] = candidate
                parent[upstream] = {"downstream": downstream, "edge": edge["id"]}
                heapq.heappush(queue, (candidate, upstream))

    if len(parent) != len(nodes) - 1:
        raise ValueError("El grafo no conecta todos sus nodos con Calle 30")
    return parent


def summarize(parent, edges, elevations, lots_per_edge):
    edge_by_id = {edge["id"]: edge for edge in edges}
    chosen = {entry["edge"] for entry in parent.values()}
    adverse = []
    for upstream, entry in parent.items():
        downstream = entry["downstream"]
        rise = round(elevations[downstream] - elevations[upstream], 3)
        if rise > RISE_FLAG:
            edge = edge_by_id[entry["edge"]]
            adverse.append(
                {
                    "edge": edge["id"],
                    "via": edge.get("source", {}).get("codigo", edge["origin"]),
                    "upstream": upstream,
                    "downstream": downstream,
                    "terrainRiseTowardOutletM": rise,
                    "lengthM": edge["length"],
                    "assignedLots": lots_per_edge[edge["id"]],
                }
            )
    adverse.sort(key=lambda item: item["terrainRiseTowardOutletM"], reverse=True)
    missed = [
        {
            "edge": edge["id"],
            "via": edge.get("source", {}).get("codigo", edge["origin"]),
            "assignedLots": lots_per_edge[edge["id"]],
            "lengthM": edge["length"],
        }
        for edge in edges
        if edge["id"] not in chosen and lots_per_edge[edge["id"]] > 0
    ]
    missed.sort(key=lambda item: item["edge"])
    return {
        "selectedEdges": len(chosen),
        "treeRoadLengthM": round(
            sum(edge["length"] for edge in edges if edge["id"] in chosen), 3
        ),
        "adverseTerrainEdges": adverse,
        "adverseTerrainEdgeCount": len(adverse),
        "maximumAdverseTerrainRiseM": adverse[0]["terrainRiseTowardOutletM"] if adverse else 0,
        "lotBearingEdgesOutsideTree": missed,
        "assignedLotsOnEdgesOutsideTree": sum(item["assignedLots"] for item in missed),
    }


def make_geojson(edges, base_parent, virtual_parent, lots_per_edge, elevations):
    base = {entry["edge"]: upstream for upstream, entry in base_parent.items()}
    virtual = {entry["edge"]: upstream for upstream, entry in virtual_parent.items()}
    features = []
    for edge in edges:
        edge_id = edge["id"]
        upstream = base.get(edge_id)
        rise = None
        if upstream is not None:
            downstream = base_parent[upstream]["downstream"]
            rise = round(elevations[downstream] - elevations[upstream], 3)
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": edge["coordinates"]},
                "properties": {
                    "id": edge_id,
                    "via": edge.get("source", {}).get("codigo", edge["origin"]),
                    "origin": edge["origin"],
                    "lengthM": edge["length"],
                    "assignedLots": lots_per_edge[edge_id],
                    "inBaseTree": edge_id in base,
                    "inConditionalPTARTree": edge_id in virtual,
                    "baseTerrainRiseTowardOutletM": rise,
                    "status": (
                        "HIPOTESIS_INTERNA_PTAR"
                        if edge_id == "VX-PTAR-01"
                        else "CONTRAPENDIENTE_TERRENO_REVISAR"
                        if rise is not None and rise > RISE_FLAG
                        else "LOTE_FUERA_ARBOL_REVISAR"
                        if edge_id not in base and lots_per_edge[edge_id]
                        else "CORREDOR_ARBOL_PRELIMINAR"
                        if edge_id in base
                        else "VIA_NO_SELECCIONADA"
                    ),
                },
            }
        )
    return {"type": "FeatureCollection", "features": features}


def draw_map(parcels, edges, node_by_id, base_summary, base_parent, virtual_edge):
    chosen = {entry["edge"] for entry in base_parent.values()}
    critical = {item["edge"] for item in base_summary["adverseTerrainEdges"]}
    missed = {item["edge"] for item in base_summary["lotBearingEdgesOutsideTree"]}
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.subplots_adjust(left=0.10, right=0.98, top=0.91, bottom=0.13)
    for polygon in parcels.values():
        ax.add_patch(Polygon(polygon, closed=True, facecolor="#f0f0ed", edgecolor="#d4d4cf", linewidth=0.22))
    for edge in edges:
        if edge["id"] == virtual_edge["id"]:
            continue
        x, y = zip(*edge["coordinates"])
        ax.plot(x, y, color="#c1c5c9", linewidth=0.8, zorder=2)
    for edge in edges:
        edge_id = edge["id"]
        if edge_id == virtual_edge["id"]:
            continue
        x, y = zip(*edge["coordinates"])
        if edge_id in chosen:
            ax.plot(x, y, color="#c62828" if edge_id in critical else "#136f9a", linewidth=3.0 if edge_id in critical else 1.8, zorder=4)
        elif edge_id in missed:
            ax.plot(x, y, color="#eb8c24", linewidth=2.4, linestyle="--", zorder=5)
    x, y = zip(*virtual_edge["coordinates"])
    ax.plot(x, y, color="#8524a8", linestyle=(0, (4, 2)), linewidth=2.8, zorder=6)
    px, py = node_by_id[ROOT]["coordinate"]
    wx, wy = node_by_id[WEST]["coordinate"]
    ax.scatter([px], [py], marker="*", s=230, color="#0e526e", zorder=8)
    ax.scatter([wx], [wy], marker="o", s=70, color="#8524a8", zorder=8)
    ax.annotate("S1 Calle 30", (px, py), (px - 90, py + 38), fontsize=9, arrowprops={"arrowstyle": "->", "color": "#334"})
    ax.annotate("Calle 31: +7.03 m\nsi se fuerza hacia el oeste", (wx, wy), (wx - 180, wy - 50), fontsize=9, color="#a32121", arrowprops={"arrowstyle": "->", "color": "#a32121"})
    ax.set_xlim(308275, 308885)
    ax.set_ylim(8622650, 8623015)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Este (coordenadas del DWG; referencia UTM por formalizar)")
    ax.set_ylabel("Norte")
    ax.set_title("Terra Lima · Primera Expediente · criba de corredores de desagüe hacia Calle 30")
    ax.grid(alpha=0.15)
    ax.legend(
        handles=[
            Line2D([0], [0], color="#136f9a", lw=2, label="Árbol vial preliminar (no tuberías)"),
            Line2D([0], [0], color="#c62828", lw=3, label="Ascenso de terreno hacia S1: revisar"),
            Line2D([0], [0], color="#eb8c24", lw=2, ls="--", label="Vía con lotes fuera del árbol"),
            Line2D([0], [0], color="#8524a8", lw=2, ls="--", label="Enlace PTAR hipotético; no aprobado"),
        ],
        loc="upper right",
        fontsize=8,
    )
    fig.text(0.5, 0.025, "NO ES DISEÑO HIDRÁULICO NI PLANO CONSTRUCTIVO · cotas de terreno, sin bateas/caudales", ha="center", fontsize=10, color="#9b2424", weight="bold")
    fig.savefig(OUT / "PL-D01_criba_corredores_calle30_v1.png", dpi=170)
    plt.close(fig)


def draw_terrain_profiles(profiles):
    codes = ["CALLE31", "PASAJE03"]
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), constrained_layout=True)
    for ax, code in zip(axes, codes):
        profile = next(item for item in profiles if item["source"]["codigo"] == code)
        samples = profile["samples"]
        xs = [sample["station"] for sample in samples]
        ys = [sample["terrainElevation"] for sample in samples]
        ax.plot(xs, ys, color="#136f9a", linewidth=2)
        ax.fill_between(xs, ys, min(ys) - 1, color="#dcebf0", alpha=0.55)
        ax.set_xlim(0, max(xs))
        ax.set_ylim(min(ys) - 0.6, max(ys) + 1.0)
        ax.set_ylabel("Cota de terreno (m)")
        ax.grid(alpha=0.25)
        ax.set_title(f"{code} · perfil de terreno natural; NO es batea de tubería", loc="left", fontsize=11)
        ax.set_xlabel("Progresiva del eje preliminar (m)")
        if code == "CALLE31":
            ax.annotate("S3 oeste PTAR\n79.347 m", (0, ys[0]), (8, ys[0] + 2.0),
                        arrowprops={"arrowstyle": "->", "color": "#9b2424"}, color="#9b2424")
            ax.annotate("Árbol hacia S1 fuerza drenaje en sentido ascendente del terreno\n18 lotes en TV-0043; +7.025 m entre extremos",
                        (90, ys[min(range(len(xs)), key=lambda i: abs(xs[i] - 90))]),
                        (52, max(ys) - 1.0),
                        arrowprops={"arrowstyle": "->", "color": "#9b2424"},
                        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8},
                        color="#9b2424", fontsize=9)
        else:
            ax.annotate("Árbol hacia S1 invierte la caída natural\n8 lotes; +1.947 m entre extremos",
                        (xs[-1], ys[-1]), (3, max(ys) + 0.3),
                        arrowprops={"arrowstyle": "->", "color": "#9b2424"}, color="#9b2424", fontsize=9)
    fig.suptitle("Terra Lima · perfiles críticos para definir alternativas de desagüe", fontsize=14)
    fig.savefig(OUT / "PF-D01_perfiles_terreno_criticos_v1.png", dpi=170)
    plt.close(fig)


def main():
    graph_file = DATA / "vias" / "grafo_vial_primera_expediente_v3.json"
    topo_file = DATA / "topografia" / "grafo_vial_cotas_terreno_v1.json"
    assignment_file = DATA / "vias" / "asignacion_lotes_grafo_v1.json"
    parcels_file = DATA / "parcels_primera_expediente.json"
    interface_file = DATA / "vias" / "interfaces_referenciales_v1.json"
    profiles_file = DATA / "topografia" / "perfiles_ejes_terreno_v1.json"
    graph = read_json(graph_file)
    topo = read_json(topo_file)
    assignment = read_json(assignment_file)
    parcels = read_json(parcels_file)
    interfaces = read_json(interface_file)
    profiles = read_json(profiles_file)

    node_by_id = {node["id"]: node for node in graph["nodes"]}
    elevations = {node["id"]: node["cotaTerreno"] for node in topo["nodes"]}
    if len(node_by_id) != 82 or len(graph["edges"]) != 91:
        raise ValueError("Cambió el grafo vial: revisar identificadores y método")
    s1 = next(
        item
        for ref in interfaces["references"]
        for item in ref["alternativasGeometricas"]
        if item["via"] == "CALLE30"
    )
    if math.dist(node_by_id[ROOT]["coordinate"], s1["puntoEjeProvisional"]) > 0.01:
        raise ValueError("La interfaz Calle 30 ya no coincide con NV-0055")

    lots_per_edge = Counter(record["tramoVial"] for record in assignment["records"] if record.get("tramoVial"))
    missing_front = [record["codigo"] for record in assignment["records"] if not record.get("tramoVial")]
    base_parent = route(graph["nodes"], graph["edges"], elevations, ROOT)
    base_summary = summarize(base_parent, graph["edges"], elevations, lots_per_edge)

    west_point = node_by_id[WEST]["coordinate"]
    root_point = node_by_id[ROOT]["coordinate"]
    virtual_edge = {
        "id": "VX-PTAR-01",
        "fromNode": WEST,
        "toNode": ROOT,
        "length": round(math.dist(west_point, root_point), 3),
        "origin": "HIPOTESIS_INTERNA_PTAR",
        "coordinates": [west_point, root_point],
    }
    virtual_edges = [*graph["edges"], virtual_edge]
    virtual_parent = route(graph["nodes"], virtual_edges, elevations, ROOT)
    virtual_summary = summarize(virtual_parent, virtual_edges, elevations, lots_per_edge)
    if "VX-PTAR-01" not in {entry["edge"] for entry in virtual_parent.values()}:
        raise ValueError("El enlace hipotético no se usó; revisar criba")

    result = {
        "version": "v1_primera_expediente_desague_criba",
        "status": "CORREDORES_PRELIMINARES_NO_DISENO_HIDRAULICO",
        "purpose": "Criba topológica y de terreno para orientar perfiles; no define tuberías, caudales, buzones, cotas de batea ni bombeo.",
        "sources": {path.name: sha256(path) for path in [graph_file, topo_file, assignment_file, parcels_file, interface_file, profiles_file]},
        "method": {
            "root": ROOT,
            "rootCoordinate": root_point,
            "terrainSource": "TIN Civil 3D muestreada a 1 m; cota de terreno natural",
            "edgeCost": "longitud vial m + 1000 * max(0, cota_terreno_nodo_destino - cota_terreno_nodo_origen) m",
            "edgeCostNote": "Penalidad arbitraria para comparar corredores; no equivale a pendiente de tubería ni reemplaza OS.070.",
            "terrainRiseFlagM": RISE_FLAG,
            "connections": "33 conectores del grafo inferidos por continuidad vial, pendientes de validación",
        },
        "coverage": {
            "lotsInScope": len(assignment["records"]),
            "lotsAssignedToRoadEdge": sum(bool(record.get("tramoVial")) for record in assignment["records"]),
            "lotsWithoutRoadEdge": missing_front,
            "ptarLotIncludedInGeometricAssignments": "E03MZD049P",
            "populationOrFlowAssigned": False,
        },
        "baseSingleInterfaceCalle30": base_summary,
        "conditionalInternalPTARLink": {
            "description": "Conector geométrico oeste Calle 31 a Calle 30 dentro del predio PTAR; requiere expediente PTAR, servidumbre interna y cota de entrada. No es tubería aprobada.",
            "edge": virtual_edge,
            "summary": virtual_summary,
        },
        "baseParentByUpstreamNode": base_parent,
        "conditionalParentByUpstreamNode": virtual_parent,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "desague_corredores_calle30_v1.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "desague_corredores_calle30_v1.geojson").write_text(
        json.dumps(
            make_geojson(virtual_edges, base_parent, virtual_parent, lots_per_edge, elevations),
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    draw_map(parcels, virtual_edges, node_by_id, base_summary, base_parent, virtual_edge)
    draw_terrain_profiles(profiles["profiles"])
    print(json.dumps({"output": str(OUT), "base": base_summary, "conditional": virtual_summary}, ensure_ascii=False))


if __name__ == "__main__":
    main()
