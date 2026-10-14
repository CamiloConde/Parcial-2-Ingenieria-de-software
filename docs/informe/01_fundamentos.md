## 1. Fundamentos: problema, actores y alcance

**Problema.** Un colectivo de escritores prepara una ficción interactiva para un festival universitario. Necesita un programa que interprete relatos escritos en archivos, ofrezca decisiones que dependen de lo ocurrido en la partida y avise de los errores del contenido antes de que un lector lo juegue. Hoy cualquier cambio en la historia exigiría modificar código, y un archivo mal escrito podría cerrar el programa frente al público.

**Actores.**

| Actor | Rol frente al sistema | Interés principal |
|---|---|---|
| Escritora (autora de contenido) | Escribe y edita archivos de historia JSON; ejecuta la validación | Cambiar escenas y decisiones sin programar (N01, N06) |
| Diseñador de la experiencia | Define condiciones y efectos de las opciones | Decisiones con consecuencias (N02, N03, N04) |
| Lector (jugador) | Recorre la historia en consola | Leer, elegir, reconocer el final y reiniciar (N02, N05) |
| Coordinadora del festival | Opera el programa en el evento | Que un error no cierre el programa de forma inesperada (N06) |

**Alcance de la versión entregada.** Incluye: carga de historias desde archivos JSON con un contrato documentado; validación previa con mensajes que indican la causa y el campo o ID; motor de sesión con condiciones de igualdad booleana y efectos de asignación; interfaz de consola, reinicio y detección de bloqueo durante la partida. **Fuera de alcance:** cuentas, base de datos, guardado entre ejecuciones, red, editor visual, audio, imágenes, lenguaje de expresiones y análisis automático de todos los caminos del relato.

**Riesgos y mitigación.**

| ID | Riesgo | Prob./Impacto | Mitigación aplicada |
|---|---|---|---|
| R1 | Un archivo con errores (destino inexistente, variable mal escrita) provoca un cierre inesperado durante el festival | Media / Alto | Validación completa **antes** de abrir la sesión; la interfaz atrapa `ErrorContenido` y muestra la lista de problemas; pruebas U4 parametrizadas con las nueve categorías |
| R2 | La lógica de la historia de referencia queda "cableada" en el código y la segunda historia no funciona sin editar el motor | Media / Alto | El motor evalúa condiciones y efectos solo desde los datos; prueba de modificabilidad con una segunda historia de IDs y variables distintos; revisión de que `motor/` no contiene IDs como `E1` o `conoce_origen` |

**Priorización de atributos de calidad.** Se ordenaron según las voces del cliente y la rúbrica:

1. **Confiabilidad** (coordinadora: "el lector no debe encontrarse con un cierre inesperado"). Una entrada inválida no puede alterar ni terminar la partida.
2. **Modificabilidad del contenido** (escritora: "agregar escenas sin pedir que modifiquen el programa"). Es la razón de existir del motor.
3. **Claridad de errores** (N06). Sin ella la escritora no puede corregir sola su archivo.
4. **Facilidad de uso** de la consola: importante, pero con menor riesgo porque la interacción es mínima (elegir un número).

El rendimiento no se priorizó: las historias tienen decenas de escenas y la evaluación es lineal.

**Decisión de responsabilidad profesional (autoría y dependencias).** El contenido narrativo pertenece al colectivo de escritores; el motor no modifica, recolecta ni transmite los textos ni las decisiones de los lectores (no hay telemetría ni archivos de registro de partidas). Además, se decidió **no usar dependencias en tiempo de ejecución**: el motor solo usa la biblioteca estándar de Python (licencia PSF) y la única dependencia de desarrollo es `pytest` (licencia MIT), documentada en el README. Así el festival puede ejecutar el programa sin descargar paquetes de terceros y sin obligaciones de licencia adicionales.
