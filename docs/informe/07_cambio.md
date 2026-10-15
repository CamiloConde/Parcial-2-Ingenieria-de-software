## 7. Gestión del cambio: deshacer la última decisión (SC01)

**Versión de partida.** Al recibir la solicitud de la hora 6 la versión disponible era el tag **`v1.0`** (commit `d090e6c`). Estaba completa: 54 pruebas pasaban (`evidencias/registro_pruebas_v1.0.txt`) y no tenía retroceso, según el acuerdo provisional P1. La solicitud **SC01** reemplaza ese acuerdo y responde la pregunta P1: el retroceso es de **un solo nivel** y revierte todas las consecuencias.

**Nueva necesidad y requisitos.** *N07 (SC01):* el lector necesita deshacer su última decisión y que se reviertan todas sus consecuencias.

| RF | Requisito | Criterio de aceptación |
|---|---|---|
| RF15 | Deshacer restaura exactamente la escena y **todas** las variables que había antes de la última elección válida, también desde una escena final. | Desde `E2`, `investigar` lleva a `E3` con `conoce_origen = verdadero`; deshacer devuelve a `E2` con `conoce_origen = falso`. Desde `E4`, `E5` o `E6`, deshacer devuelve a `E3` con los valores previos. |
| RF16 | El retroceso es de un solo nivel: al comenzar no está disponible, y después de deshacer no se permite otro hasta realizar una nueva elección válida. | Un segundo deshacer seguido no cambia nada y se informa "No hay una decisión para deshacer"; tras `continuar`, deshacer vuelve a estar disponible. |
| RF17 | Reiniciar elimina el historial. Una opción inexistente o no habilitada no modifica la sesión ni sustituye la última elección válida guardada. | Tras reiniciar, deshacer es rechazado en `E1`. En `E3`, enviar `activar_sin_verificar` (no habilitada) y luego deshacer regresa a `E2`. |

**Análisis de impacto.**

| Artefacto | Impacto | Cambio realizado |
|---|---|---|
| Requisitos | Alto | Se agregan N07, RF15-RF17. P1 pasa de "acuerdo provisional" a "respondida por SC01". RF06 y RF10 no cambian su texto, pero su aceptación ahora también cubre el historial. Los criterios de RF09 y RF14 se actualizaron porque en un final o en un bloqueo ahora también se ofrece deshacer (defecto D2, detectado en la revisión cruzada). |
| Casos de uso (A2) | Medio | Nuevo CU06 *Deshacer última decisión*. |
| Clases (A3) | Medio | `Sesion` agrega `_anterior: EstadoSesion \| None`, `puede_deshacer` y `deshacer()`. Nueva clase `EstadoSesion` (instantánea inmutable). |
| Secuencia (A4) | Bajo | `elegir` guarda la instantánea antes de aplicar los efectos. |
| Estados (A5) | Medio | Nueva transición "deshacer" desde `EnCurso`, `Finalizada` y `Bloqueada` cuando hay instantánea. |
| Componentes (A6) | Nulo | Las capas y dependencias no cambian; el contenido JSON tampoco (RNF01 se mantiene). |
| Código | Bajo | `motor/sesion.py` (+1 clase, +2 miembros) e `interfaz/consola.py` (comando `d`). Cargador, validador y modelo sin cambios. |
| Pruebas | Medio | Nueva U6 con variantes; se extienden U5 (reiniciar borra historial) e I1 (deshacer desde un final tras cargar el archivo). |
| Trazabilidad, README, backlog | Medio | Filas RF15-RF17 en la matriz (A7), comando `d` en el README y tarjetas B12-B13 en el tablero. |

**ADR-03. Mecanismo de deshacer: instantánea del estado previo.**
*Contexto:* hay que restaurar **exactamente** la escena y todas las variables, con un solo nivel. *Alternativas:* (a) patrón Command, en el que cada efecto guarda su inverso; (b) pila de historial completa limitada a un elemento; (c) una **instantánea** inmutable (`EstadoSesion`) del estado anterior a la última elección válida. *Elección:* (c). *Consecuencias:* (+) la restauración es exacta por construcción, aunque un efecto asigne el valor que la variable ya tenía (caso en que un inverso calculado fallaría); (+) "un solo nivel" se cumple naturalmente: al deshacer, la instantánea pasa a `None`; (+) el cambio se concentra en `elegir`, que ya era el único punto que modifica el estado; (−) para rehacer o deshacer varios niveles habría que cambiar la instantánea por una pila (no se exige).

**Evidencia del comportamiento nuevo.** `tests/test_cambio_deshacer.py` (U6 y sus variantes), `tests/test_motor.py::test_u5_reiniciar_elimina_historial`, `tests/test_i1_integracion.py::test_i1_deshacer_desde_un_final_*` y el recorrido `evidencias/recorridos/deshacer.txt`. La versión posterior al cambio es el tag **`v2.0`**.
