# -*- coding: utf-8 -*-
"""Dibuja una vista previa (PNG) del DXF de una corrida leyendo sus entidades y capas, sin AutoCAD.
Uso: python vista_previa_dxf.py <corrida> [x0 x1 y0 y1 nombre]   (sin ventana: vista general + zonas predefinidas)"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ACI = {1: "#d62728", 2: "#c9a000", 3: "#2ca02c", 4: "#17becf", 5: "#1f3fd0", 6: "#c000c0", 7: "#222222", 8: "#888888"}


def leer_dxf(path):
    pares = []
    with open(path, encoding="ascii", errors="replace") as f:
        lin = [l.rstrip("\n").rstrip("\r") for l in f]
    for i in range(0, len(lin) - 1, 2):
        pares.append((lin[i].strip(), lin[i + 1]))
    capas, ents, i = {}, [], 0
    while i < len(pares):
        c, v = pares[i]
        if c == "0" and v == "LAYER":
            d = {}
            j = i + 1
            while j < len(pares) and pares[j][0] != "0":
                d[pares[j][0]] = pares[j][1]
                j += 1
            capas[d.get("2")] = int(d.get("62", 7))
            i = j
            continue
        if c == "0" and v in ("LINE", "CIRCLE", "TEXT"):
            d = {"tipo": v}
            j = i + 1
            while j < len(pares) and pares[j][0] != "0":
                d[pares[j][0]] = pares[j][1]
                j += 1
            ents.append(d)
            i = j
            continue
        i += 1
    return capas, ents


def dibujar(capas, ents, ventana, salida, con_textos, titulo):
    fig, ax = plt.subplots(figsize=(16, 9.5) if ventana is None else (16, 10), dpi=130)
    x0, x1, y0, y1 = ventana or (None,) * 4

    def dentro(x, y):
        return ventana is None or (x0 <= x <= x1 and y0 <= y <= y1)

    for e in ents:
        capa = e.get("8", "")
        col = ACI.get(capas.get(capa, 7), "#222222")
        if e["tipo"] == "LINE":
            xa, ya, xb, yb = float(e["10"]), float(e["20"]), float(e["11"]), float(e["21"])
            if dentro(xa, ya) or dentro(xb, yb):
                lw = {"EPANET_TUBO_DN90": 1.0, "EPANET_TUBO_DN110": 1.6, "EPANET_TUBO_DN160": 2.2, "EPANET_TUBO_DN200": 3.0, "EPANET_TUBO_DN250": 3.8}.get(capa, 1.0)
                ax.plot([xa, xb], [ya, yb], color=col, lw=lw, solid_capstyle="round", zorder=2)
        elif e["tipo"] == "CIRCLE":
            x, y, r = float(e["10"]), float(e["20"]), float(e["40"])
            if not dentro(x, y):
                continue
            if capa == "EPANET_RESERVORIO":
                ax.add_patch(plt.Circle((x, y), r, fill=True, color="#1f3fd0", alpha=0.35, zorder=3))
                ax.add_patch(plt.Circle((x, y), r, fill=False, color="#1f3fd0", lw=2, zorder=4))
            elif capa == "EPANET_REVISAR":
                ax.add_patch(plt.Circle((x, y), r * (1.0 if ventana else 2.2), fill=False, color=col, lw=1.6, zorder=6))
            else:
                ax.add_patch(plt.Circle((x, y), r * (1.0 if ventana else 1.6), color=col, zorder=5))
        elif e["tipo"] == "TEXT" and con_textos:
            x, y = float(e["10"]), float(e["20"])
            if dentro(x, y):
                capa_t = capa
                if capa_t == "EPANET_REVISAR":
                    ax.text(x, y, e["1"], color="#c000c0", fontsize=7, weight="bold", zorder=8)
                else:
                    ax.text(x, y, e["1"], fontsize=5.2, rotation=float(e.get("50", 0)), rotation_mode="anchor",
                            color="#444444" if capa_t == "EPANET_TUBO_TXT" else "#000000", zorder=7)
        elif e["tipo"] == "TEXT" and capa == "EPANET_REVISAR":
            pass
    ax.set_aspect("equal")
    if ventana:
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
    else:
        ax.autoscale()
    ax.set_title(titulo, fontsize=12, loc="left")
    ax.grid(alpha=0.2)
    # leyenda
    from matplotlib.lines import Line2D
    h = [Line2D([0], [0], marker="o", color="w", markerfacecolor=ACI[1], markersize=8, label="Nodo P < 15 mca"),
         Line2D([0], [0], marker="o", color="w", markerfacecolor=ACI[2], markersize=8, label="Nodo 15-25 mca"),
         Line2D([0], [0], marker="o", color="w", markerfacecolor=ACI[3], markersize=8, label="Nodo 25-35 mca"),
         Line2D([0], [0], marker="o", color="w", markerfacecolor=ACI[4], markersize=8, label="Nodo > 35 mca"),
         Line2D([0], [0], marker="o", color=ACI[6], markerfacecolor="none", markersize=10, label="EPANET_REVISAR"),
         Line2D([0], [0], color=ACI[6], lw=1.0, label="Tubo DN90"), Line2D([0], [0], color=ACI[4], lw=1.6, label="Tubo DN110"),
         Line2D([0], [0], color=ACI[3], lw=2.2, label="Tubo DN160"), Line2D([0], [0], color=ACI[2], lw=3.0, label="Tubo DN200"),
         Line2D([0], [0], color=ACI[1], lw=3.8, label="Tubo DN250")]
    ax.legend(handles=h, loc="upper left", fontsize=8, ncol=2, framealpha=0.9)
    fig.tight_layout()
    fig.savefig(salida)
    plt.close(fig)
    return salida


def main(corrida, extra):
    d = os.path.join(BASE, "resultados", "v3_agua", corrida, "civil3d")
    capas, ents = leer_dxf(os.path.join(d, "red_agua_modelo_epanet.dxf"))
    por_capa = {}
    for e in ents:
        por_capa[e.get("8")] = por_capa.get(e.get("8"), 0) + 1
    print("Capas del DXF y entidades:")
    for k in sorted(por_capa):
        print("  %-26s %5d  (color %s)" % (k, por_capa[k], capas.get(k)))
    out = []
    if extra:
        x0, x1, y0, y1 = map(float, extra[:4])
        out.append(dibujar(capas, ents, (x0, x1, y0, y1), os.path.join(d, "vista_%s.png" % extra[4]), True, "%s - %s" % (corrida, extra[4])))
    else:
        out.append(dibujar(capas, ents, None, os.path.join(d, "vista_general.png"), False, "Red de agua Terra Lima - %s (PRELIMINAR): presion por nodo, DN y puntos a revisar" % corrida))
        out.append(dibujar(capas, ents, (308150, 308480, 8622720, 8622900), os.path.join(d, "vista_zona_R1_reservorios.png"), True, "Zona de los reservorios R1 y R2 (con textos)"))
        out.append(dibujar(capas, ents, (308380, 308660, 8622900, 8623100), os.path.join(d, "vista_zona_fronteras.png"), True, "Zona de fronteras R1/R2 (con textos)"))
    return out


if __name__ == "__main__":
    for p in main(sys.argv[1], sys.argv[2:]):
        print(p)
