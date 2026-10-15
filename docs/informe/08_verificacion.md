## 8. Verificación y resultados

**Pruebas automatizadas** (`python -m pytest -v`). La última ejecución da **70 pruebas aprobadas y 0 fallidas** (`evidencias/registro_pruebas.txt`). La versión `v1.0` tenía 54 pruebas aprobadas (`evidencias/registro_pruebas_v1.0.txt`). Cada caso declara entradas, resultado esperado y aserciones; las variantes se agrupan con `pytest.mark.parametrize`.

| Escenario | Archivo / prueba | Variantes |
|---|---|---|
| U1 Condiciones cumplidas y no cumplidas | `tests/test_motor.py::test_u1_*` | 2 de `E3` + 5 de evaluación |
| U2 Elección válida: efectos y destino | `tests/test_motor.py::test_u2_*` | 6 caminos (incluye CA01) |
| U3 Opción inexistente o no habilitada | `tests/test_motor.py::test_u3_*` | 7 (incluye CA02 y elección desde un final) |
| U4 Errores de contenido | `tests/test_u4_validacion.py` | 11 archivos + 2 de lectura + 5 en memoria + acumulación |
| U5 Reiniciar (extendida por SC01) | `tests/test_motor.py::test_u5_*` | 5 de restauración + 3 de borrado de historial |
| U6 Deshacer (SC01) | `tests/test_cambio_deshacer.py` | Restaura y consume; inicio; entrada inválida ×4; nueva elección; un nivel; efecto idempotente |
| I1 Archivo real + motor (extendida por SC01) | `tests/test_i1_integracion.py` | 3 finales; deshacer desde los 3 finales; consola completa; consola con deshacer |

**Cobertura de validación.** Hay un caso por cada categoría exigida: archivo ilegible o estructura incorrecta, campos obligatorios ausentes, inicio inexistente, escenas u opciones duplicadas, destino inexistente, variable no declarada, valor no booleano y cantidad de opciones incompatible con el carácter final. Además se cubre el **bloqueo durante la partida** (`test_bloqueo_en_partida_*` y `evidencias/recorridos/bloqueo.txt`). El mensaje de CA03 es: `[DESTINO_INEXISTENTE] El destino 'E99' no corresponde a ninguna escena. (en escenas[E3].opciones[cortar].destino)`.

**Verificación de RNF** (`python scripts/verificar_rnf.py`; resultados reales en `evidencias/rnf_resultados.txt`).

| RNF | Meta | Resultado medido |
|---|---|---|
| RNF01 Modificabilidad | 0 líneas de código modificadas para historias nuevas | **0**. Hash SHA-256 de `motor/` e `interfaz/` idéntico antes y después. `el_faro.json` alcanza sus 2 finales (`F3`, `F4`) y la escena `E7` agregada por el script es jugable. El commit de la segunda historia solo modificó `historias/el_faro.json`. |
| RNF02 Claridad de errores | 100 % con categoría, ID y sin `Traceback` | **11/11 = 100 %**, con código de salida 1 en todos |
| RNF03 Confiabilidad | 0 excepciones y 0 alteraciones con 1000 entradas | Referencia: 1000 entradas, 871 rechazadas, **0 excepciones, 0 alteraciones**. `el_faro.json`: 1000 entradas, 855 rechazadas, **0 y 0** |

**Defecto encontrado por la verificación.** En la primera ejecución de RNF03, la entrada `'²'` cerraba la consola: `'²'.isdigit()` es verdadero en Python, pero `int('²')` lanza `ValueError`. Se corrigió en `interfaz/consola.py` (se exige `isascii()`) y se agregó una prueba de regresión (`test_rnf03_regresion_digitos_unicode_*`).

**Verificación del producto.** Los recorridos reales están en `evidencias/recorridos/`. Incluyen los tres finales (`final_E4.txt`, `final_E5.txt`, `final_E6.txt`), cómo una condición cambia las opciones (`condicion_cambia_opciones.txt`), entradas inválidas, reinicio, deshacer, la segunda historia, el bloqueo y el error `E99`. La suite también se ejecutó en un segundo equipo, Windows con Python 3.12: 70 pruebas aprobadas y RNF cumplidos (`evidencias/ejecucion_segundo_equipo.txt`). La lista de comprobación manual paso a paso está en `docs/verificacion_manual.md`.

**Fallos pendientes y limitaciones declaradas.** No hay pruebas fallidas. Limitaciones: (1) la descripción técnica del JSON mal formado la genera Python en inglés, aunque la categoría, la línea y la columna están en español; (2) no se analizan todos los caminos del relato antes de jugar, por lo que un bloqueo se informa cuando ocurre (la guía no lo exige); (3) deshacer es de un nivel y sin rehacer, como pide SC01.
