## A7. Matriz de trazabilidad (versión v2.0)

Rutas relativas a la raíz del ZIP. "CA" son los criterios de aceptación de la guía. Los resultados de la última ejecución están en `evidencias/registro_pruebas.txt` y `evidencias/rnf_resultados.txt`.

| Req. | Nec. | Modelos | Componente / archivo | Evidencia de verificación |
|---|---|---|---|---|
| RF01 | N01 | A1, A2 CU07, A6 | `jugar.py`, `motor/cargador.py::cargar_historia` | `tests/test_i1_integracion.py::test_i1_archivo_real_hasta_cada_final`; `tests/test_rnf.py::test_rnf01_*` (carga `el_faro.json`); `evidencias/recorridos/segunda_historia.txt` |
| RF02 | N01 | A3 `Historia`, A5 `Validando→EnCurso` | `motor/sesion.py::Sesion.reiniciar` (usado por `__init__`) | `tests/test_motor.py::test_u5_*` (estado inicial), `test_i1_archivo_real_hasta_cada_final` |
| RF03 | N02 | A4 | `interfaz/consola.py::Consola.mostrar_escena` | `tests/test_i1_integracion.py::test_i1_consola_completa_*`; `evidencias/recorridos/final_E4.txt` |
| RF04 | N02 | A3 `Opcion.habilitada`, A4 | `motor/modelo.py::Opcion.habilitada`, `motor/sesion.py::opciones_disponibles` | `tests/test_motor.py::test_u1_*` (CA01, conjuntos exactos) |
| RF05 | N03 | A4 rama `alt`, A5 | `motor/sesion.py::elegir`, `_aplicar` | `tests/test_motor.py::test_u2_*` (6 caminos) |
| RF06 | N03 | A4 rama `else`, A5 "entrada inválida" | `motor/sesion.py::_opcion_habilitada` | `tests/test_motor.py::test_u3_*` (CA02 incluido) |
| RF07 | N03 | A4, A5 | `interfaz/consola.py::procesar`, `_traducir_opcion` | `tests/test_i1_integracion.py::test_i1_consola_completa_*`; `tests/test_rnf.py::test_rnf03_*` |
| RF08 | N04 | A3 `Sesion.variables`, A5 | `motor/sesion.py` (`_variables`) | `tests/test_motor.py::test_u1_condiciones_habilitan_*`, `test_u2_*` |
| RF09 | N05 | A2 CU05, A5 `Finalizada` | `motor/sesion.py::terminada`, `interfaz/consola.py::mostrar_escena` | `tests/test_i1_integracion.py` (3 finales); `evidencias/recorridos/final_E4.txt`, `final_E5.txt`, `final_E6.txt` |
| RF10 | N05 | A2 CU04, A5 "reiniciar" | `motor/sesion.py::reiniciar` | `tests/test_motor.py::test_u5_*` |
| RF11 | N06 | A2 CU01, A5 `Rechazada` | `motor/cargador.py`, `motor/validador.py::validar` | `tests/test_u4_validacion.py` (CA03 `destino_inexistente.json`) |
| RF12 | N06 | A3 `Problema`, `ErrorContenido` | `motor/errores.py`, `motor/validador.py` | `tests/test_u4_validacion.py` (11 archivos + 5 variantes); `tests/test_rnf.py::test_rnf02_*` |
| RF13 | N06 | A1, A2 CU01 | `jugar.py` (`--validar`) | `tests/test_rnf.py::test_rnf02_*` (proceso externo, código 1); `evidencias/recorridos/error_destino_E99.txt` |
| RF14 | N06 | A5 `Bloqueada` | `motor/sesion.py::bloqueada`, `interfaz/consola.py::mostrar_escena` | `tests/test_motor.py::test_bloqueo_en_partida_*`; `evidencias/recorridos/bloqueo.txt` |
| RF15 | N07 (SC01) | A2 CU06, A3 `EstadoSesion`, A4, A5 "deshacer" | `motor/sesion.py::deshacer`, `_instantanea` | `tests/test_cambio_deshacer.py::test_u6_deshacer_restaura_*`; `tests/test_i1_integracion.py::test_i1_deshacer_desde_un_final_*`; `evidencias/recorridos/deshacer.txt` |
| RF16 | N07 (SC01) | A3 `puede_deshacer`, A5 guarda `[hay anterior]` | `motor/sesion.py::deshacer`, `puede_deshacer` | `tests/test_cambio_deshacer.py::test_u6_al_comenzar_*`, `test_u6_variante_solo_un_nivel`, `test_u6_variante_nueva_eleccion_*` |
| RF17 | N07 (SC01) | A4 rama `else`, A5 "reiniciar / borra historial" | `motor/sesion.py::elegir`, `reiniciar` | `tests/test_cambio_deshacer.py::test_u6_variante_entrada_invalida_*`; `tests/test_motor.py::test_u5_reiniciar_elimina_historial` |
| RNF01 | N01 | A6 (regla de dependencia) | `historias/el_faro.json`; `motor/` sin IDs de historias | `tests/test_rnf.py::test_rnf01_*`; `scripts/verificar_rnf.py`; `evidencias/rnf_resultados.txt`; `git log --stat` del commit de la segunda historia (`evidencias/historial_git.txt`) |
| RNF02 | N06 | A3 `Problema` | `motor/validador.py`, `jugar.py` | `tests/test_rnf.py::test_rnf02_*`; `evidencias/rnf_resultados.txt` |
| RNF03 | N03 | A5 "entrada inválida / sin cambios" | `interfaz/consola.py`, `motor/sesion.py` | `tests/test_rnf.py::test_rnf03_*` (incluye regresión `'²'`); `evidencias/rnf_resultados.txt` |
