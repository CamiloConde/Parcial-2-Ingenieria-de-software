## 3. Requerimientos

### 3.1 Requisitos funcionales

Cada RF describe un comportamiento observable y su criterio de aceptación (CA). "Historia de referencia" es `historias/la_ultima_transmision.json`.

| RF | Necesidad | Requisito | Criterio de aceptación |
|---|---|---|---|
| RF01 | N01 | El sistema carga una historia desde la ruta de un archivo JSON indicada al ejecutar el programa. | `python jugar.py historias/el_faro.json` muestra el título y la escena inicial de ese archivo, no los de otra historia. |
| RF02 | N01 | Al comenzar una partida, la escena actual es la indicada en `inicio` y cada variable toma el valor declarado en `variables`. | Con la historia de referencia, una sesión nueva está en `E1` con `conoce_origen = falso` y `confia_en_la_voz = falso`. |
| RF03 | N02 | El sistema muestra el texto de la escena actual. | Al iniciar la historia de referencia se muestra el texto de `E1`. |
| RF04 | N02 | El sistema muestra **únicamente** las opciones de la escena actual cuyas condiciones se cumplen todas; un mapa de condiciones vacío habilita la opción. | En `E3` con `conoce_origen = verdadero` se muestran exactamente "Activar con código" y "Cortar comunicación" (CA01); con `conoce_origen = falso`, exactamente "Activar sin verificar" y "Cortar comunicación". |
| RF05 | N03 | Al elegir una opción habilitada, el sistema aplica todos sus efectos y cambia la escena actual al destino de la opción. | Desde `E2`, elegir `investigar` deja la sesión en `E3` con `conoce_origen = verdadero` (CA01). |
| RF06 | N03 | Si se solicita una opción inexistente o no habilitada, el motor la rechaza, informa el motivo y no modifica escena ni variables. | En `E3` sin conocer el origen, enviar `activar_codigo` directamente al motor devuelve rechazo y la sesión sigue en `E3` con las mismas variables (CA02). |
| RF07 | N03 | La interfaz rechaza entradas no reconocidas (texto libre, número fuera de rango, vacío) con un mensaje y sin modificar la partida. | En `E1`, escribir `abc` o `9` muestra "Entrada no válida…" y vuelve a mostrar `E1`. |
| RF08 | N04 | Los valores de las variables se conservan durante toda la partida y las condiciones posteriores se evalúan con ellos. | Tras `revisar` → `investigar`, en `E3` aparece "Activar con código" y no "Activar sin verificar". |
| RF09 | N05 | Cuando la escena actual es final, el sistema muestra su texto, la indica como desenlace y no ofrece opciones de avance. | Al llegar a `E6` se muestra "FIN" con el texto de `E6` y solo los comandos reiniciar y salir. |
| RF10 | N05 | El lector puede reiniciar en cualquier momento; la sesión vuelve a la escena inicial y a los valores iniciales de todas las variables. | Tras llegar a `E4`, reiniciar deja la sesión en `E1` con todas las variables en falso (U5). |
| RF11 | N06 | El sistema valida el archivo completo antes de abrir una sesión; si existe algún error, no se abre una sesión jugable. | Una copia con destino `E99` se rechaza y no se muestra ninguna escena (CA03). |
| RF12 | N06 | Cada error de contenido se informa con su categoría, la causa y el campo o ID involucrado. | El error de CA03 indica `[DESTINO_INEXISTENTE]`, la escena, la opción y el valor `E99`. |
| RF13 | N06 | El escritor puede validar un archivo sin jugarlo mediante `--validar`; el programa termina con código 0 si es válido y 1 si no lo es. | `python jugar.py --validar historias/invalidas/destino_inexistente.json` lista el error y termina con código 1. |
| RF14 | N06 | Si durante una partida una escena no final no tiene opciones habilitadas, el sistema informa el bloqueo y permite reiniciar o salir. | Con `historias/invalidas/bloqueo_en_partida.json`, al llegar a la escena bloqueada se muestra "BLOQUEO" y reiniciar vuelve al inicio. |

