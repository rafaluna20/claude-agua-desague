# -*- coding: utf-8 -*-
"""Utilidades comunes del calculo de agua potable de Terra Lima (PRELIMINAR).
Parametros siempre desde datos/parametros_agua_potable_v1.json (valor + fuente + estado)."""
import hashlib, json, os, sys, copy

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))  # W_contraste
RUTA_PARAMETROS = os.path.join(BASE, "datos", "parametros_agua_potable_v1.json")


def sha256(path, n=64):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:n]


class Parametros:
    """Acceso por 'seccion.clave'. Registra cada parametro consultado para listar su estado en el informe."""

    def __init__(self, ruta=RUTA_PARAMETROS, cambios=None):
        self.ruta = ruta
        self.datos = json.load(open(ruta, encoding="utf-8"))
        self.sha = sha256(ruta)
        self.cambios = {}
        self.usados = {}
        for k, v in (cambios or {}).items():
            self.fijar(k, v)

    def _nodo(self, clave):
        sec, k = clave.split(".", 1)
        return self.datos[sec][k]

    def fijar(self, clave, valor):
        """Sobrescribe un valor SOLO para esta corrida y queda anotado (estado pasa a 'CAMBIADO EN CORRIDA')."""
        nodo = self._nodo(clave)
        self.cambios[clave] = dict(valor_original=nodo["valor"], valor_corrida=valor)
        nodo["valor"] = valor
        nodo["estado_original"] = nodo.get("estado")
        nodo["estado"] = "CAMBIADO EN CORRIDA"

    def __call__(self, clave):
        nodo = self._nodo(clave)
        self.usados[clave] = nodo
        return nodo["valor"]

    def archivo(self, nombre):
        return os.path.join(BASE, self.datos["archivos"][nombre])

    def tabla_estados(self):
        filas = []
        for clave, nodo in sorted(self.usados.items()):
            filas.append((clave, nodo["valor"], nodo.get("unidad", ""), nodo.get("estado", ""), nodo.get("fuente", "")))
        return filas

    def pendientes(self):
        return [f for f in self.tabla_estados() if f[3] in ("NO VERIFICADO", "SUPUESTO", "CAMBIADO EN CORRIDA")]


def leer_set(args):
    """Lee pares seccion.clave=valor (JSON) de la linea de comandos."""
    out = {}
    for a in args:
        k, v = a.split("=", 1)
        try:
            out[k] = json.loads(v)
        except ValueError:
            out[k] = v
    return out


def dir_corrida(nombre):
    d = os.path.join(BASE, "resultados", "v3_agua", nombre)
    os.makedirs(d, exist_ok=True)
    return d


def escribir_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


def sha_scripts():
    d = os.path.dirname(os.path.abspath(__file__))
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".py"):
            out[f] = sha256(os.path.join(d, f), 12)
    return out
