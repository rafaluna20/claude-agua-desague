# W_contraste: espacio de trabajo del diseño de contraste de agua y desagüe

**Qué es.** Carpeta de trabajo (borradores; no lleva código de documento, regla 5 de `00_REGLAS_DE_DOCUMENTOS.md`) donde un agente principal y varios subagentes diseñan **desde cero** el agua y el desagüe de Terra Lima / Pucusana para **compararlo con lo ya ejecutado** por S&G Edifica. Plan y decisión de alcance: `TL-TEC-015`.

**Reglas de la carpeta**
1. `datos/` = entradas **congeladas** (ver `MANIFIESTO.json` con hashes). No se editan. Si cambia un dato, se crea una versión nueva y el principal marca qué resultados quedan desactualizados.
2. `resultados/` = salidas de scripts (Excel, DXF, JSON, PNG), con versión. Los números salen de scripts, no de redacción libre.
3. `supuestos.md` = registro de supuestos S-xxx (valor, fuente, estado: CONFIRMADO / PENDIENTE). Todo documento que use una cifra cita su supuesto o su fuente.
4. `normas/` = libro de normas: cada criterio con norma, numeral y texto verificado. Lo que no se pudo verificar se marca `NO VERIFICADO`.
5. `tareas/` = ficha de entrega (T-xx_ficha.md) e informe (T-xx_informe.md) de cada tarea de subagente.
6. `revision/` = observaciones del revisor independiente.
7. Nombres sin tildes ni espacios y rutas de máximo 200 caracteres (regla 7). Todo `.md` formal que salga de aquí y deba codificarse recibe su fila en `00_REGISTRO_MAESTRO.md` el mismo día.
8. Lo legal se marca **PARA VALIDAR CON VALVERDE**. Nada de aquí es expediente presentable hasta que lo revise y firme un ingeniero sanitario colegiado.
9. Los agentes solo escriben dentro de esta carpeta. Odoo y Civil 3D, en solo lectura.