### 3.2 Requisitos no funcionales medibles

| RNF | Atributo | Requisito y métrica | Procedimiento de verificación | Evidencia |
|---|---|---|---|---|
| RNF01 | Modificabilidad del contenido | Incorporar una historia nueva o agregar una escena y una opción a una existente requiere **0 líneas modificadas** en `motor/` e `interfaz/`. | (a) Cargar y recorrer hasta todos sus finales la segunda historia `el_faro.json`; (b) el script agrega por programa una escena `E7` y una opción a una copia temporal de la historia de referencia y la juega; (c) compara el hash SHA-256 de `motor/` e `interfaz/` antes y después; (d) `git log --stat` del commit que añadió la segunda historia solo toca `historias/`. | `tests/test_rnf.py::test_rnf01_*`, `evidencias/rnf_resultados.txt` |
| RNF02 | Claridad de errores | El **100 %** de los archivos de `historias/invalidas/` produce con `--validar`: código de salida 1, un mensaje con la categoría `[...]` y el ID o campo esperado, y **0** trazas `Traceback`. | El script ejecuta `jugar.py --validar` como proceso externo sobre cada archivo y comprueba los tres criterios. | `tests/test_rnf.py::test_rnf02_*`, `evidencias/rnf_resultados.txt` |
| RNF03 | Confiabilidad | Ante **1000** entradas aleatorias de la interfaz (semilla fija 2026; texto, números, IDs, comandos), hay **0** excepciones no controladas y cada entrada rechazada deja escena y variables idénticas. | El script alimenta la interfaz de consola con las entradas generadas y compara el estado antes y después de cada entrada rechazada. | `tests/test_rnf.py::test_rnf03_*`, `evidencias/rnf_resultados.txt` |

### 3.3 Preguntas al cliente, respuestas y supuestos

| ID | Pregunta | Respuesta o supuesto registrado |
|---|---|---|
| P1 | La escritora quiere retroceder siempre y el diseñador quiere decisiones irreversibles. ¿El retroceso debe estar disponible siempre, limitarse a cierto número de pasos o prohibirse en decisiones marcadas como irreversibles? | **Acuerdo provisional:** la primera versión no implementa retroceso. No se presupone la decisión final del cliente. |
| P2 | ¿Las opciones cuyas condiciones no se cumplen deben verse deshabilitadas o no deben verse? | **Supuesto:** no se muestran (N02: "ver únicamente decisiones compatibles"; CA01 exige ver exactamente dos opciones en `E3`). |
| P3 | ¿El lector debe ver los valores de las variables durante la partida? | **Supuesto:** no; revelaría la lógica del relato. Para pruebas y demostración existe la opción `--depurar`, que muestra el estado. |

### 3.4 Revisión cruzada: defecto detectado y corrección

Los requisitos se revisaron entre integrantes contra N01-N06 y CA01-CA03 antes de implementar el motor.

| Defecto | Hallazgo | Corrección |
|---|---|---|
| D1 (ambigüedad / contradicción) | La primera redacción de RF04 decía "muestra las opciones de la escena actual **e indica cuáles están disponibles**". Admitía mostrar también las opciones no habilitadas (por ejemplo, en gris), lo que contradice N02 ("ver **únicamente** decisiones compatibles") y CA01, que exige ver **exactamente dos** opciones en `E3`. Además su criterio de aceptación no permitía comprobar que la opción no habilitada quedara oculta. | RF04 se reescribió como "muestra **únicamente** las opciones cuyas condiciones se cumplen todas" y su criterio ahora verifica los dos casos de `E3` con conjuntos exactos. Se alineó con el supuesto P2. Cambio visible en el historial de Git (commit "Corrige RF04 tras revisión cruzada de requisitos"). |
