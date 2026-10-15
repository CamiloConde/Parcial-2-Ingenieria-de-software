# Verificación manual paso a paso

Lista de comprobación para confirmar a mano que el programa funciona como exigen la guía y la solicitud de cambio. Complementa las pruebas automatizadas, pero no las reemplaza. Marque cada casilla al obtener el resultado esperado.

Ejecute los comandos desde la carpeta del proyecto. En Windows use `python` (o `py`); en Linux o macOS, `python3` si `python` no existe. Para ver las variables, todas las partidas usan `--depurar`.

---

## 0. Preparación

| # | Acción | Resultado esperado | ✓ |
|---|---|---|---|
| 0.1 | `python --version` | 3.10 o superior | ☐ |
| 0.2 | `python -m pip install -r requirements.txt` | Instala pytest sin errores | ☐ |
| 0.3 | `python -m pytest` | Última línea: `70 passed` | ☐ |
| 0.4 | `python scripts/verificar_rnf.py` | Última línea: `RESULTADO GLOBAL: CUMPLE` | ☐ |

## 1. Inicio de partida (N01, N02)

Comando: `python jugar.py historias/la_ultima_transmision.json --depurar`

| # | Entrada | Resultado esperado | ✓ |
|---|---|---|---|
| 1.1 | (ninguna) | Título "La última transmisión", escena `[E1]` "Son las 02:13…", estado `conoce_origen=falso, confia_en_la_voz=falso`, una opción: `1. Revisar señal` | ☐ |
| 1.2 | (ninguna) | La línea de comandos **no** muestra `d = deshacer` (al comenzar no hay retroceso) | ☐ |

## 2. Los tres finales (N03, N05)

Siga en la misma partida. Antes de cada recorrido escriba `r` para reiniciar.

| # | Entradas | Resultado esperado | ✓ |
|---|---|---|---|
| 2.1 | `1`, `1`, `1` | `[E4]` "…guía a un equipo de rescate…", `*** FIN — desenlace E4 ***`, ambas variables en `verdadero` | ☐ |
| 2.2 | `r`, `1`, `2`, `1` | `[E5]` "…mensaje automático antiguo…", `*** FIN — desenlace E5 ***`, `conoce_origen=falso`, `confia_en_la_voz=verdadero` | ☐ |
| 2.3 | `r`, `1`, `2`, `2` | `[E6]` "…interrumpe la comunicación…", `*** FIN — desenlace E6 ***` | ☐ |
| 2.4 | En un final, escribir `1` | `Entrada no válida: '1'`. Sigue en el final, sin opciones de avance | ☐ |

## 3. Una condición cambia las opciones (N02, N04, CA01, CA02)

| # | Entradas | Resultado esperado | ✓ |
|---|---|---|---|
| 3.1 | `r`, `1`, `1` (investigar) | En `[E3]`, exactamente: `1. Activar con código` y `2. Cortar comunicación`; `conoce_origen=verdadero` | ☐ |
| 3.2 | `r`, `1`, `2` (continuar) | En `[E3]`, exactamente: `1. Activar sin verificar` y `2. Cortar comunicación`; `conoce_origen=falso` | ☐ |
| 3.3 | En la situación 3.2, escribir `activar_codigo` | `La opción 'activar_codigo' no está habilitada con lo ocurrido hasta ahora.` Sigue en `E3` con las mismas variables (CA02) | ☐ |

## 4. Entradas inválidas no alteran la partida (N03, RNF03)

| # | Entrada (en cualquier escena no final) | Resultado esperado | ✓ |
|---|---|---|---|
| 4.1 | `9` | `Entrada no válida: '9'…`; misma escena y variables | ☐ |
| 4.2 | `abc` | `La opción 'abc' no existe en esta escena.`; sin cambios | ☐ |
| 4.3 | (Enter vacío) | `Entrada no válida: ''…`; sin cambios | ☐ |
| 4.4 | `²` o `-1` | `La opción '²' no existe en esta escena.` (o `'-1'`); el programa **no** se cierra | ☐ |

## 5. Reiniciar (N05, U5)

| # | Entradas | Resultado esperado | ✓ |
|---|---|---|---|
| 5.1 | `1`, `1`, `1` (llegar a E4) y luego `r` | `Partida reiniciada.`, `[E1]` con ambas variables en `falso` | ☐ |
| 5.2 | Justo después de 5.1, `d` | `No hay una decisión para deshacer.` (reiniciar borra el historial) | ☐ |

## 6. Deshacer: solicitud de cambio SC01 (RF15-RF17)

Ejemplo del anexo de la hora 6. Escriba `r` antes de empezar.

