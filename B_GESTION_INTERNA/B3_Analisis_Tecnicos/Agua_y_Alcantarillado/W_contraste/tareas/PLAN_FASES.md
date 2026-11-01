# Plan de fases y puertas de revision - contraste sanitario Terra Lima

**Rol del principal.** Coordina el orden de trabajo, las entradas, los supuestos, las puertas de revision y la coherencia entre entregables. No sustituye al calculista ni al revisor independiente.

**Alcance vigente.** Diseno independiente de agua potable y alcantarillado para contrastar la obra ejecutada por S&G Edifica. Es un espacio interno de trabajo; ningun resultado es presentable ni ejecutable hasta la revision y firma de un ingeniero sanitario colegiado (**PARA VALIDAR CON VALVERDE**).

## Base controlada

- Geometria global: `datos/v3_48calles/` (congelada; 48 calles y 1,341 lotes). Geometria vigente para este expediente: `datos/v4_primera_expediente/` (444 lotes dentro de `00_primera_expediente`; `E01MZS002P` queda en revision de limite).
- Prediseno de desague existente: `resultados/v0.4_48calles_pasajes/`. Es una referencia preliminar y no un diseno aprobado.
- Supuestos: `supuestos.md`. Los pendientes no se convierten en datos de diseno por el solo hecho de aparecer en un borrador.
- Obra ejecutada: solo podra considerarse contrastable contra planos de replanteo/as-built, protocolos y evidencia georreferenciada. Las cartas, informes sin firma y alegaciones conservan su propio estado de evidencia.

## Fases y secuencia

| Fase | Especialista | Entrada minima | Salida controlada | Puerta de salida |
|---|---|---|---|---|
| 1. Criterios y evidencia | Normas y fuentes; Datos y as-built | Textos normativos, expediente y fuentes locales | Libro de normas, inventario ejecutado y brechas | G1 |
| 2. Diseno preliminar coordinado | Desague; Agua | G1 aprobada y topografia/demanda suficientes | Calculos reproducibles, perfiles, buzones y modelo de agua | G2 |
| 3. Metrados y presupuesto | Metrados y presupuesto | G2 y precios/fuentes de Odoo identificados | Metrados, APU, presupuesto y cronograma preliminares | G3 |
| 4. Planos y memorias | Planos y memorias | G2/G3, plantillas y responsables definidos | DXF/DWG, memorias y especificaciones de trabajo | G3 |
| 5. Revision independiente | Revisor independiente | Todos los entregables anteriores y fuentes | Matriz de observaciones con evidencia y severidad | G4 |
| 6. Cierre tecnico | Principal + ingeniero sanitario | Observaciones cerradas y datos faltantes resueltos | Paquete listo para formalizacion y firma | G4 aprobada |

## G1 - criterios y base de contraste

G1 solo puede abrir la Fase 2 cuando se cumplan todos estos controles:

1. Cada criterio de agua, alcantarillado y PTAR tiene fuente, numeral y estado `VERIFICADO` o `NO VERIFICADO`; no se usaran como definitivos los criterios no verificados.
2. El inventario de la obra ejecutada diferencia `CONFIRMADO`, `ALEGADO POR EL CONTRATISTA`, `BORRADOR` y `POR CONFIRMAR`, y declara si existe o no informacion georreferenciada/as-built.
3. El principal registra la decision del responsable tecnico sobre los supuestos que condicionan el calculo. Al corte 2026-10-10, la fuente (S-006) y el alcance general (S-001) tienen direccion de usuario, pero siguen pendientes la inclusion de E01MZS002P, la poblacion/dotacion, la factibilidad y condicion de entrega, las interfaces PTAR y las decisiones topograficas/constructivas.
4. Se identifica el ingeniero sanitario revisor y el alcance de su validacion.

Si falta un elemento, se pueden elaborar alternativas y borradores marcados `PRELIMINAR`, pero no se cerrara G1 ni se emitira un diseno final.

## G2 - diseno preliminar coordinado

- Desague: red, perfiles, cotas de batea, buzones, cruces y descarga/PTAR con trazabilidad a criterios y supuestos.
- Agua: fuente de servicio decidida (Asociacion/SEDAPAL/PTAR cuando corresponda), demanda, reservorios, matriz de Av. E, red mallada, presiones y velocidades; archivo EPANET reproducible si resulta aplicable.
- Coordinacion: separaciones agua-desague, interferencias, lotes sin conexion y tramos que dependan de pasajes inferidos.
- No se permite usar terreno, trazos, capacidad de reservorios o red ejecutada no comprobados como si fueran as-built.

## G3 - documentos de trabajo completos

Antes de metrados, presupuesto, cronograma, planos y memorias, cada cantidad debe vincularse con una salida versionada de diseno. Las partidas de Odoo son referencia de precios/estructura y deben conservar fecha, fuente y alcance. Los documentos siguen siendo internos hasta la revision independiente.

## G4 - cierre para formalizacion

El revisor independiente rehace las verificaciones criticas con un metodo distinto cuando sea posible, contrasta planos, metrados, memoria y presupuesto, y emite observaciones clasificadas. Solo pueden cerrarse con evidencia. La firma, responsabilidad profesional y eventual presentacion externa son **PARA VALIDAR CON VALVERDE**.

## Regla de continuidad durante la ausencia del usuario

Los especialistas pueden avanzar hasta la siguiente puerta usando solo datos verificables y salidas rotuladas como preliminares. Una decision de alcance, una norma no disponible, un as-built faltante o un supuesto pendiente se registra como bloqueo; no se rellena con una cifra inventada ni se reemplaza la aprobacion del responsable tecnico.
