# -*- coding: utf-8 -*-
"""Escritura de .inp y ejecucion del motor oficial EPANET 2.2 (runepanet.exe) con lectura del informe."""
import os, re, subprocess, tempfile, shutil

NUM = r"-?\d+\.?\d*(?:[eE][-+]?\d+)?"
RE_NODO = re.compile(r"^\s*(\S+)\s+(%s)\s+(%s)\s+(%s)\s*$" % (NUM, NUM, NUM))
RE_ENLACE = re.compile(r"^\s*(\S+)\s+(%s)\s+(%s)\s+(%s)(?:\s+[A-Za-z]+)?\s*$" % (NUM, NUM, NUM))
RE_HORA = re.compile(r"(?:Node|Link) Results(?: at\s+(\d+):(\d+)\s+hrs)?")


def escribir_inp(path, titulo, nombre_res, nivel_res, xy_res, nodos, cotas, demandas_ls, ed, D, nres,
                 patron=None, horas=0):
    """nodos: array (n,2); cotas: m; demandas_ls: L/s por nodo (base si hay patron); ed: [(a,b,L)]; D: m interior.
    La tuberia SALIDA conecta el reservorio con el nodo nres (2 m, DN 600)."""
    L = ["[TITLE]", titulo, "", "[JUNCTIONS]", ";ID Elev Demand(L/s)"]
    for i in range(len(nodos)):
        L.append("N%d %.2f %.4f" % (i, cotas[i], demandas_ls[i]))
    L += ["", "[RESERVOIRS]", ";ID Head", "%s %.2f" % (nombre_res, nivel_res), "", "[TANKS]", "",
          "[PIPES]", ";ID N1 N2 Length(m) Diam(mm) Rough(HW) MinorLoss Status",
          "SALIDA_%s %s N%d 2 600 140 0 Open" % (nombre_res, nombre_res, nres)]
    for p, (a, b, Lm) in enumerate(ed):
        L.append("T%d N%d N%d %.2f %.1f 140 0 Open" % (p, a, b, Lm, D[p] * 1000))
    L += ["", "[PUMPS]", "", "[VALVES]", "", "[DEMANDS]", ""]
    L += ["[PATTERNS]"]
    if patron:
        for i in range(0, len(patron), 6):
            L.append("P1 " + " ".join("%.4f" % v for v in patron[i:i + 6]))
    L += ["", "[CONTROLS]", "", "[OPTIONS]", "Units LPS", "Headloss H-W", "Specific Gravity 1", "Viscosity 1", "Trials 100",
          "Accuracy 0.001", "Unbalanced Continue 10", "Pattern %s" % ("P1" if patron else "1"), "Demand Multiplier 1", "",
          "[TIMES]", "Duration %d" % horas]
    if horas:
        L += ["Hydraulic Timestep 1", "Pattern Timestep 1", "Report Timestep 1", "Report Start 0"]
    L += ["", "[REPORT]", "Status No", "Summary No", "Nodes ALL", "Links ALL", "", "[COORDINATES]", ";Node X Y"]
    for i in range(len(nodos)):
        L.append("N%d %.2f %.2f" % (i, nodos[i][0], nodos[i][1]))
    L.append("%s %.2f %.2f" % (nombre_res, xy_res[0], xy_res[1]))
    L += ["", "[END]"]
    with open(path, "w", encoding="ascii", errors="replace") as f:
        f.write("\n".join(L) + "\n")


def leer_inp(path):
    sec, cur = {}, None
    for l in open(path, encoding="ascii", errors="replace"):
        l = l.rstrip("\n")
        if l.startswith("["):
            cur = l.strip()
            sec[cur] = []
        elif l.strip() and not l.startswith(";") and cur:
            sec[cur].append(l.split())
    return sec


def correr(inp, exe):
    """Devuelve {hora: {'nodos': {id: (demanda, carga, presion)}, 'enlaces': {id: (caudal, velocidad, perdida)}}}."""
    tmp = tempfile.mkdtemp()
    try:
        ti = os.path.join(tmp, "t.inp")
        shutil.copyfile(inp, ti)
        r = subprocess.run([exe, ti, os.path.join(tmp, "t.rpt")], capture_output=True, text=True)
        rpt = open(os.path.join(tmp, "t.rpt"), encoding="latin-1").read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if "Error" in rpt[:400] or "ERROR" in r.stdout:
        raise RuntimeError("EPANET reporto un error: " + (rpt[:400] or r.stdout))
    res, hora, modo = {}, 0, None
    for l in rpt.splitlines():
        m = re.search(r"(Node|Link) Results(?: at\s+(\d+):(\d+)(?::\d+)?\s+hrs)?", l)
        if m:
            modo = "nodos" if m.group(1) == "Node" else "enlaces"
            hora = int(m.group(2)) if m.group(2) else 0
            res.setdefault(hora, dict(nodos={}, enlaces={}))
            continue
        if modo == "nodos":
            m = RE_NODO.match(l)
            if m:
                res[hora]["nodos"][m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
        elif modo == "enlaces":
            m = RE_ENLACE.match(l)
            if m:
                res[hora]["enlaces"][m.group(1)] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    if not res or not res[min(res)]["nodos"]:
        raise RuntimeError("No se pudo leer el informe de EPANET")
    return res