| # | Entradas | Resultado esperado | ✓ |
|---|---|---|---|
| 6.1 | `1`, `1` | `[E3]` con `conoce_origen=verdadero` y la ayuda muestra `d = deshacer` | ☐ |
| 6.2 | `d` | `Se deshizo la última decisión.` → `[E2]` con `conoce_origen=falso` | ☐ |
| 6.3 | `d` otra vez | `No hay una decisión para deshacer.`; sigue en `E2` (un solo nivel) | ☐ |
| 6.4 | `2` (continuar) | `[E3]` muestra `Activar sin verificar` y `Cortar comunicación`; `d` vuelve a estar disponible | ☐ |
| 6.5 | `2` (cortar → E6) y luego `d` | Regresa a `[E3]` con los valores previos (`conoce_origen=falso`, `confia_en_la_voz=falso`): deshacer desde un final | ☐ |
| 6.6 | `r`, `1`, `1` (E3), luego `activar_sin_verificar` (no habilitada) y luego `d` | Rechaza la opción; después `d` regresa a `[E2]` con `conoce_origen=falso`: la entrada inválida no reemplazó el historial | ☐ |
| 6.7 | `s` | `Hasta pronto.` | ☐ |

## 7. Segunda historia con el mismo motor (RNF01)

Comando: `python jugar.py historias/el_faro.json --depurar`

| # | Entradas | Resultado esperado | ✓ |
|---|---|---|---|
| 7.1 | (ninguna) | Título "El faro de Punta Gris", `[F1]`, `tiene_llave=falso` | ☐ |
| 7.2 | `1` (cobertizo) | `[F2]` con `tiene_llave=verdadero` y la opción "Abrir el candado con la llave oxidada" | ☐ |
| 7.3 | `1` | `*** FIN — desenlace F3 ***` | ☐ |
| 7.4 | `r`, `2` (correr) | `[F2]` **sin** la opción de abrir: solo "Refugiarse en el portal…" | ☐ |
| 7.5 | `1`, `s` | `*** FIN — desenlace F4 ***` y salida | ☐ |

## 8. Validación de archivos (N06, CA03)

| # | Comando | Resultado esperado | ✓ |
|---|---|---|---|
| 8.1 | `python jugar.py --validar historias/la_ultima_transmision.json` | `…es válida: 6 escenas, 3 finales.` | ☐ |
| 8.2 | `python jugar.py --validar historias/invalidas/destino_inexistente.json` | `[DESTINO_INEXISTENTE] El destino 'E99' no corresponde a ninguna escena. (en escenas[E3].opciones[cortar].destino)` y "No se abrió ninguna partida" | ☐ |
| 8.3 | `python jugar.py historias/invalidas/destino_inexistente.json` (intentar jugar) | Mismo error; **no** se muestra ninguna escena | ☐ |
| 8.4 | Repetir 8.2 con cada archivo de `historias/invalidas/` | Cada uno muestra su categoría entre corchetes y el ID o campo; ninguno muestra `Traceback` | ☐ |
| 8.5 | `python jugar.py --validar no_existe.json` | `[ARCHIVO_ILEGIBLE] No existe el archivo.` | ☐ |

Categorías esperadas en 8.4: `archivo_ilegible` → ARCHIVO_ILEGIBLE · `campo_faltante` → CAMPO_FALTANTE · `escena_duplicada` → ESCENA_DUPLICADA · `estructura_incorrecta` → ESTRUCTURA_INCORRECTA · `final_con_opciones` → FINAL_CON_OPCIONES · `inicio_inexistente` → INICIO_INEXISTENTE · `no_final_sin_opciones` → NO_FINAL_SIN_OPCIONES · `opcion_duplicada` → OPCION_DUPLICADA · `valor_no_booleano` → VALOR_NO_BOOLEANO · `variable_no_declarada` → VARIABLE_NO_DECLARADA.

## 9. Bloqueo durante la partida (RF14)

Comando: `python jugar.py historias/pruebas/bloqueo_en_partida.json`

| # | Entradas | Resultado esperado | ✓ |
|---|---|---|---|
| 9.1 | `1`, `2` | `!!! BLOQUEO: ninguna opción está habilitada…` y comandos `d`, `r`, `s` | ☐ |
| 9.2 | `r` | Vuelve a `[E1]` | ☐ |

## 10. Prueba de modificabilidad hecha a mano (opcional, RNF01)

1. Copie `historias/el_faro.json` como `historias/mi_prueba.json`.
2. En la copia, cambie el texto de `F1`, agregue una escena final `F5` (`"final": true, "opciones": []`) y, en `F2`, una opción con `"destino": "F5"`.
3. `python jugar.py historias/mi_prueba.json` → la nueva opción aparece y lleva a `F5`, **sin tocar ningún archivo `.py`**.
4. Cambie `"destino": "F5"` por `"F9"` y valide: debe aparecer `[DESTINO_INEXISTENTE]` con `F9`.
5. Borre `historias/mi_prueba.json` al terminar.
