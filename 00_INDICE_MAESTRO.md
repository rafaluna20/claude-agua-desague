# Expediente Terra Lima: índice maestro (v2)

Versión de trabajo creada el 2026-10-03 a partir de `expediente-terraLima` (la original queda intacta). Reglas de formatos, nombres y códigos: `00_REGLAS_DE_DOCUMENTOS.md`. Lista de todos los documentos: `00_REGISTRO_MAESTRO.md`.

## Estructura
```
A_EXPEDIENTE_HU/                      lo que se presenta o recibe de la autoridad (ver A_EXPEDIENTE_HU/00_LEEME_Estructura_Division.md)
  A0_Comun/                           sirve a las dos partes: legal base, estudios básicos, plano matriz, división P1/P2
  P1_Parte_1/                      Parte 1 (768 lotes): agua Asociación Santa María, PTAR, luz Luz del Sur
  P2_Parte_2/                      Parte 2 (582 lotes): agua y desagüe SEDAPAL, luz Luz del Sur
B_GESTION_INTERNA/                    uso interno de Renasur; no se entrega
  B1_Gestion                          gobernanza, calendario, contratos, valorizaciones, planes y registros de problemas
  B2_Costos_y_Presupuestos
  B3_Analisis_Tecnicos                hipótesis y estrategias (agua, PTAR, electrificación)
  B4_Supervision_y_Calidad
  B5_Operacion_y_Mantenimiento
  B6_Correspondencia
  B7_Presentaciones_Renders
obra agua y desague/      referencias de terceros (reglamento SEDAPAL, carta y sustento de S&G) y borradores
_plantillas_originales/   contrato y TDR genéricos (modelo, no documentos del proyecto)
_archivo_temporal/        textos extraídos, scripts y borrador del organigrama
_herramientas/            md2pdf.py, lista_a_excel.py
```

## Estado de A
| Carpeta | Estado | Contenido real |
|---|---|---|
| A0 / 1_Legal_Base | **Vacía** | Faltan licencia/resolución 002-2025, partida registral, certificados |
| A0 / 2_Estudios_Basicos | Parcial | Solo topografía (informe, TP-01/02/03, UL-01, 2 fotos de BMs). Faltan suelos, ambiental, CIRA, tráfico, hidrología, riesgos |
| A0 / 3_Planimetria_General | **Vacía** | Falta el plano matriz de toda la habilitación |
| A0 / 4_Division_P1_P2 | **Vacía (nueva)** | **Falta el plano de delimitación entre Parte 1 y Parte 2** |
| P1 y P2 | **Vacías** | Estructura lista; guía en `00_LEEME_Parte1.md` y `00_LEEME_Parte2.md` |

## Estado de B
| Carpeta | Estado |
|---|---|
| B1 Gestión | Con contenido: TL-GES-001/002/003, contrato TL-CON-005 (ficha, firmado, PDF) |
| B2 Costos | Con contenido: TL-COS-001 (real vs. supuestos) y 3 análisis de supuestos |
| B3 Análisis técnicos | 14 documentos TL-TEC (hipótesis sin validar; ver alerta TL-TEC-001) |
| B4 Supervisión | Mínimo: registro diario con 2 entradas (TL-SUP-001) |
| B5, B6, B7 | Vacías |

## Pendientes prioritarios
1. **Conseguir el contenido de A1**: licencia/resolución de habilitación, partida registral, factibilidades. Es lo que respalda la recepción de obras y la inscripción de lotes.
2. Cargar en A4 los proyectos de ingeniería aprobados (anexos A y B del contrato de saneamiento).
3. Definir y dibujar la **frontera entre Parte 1 y Parte 2** (A0/4_Division_P1_P2).
4. Confirmar lotes vendidos reales (Odoo) y actualizar `TL-GES-003`.
5. Decidir el esquema de agua/desagüe (ver `TL-TEC-001`).
5. Confirmar fecha de inicio y supervisor designado del contrato 005-2026.
6. Revisar las observaciones de la ficha del contrato (posible adenda).
7. Contrastar pistas y veredas V3 con la topografía real y reflejarlo en B2.
8. `MD_Topografia_HU_1350_Lotes_Ejemplo.md` (en A2) es un ejemplo, no un documento del proyecto: sacarlo de A cuando se confirme.
