## 2. Proceso y agilidad

**Proceso elegido: Kanban incremental con dos entregas internas.** El trabajo dura 12 horas en pareja y llega un cambio en la hora 6. Se usa un tablero con flujo continuo, límite de trabajo en curso (WIP = 2, una tarjeta por integrante en "En progreso") y dos versiones etiquetadas en Git: `v1.0` (versión disponible al recibir el cambio) y `v2.0` (versión final).

**Comparación con la alternativa (Scrum).** Scrum organiza el trabajo en sprints de duración fija con planificación, revisión y retrospectiva. En una ventana de 12 horas, un sprint útil ocuparía casi toda la ventana y sus ceremonias consumirían tiempo de construcción; además, el cambio de la hora 6 llega a mitad de cualquier sprint razonable. Kanban permite reordenar el backlog en el momento en que llega la solicitud sin "romper" un compromiso de sprint.

| Actividad | Cómo se realiza en esta entrega |
|---|---|
| Especificación | RF y RNF propios en este informe, con criterios de aceptación derivados de N01-N06 y de CA01-CA03 |
| Desarrollo | Incremental por tarjetas del tablero: carga y validación, luego motor, luego interfaz, luego cambio |
| Validación | Pruebas automatizadas (pytest) escritas junto a cada incremento; recorridos manuales de los finales; script de verificación de RNF |
| Evolución | Tag `v1.0` antes del cambio; análisis de impacto (sección 7); actualización de backlog, modelos, código, pruebas y matriz; tag `v2.0` |

**Backlog priorizado** (el tablero y sus capturas inicial y final están en el Anexo, sección A9).

| ID | Elemento | Prioridad | Responsable |
|---|---|---|---|
| B01 | Alcance, actores, riesgos y calidad | Alta | Camilo Conde |
| B02 | Requisitos RF/RNF y preguntas al cliente | Alta | Camilo Conde |
| B03 | Revisión cruzada de requisitos | Alta | Miguel Jacome |
| B04 | Modelos (contexto, casos de uso, clases, secuencia, estados) | Alta | Camilo Conde |
| B05 | Arquitectura y decisiones (ADR) | Alta | Camilo Conde |
| B06 | Cargador y validador con mensajes de error | Alta | Camilo Conde |
| B07 | Motor de sesión: opciones, elección, estado, reinicio | Alta | Camilo Conde |
| B08 | Interfaz de consola | Media | Camilo Conde |
| B09 | Pruebas U1-U5 e I1 | Alta | Camilo Conde |
| B10 | Segunda historia y su redacción | Media | Miguel Jacome |
| B11 | Verificación de RNF y ejecución en un segundo equipo | Media | Miguel Jacome |
| B14 | Video de demostración y empaquetado | Alta | Ambos |

**Prácticas ágiles aplicadas.**

1. **Programación en pareja con rol de revisor.** Mientras un integrante implementaba un incremento, el otro revisaba requisitos y pruebas; la revisión cruzada de requisitos (sección 3.4) detectó un defecto antes de codificar.
2. **Pruebas primero en el motor (TDD ligero).** Los escenarios U1-U5 se escribieron a partir de los criterios de aceptación antes o junto con el código de `motor/sesion.py`. Esto obligó a que `elegir` devolviera un resultado verificable en lugar de imprimir en pantalla.

**Alternativa descartada: estimación con *planning poker*.** Con 14 elementos y dos personas, estimar con cartas tomaba más tiempo que la tarea; se usó la distribución de tiempo sugerida por la guía como límite por bloque.

**Definición de terminado.** Una tarjeta pasa a "Hecho" cuando: (1) el código está en `main`; (2) tiene pruebas automatizadas que pasan con `python -m pytest`; (3) los mensajes al usuario están en español y no muestran trazas de Python; (4) los requisitos, modelos y matriz que la mencionan están actualizados; (5) el otro integrante la revisó.

**Aprendizaje y acción de mejora.** _Se registra al cierre de la entrega._
