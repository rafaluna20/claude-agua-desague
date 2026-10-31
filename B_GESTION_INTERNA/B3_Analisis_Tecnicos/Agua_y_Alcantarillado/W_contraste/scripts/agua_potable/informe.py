# -*- coding: utf-8 -*-
"""Informe en Markdown de una corrida: entradas con hash, parametros no confirmados, resultados, escenarios y puntos a revisar."""
import collections, datetime, os


def _t(filas, cab):
    s = "| " + " | ".join(cab) + " |\n|" + "|".join(["---"] * len(cab)) + "|\n"
    for f in filas:
        s += "| " + " | ".join(str(c) for c in f) + " |\n"
    return s


def escribir(path, ctx):
    P, dem, res, esc, rev, val, entradas, scripts = ctx["P"], ctx["demanda"], ctx["resumenes"], ctx["escenarios"], ctx["revisar"], ctx["validacion"], ctx["entradas"], ctx["scripts"]
    base = dem["escenarios"]["BASE"]
    L = []
    L.append("# Agua potable Terra Lima - corrida %s\n" % ctx["corrida"])
    L.append("**Estado: PRELIMINAR.** Fecha de la corrida: %s. Motor de verificacion: EPANET %s.\n" % (ctx["fecha"], ctx["epanet_version"]))
    L.append("Este informe sale de un calculo reproducible (`scripts/agua_potable/correr.py`). No esta revisado por un tercero ni reemplaza el diseno de un especialista.\n")
    L.append("## 1. Entradas y trazabilidad\n")
    L.append(_t([(k, v) for k, v in entradas.items()], ["Entrada", "SHA-256 (primeros caracteres) / dato"]))
    L.append("\nScripts usados (SHA-256 de 12 caracteres): " + ", ".join("%s `%s`" % (k, v) for k, v in scripts.items()) + "\n")
    if P.cambios:
        L.append("\n**Parametros cambiados en esta corrida respecto de `parametros_agua_potable_v1.json`:**\n")
        L.append(_t([(k, v["valor_original"], v["valor_corrida"]) for k, v in P.cambios.items()], ["Parametro", "Valor del archivo", "Valor de la corrida"]))
    L.append("\n## 2. Parametros sin confirmar que afectan el resultado\n")
    pend = P.pendientes()
    L.append(_t([(c, str(v)[:60], e, f[:110]) for c, v, u, e, f in pend], ["Parametro", "Valor", "Estado", "Fuente / nota"]))
    L.append("\n## 3. Demanda de toda la habilitacion (%d lotes)\n" % dem["total_lotes"])
    L.append("Clases: " + ", ".join("%s: %d" % (k, v) for k, v in dem["conteo"].items()) + ".\n")
    L.append(_t([(k, e["pob"], round(e["vol_total"]), round(e["qp"], 2), round(e["qmd"], 2), round(e["qmh"], 2), round(e["v_reservorio"]))
                 for k, e in dem["escenarios"].items()], ["Escenario", "Poblacion (hab)", "Volumen m3/d", "Qp L/s", "Qmd L/s", "Qmh L/s", "Reservorio total m3"]))
    L.append("\nReferencia de riego (NO va en la red potable; riego con agua tratada de la PTAR): %.0f m3/d sobre %.0f m2.\n" % (dem["riego_referencia_m3d"], dem["area_riego_m2"]))
    L.append("\n## 4. Resultados hidraulicos por red (hora punta, K2 = %s)\n" % ctx["k2"])
    cab = ["Dato"] + list(res)
    claves = [("lotes", "Lotes"), ("longitud_m", "Longitud (m)"), ("Qmh_Ls", "Qmh (L/s)"), ("presion_min_pico", "Presion minima punta (mca)"),
              ("presion_p5_pico", "Presion P5 (mca)"), ("nodos_menos_10", "Nodos < 10 mca"), ("nodos_menos_15", "Nodos < 15 mca"),
              ("estatica_max", "Estatica maxima (mca)"), ("nodos_mas_50", "Nodos con estatica > 50"), ("v_max", "Velocidad max (m/s)"),
              ("v_min", "Velocidad min (m/s)"), ("grad_max_m_km", "Gradiente max (m/km)"), ("DN", "Tuberias por DN"), ("puntas_muertas", "Puntas muertas"),
              ("nodos_aislados_del_reservorio", "Nodos aislados"), ("niveles_usados", "Niveles usados [min, max]")]
    L.append(_t([[nombre] + [res[g].get(k) for g in res] for k, nombre in claves], cab))
    L.append("\n**Validacion contra EPANET oficial** (diferencia maxima solver propio vs EPANET): " +
             "; ".join("%s: presion %.3f m, caudal %.4f L/s" % (g, v["dif_max_presion_m"], v["dif_max_caudal_Ls"]) for g, v in val.items()) + ".\n")
    L.append("\n## 5. Escenarios adicionales\n")
    L.append("### 5.1 Volumen de reservorio (sin contra incendio)\n")
    L.append(_t([(v["red"], v["vol_diario_m3"], v["regulacion_m3"], v["reserva_m3"], v["total_sin_incendio_m3"]) for v in esc["volumen"]],
                ["Red", "Volumen diario (m3)", "Regulacion (m3)", "Reserva (m3)", "Total (m3)"]))
    L.append("\nContra incendio: %d m3 si la poblacion total llega a %d hab (poblacion base: %d hab)." % (P("demanda.incendio_volumen_m3"), P("demanda.incendio_umbral_hab"), base["pob"]))
    L.append("\n### 5.2 Simulacion de 24 h (EPANET, reservorio a nivel minimo fijo)\n")
    L.append(_t([(e["red"], e["p_min_global"], "%d:00" % e["hora_p_min"], e["p_max_global"], "%d:00" % e["hora_p_max"]) for e in esc["24h"]],
                ["Red", "Presion minima (mca)", "Hora", "Presion maxima (mca)", "Hora"]))
    L.append("\n" + esc["24h"][0]["nota"])
    L.append("\n### 5.3 Rotura de un tramo (hora punta, tramo de ~30 m)\n")
    L.append(_t([(e["red"], e["tramos_evaluados"], e["tramos_que_dejan_sin_agua"],
                  max([f["demanda_perdida_Ls"] for f in e["peor_corte"]] or [0]), max([f["lotes_sin_servicio"] for f in e["peor_corte"]] or [0]),
                  min([f["presion_min_restante"] for f in e["peor_presion_sin_corte"]] or [0])) for e in esc["rotura"]],
                ["Red", "Tramos evaluados", "Tramos que dejan lotes sin agua", "Mayor demanda perdida (L/s)", "Mayor n. de lotes sin servicio", "Peor presion minima sin corte (mca)"]))
    L.append("\nSi se rompe un tramo y no hay otra via de agua, quedan sin servicio todos los lotes aguas abajo. Tramos segun la parte de la red que dejarian sin agua:\n")
    L.append(_t([(e["red"], e.get("distribucion_cortes", {}).get("mas_50_pct", "-"), e.get("distribucion_cortes", {}).get("entre_10_y_50_pct", "-"),
                  e.get("distribucion_cortes", {}).get("menos_10_pct", "-")) for e in esc["rotura"]], ["Red", "Tramos que dejan sin agua >= 50 % de la red", "Entre 10 y 50 %", "Menos de 10 %"]))
    for e in esc["rotura"]:
        L.append("\nTramos con menor presion al romperse otro tramo en %s (sin perder lotes; detalle en `escenarios.json`):\n" % e["red"])
        L.append(_t([(f["tramo"], round(f["x"]), round(f["y"]), f["presion_min_restante"]) for f in e["peor_presion_sin_corte"][:5]],
                    ["Tramo roto", "X", "Y", "Presion minima restante (mca)"]))
    L.append("\n### 5.4 Llenado de los reservorios desde el medidor (aduccion y bomba)\n")
    for b in esc["bomba"]:
        L.append("\n**%s:** aduccion de %s m (recta %s m), Qmd %s L/s, caudal de llenado %s L/s en %s h/d, DN %s, v = %s m/s, hf = %s m, nivel maximo %.1f m.\n" % (
            b["red"], b["longitud_aduccion_m"], b["distancia_recta_m"], b["qmd_Ls"], b["caudal_llenado_Ls"], b["horas_bombeo"], b["DN_aduccion"], b["v_ms"], b["perdida_hf_m"], b["nivel_max_reservorio"]))
        L.append(_t([(c["carga_fuente_m"], c["altura_dinamica_m"], "si" if c["requiere_bomba"] else "gravedad", c["potencia_kW"]) for c in b["casos"]],
                    ["Carga de la fuente (m)", "Altura dinamica (m)", "Bomba", "Potencia (kW)"]))
    L.append("\n" + esc["bomba"][0]["nota"] + "\n")
    L.append("\n## 6. Puntos a revisar (capa EPANET_REVISAR)\n")
    cont = collections.Counter((i["tipo"], "critico" if i["gravedad"] == 1 else "aviso") for i in rev)
    L.append(_t([(t, g, n) for (t, g), n in sorted(cont.items())], ["Tipo", "Gravedad", "Cantidad"]))
    L.append("\n## 7. Presion por lote\n")
    pl = ctx["lotes_presion"]
    bajos = [f for f in pl if f["presion_punta_mca"] < P("hidraulica.presion_min_diseno_mca")]
    L.append("%d de %d lotes quedan por debajo de %.0f mca en hora punta (de ellos %d por debajo de %.0f mca, la norma). Detalle: `presion_lotes.csv`.\n" % (
        len(bajos), len(pl), P("hidraulica.presion_min_diseno_mca"), len([f for f in pl if f["presion_punta_mca"] < P("hidraulica.presion_min_normativa_mca")]), P("hidraulica.presion_min_normativa_mca")))
    L.append("\n## 8. Archivos de la corrida\n")
    for a in ctx["archivos"]:
        L.append("- `%s`" % a)
    L.append("\n## 9. Limitaciones\n")
    for t in ["Regimen permanente con Hazen-Williams; diametros interiores supuestos (0.9 DN) y material/clase sin definir.",
              "Los niveles de los reservorios son supuestos hasta definir su altura real.",
              "La carga de la fuente (Santa Maria) no esta verificada y no hay factibilidad escrita.",
              "La rotura de tramos no considera valvulas de aislamiento (no estan dibujadas): se corta solo el tramo de calculo.",
              "La red no tiene hidrantes, valvulas ni conexiones domiciliarias modeladas; la demanda se asigna al nodo mas cercano de cada lote.",
              "Este calculo no reemplaza la revision independiente del expediente (pendiente hasta que el proyecto este completo)."]:
        L.append("- " + t)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
