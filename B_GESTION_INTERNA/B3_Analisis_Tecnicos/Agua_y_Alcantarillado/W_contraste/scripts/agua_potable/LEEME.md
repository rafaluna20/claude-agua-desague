# Calculo de agua potable de Terra Lima (PRELIMINAR)

Calculo reproducible de la demanda y de la red de agua de toda la habilitacion (1,341 lotes).
Todo es PRELIMINAR y no esta revisado por un tercero. No hace commit ni escribe fuera de `resultados/v3_agua/<corrida>/`.

## Uso rapido (desde esta carpeta)

```
python pruebas.py                                   # pruebas de regresion (deben pasar las 8)
python correr.py --export <export_layer_lines.json> # corrida completa con la red recien exportada de Civil 3D
python correr.py                                    # corrida con la red ya guardada en datos/
python correr.py --set hidraulica.dn_minimo_mm=75   # probar un cambio de parametro (queda anotado en el informe)
python comparar.py c01_2026-10-31 c02_AAAA-MM-DD    # que cambio entre dos corridas
```

## Piezas

| Archivo | Funcion |
|---|---|
| `../../datos/parametros_agua_potable_v1.json` | Todos los parametros con valor, unidad, fuente y estado (VERIFICADO, CONFIRMADO, ELEGIDO, SUPUESTO, NO VERIFICADO) |
| `importar_red.py` | Convierte el export de Civil 3D (`civil3d_export_layer_lines`) en la red del modelo; valida DWG, capas y tipos |
| `demanda.py` | Clasificacion de lotes, poblacion, caudales y volumen del reservorio |
| `modelo.py` | Solver propio, predimensionamiento, escenarios (rotura, 24 h, bomba), presion por lote y puntos a revisar |
| `epanet.py` | Escribe los `.inp` y corre EPANET 2.2 oficial para validar |
| `exportar_dxf.py` | DXF y Excel para Civil 3D, con la capa `EPANET_REVISAR` |
| `informe.py` | `INFORME.md` con hash de entradas y scripts, parametros sin confirmar y resultados |
| `correr.py` | Orquesta todo con compuertas (aborta si falta una capa, el DWG no es el esperado, la grilla del terreno cambio, etc.) |

## Salida de una corrida

`resultados/v3_agua/c<nn>_<fecha>/`: `INFORME.md`, `demanda.json`, `lotes_clasificados.json`, `resultados_modelo.json`,
`escenarios.json`, `presion_lotes.csv`, `revisar.json`, `tuberias_R*.csv`, `epanet/*.inp`, `civil3d/*.dxf` y `*.xlsx`, `procedencia.json`.
La carpeta `_pruebas` la reescribe `pruebas.py` y se puede borrar.

## Equivalencia con la version anterior

Con `--set hidraulica.dn_minimo_mm=110` se reproducen los resultados de `resultados/v2_red_agua_usuario` (14.4 y 18.6 mca).
El piso por defecto es DN 90 (CTPS-PR-02 Art. 8.1.4, N-026 del libro de normas).
