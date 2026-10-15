# La última transmisión: motor de historias interactivas

Parcial práctico de Ingeniería de Software. El programa de consola interpreta historias interactivas escritas en archivos JSON. Muestra solo las decisiones habilitadas por lo ocurrido, aplica sus consecuencias y valida el archivo antes de jugarlo.

## Integrantes

| Nombre | Código |
|---|---|
| Camilo Conde Corrales | T00078909 |
| Miguel Jacome y Yanez | T00078937 |

## Documentos de la entrega

| Documento | Ruta |
|---|---|
| Informe (8 páginas como máximo) | `docs/Informe.pdf` |
| Anexo: diagramas, matriz de trazabilidad y tablero | `docs/Anexo.pdf` |
| Video de demostración (MP4, 6 minutos como máximo) | **ENLACE_VIDEO_PENDIENTE** |
| Guion del video | `docs/guion_demostracion.md` |
| Comprobación manual paso a paso | `docs/verificacion_manual.md` |
| Resultados de pruebas, RNF, recorridos e historial de Git | `evidencias/` |

Las fuentes del informe y del anexo están en `docs/informe/` y `docs/anexo/` (Markdown con diagramas Mermaid).

## Versiones requeridas

| Herramienta | Versión | Uso |
|---|---|---|
| Python | 3.10 o superior (probado con 3.13) | Ejecutar el programa. Solo usa la biblioteca estándar |
| pytest | 8.0 o superior (probado con 9.1) | Solo para ejecutar las pruebas automatizadas |

## Instalación

```bash
# 1. Descomprimir el ZIP (o clonar el repositorio) y entrar a la carpeta
cd Parcial-2-Ingenieria-de-software

# 2. (Opcional) crear un entorno virtual
python -m venv .venv
# Windows:      .venv\Scripts\activate
# Linux/macOS:  source .venv/bin/activate

# 3. Instalar la dependencia de pruebas
python -m pip install -r requirements.txt
```

En Linux o macOS puede ser necesario escribir `python3` en lugar de `python`.

## Ejecución

```bash
# Jugar la historia de referencia
python jugar.py historias/la_ultima_transmision.json

# Jugar mostrando el valor de las variables (útil para la demostración)
python jugar.py historias/la_ultima_transmision.json --depurar

# Jugar la segunda historia con el mismo motor
python jugar.py historias/el_faro.json

# Validar un archivo sin jugarlo (código de salida 0 = válido, 1 = inválido)
python jugar.py --validar historias/la_ultima_transmision.json
python jugar.py --validar historias/invalidas/destino_inexistente.json
```

**Comandos durante la partida**

| Escribir | Efecto |
|---|---|
| `1`, `2`, … | Elegir la opción con ese número |
| ID de una opción (p. ej. `investigar`) | Elegir esa opción si existe y está habilitada |
| `d` | Deshacer la última decisión (un solo nivel; también desde un final) |
| `r` | Reiniciar la partida (escena y variables iniciales; borra el historial) |
| `s` | Salir |

## Rutas para demostrar cada final

| Final | Entradas desde el inicio | Opciones elegidas | Variables al final |
|---|---|---|---|
| **E4 Rescate** | `1`, `1`, `1` | Revisar señal → Investigar archivo → Activar con código | `conoce_origen = verdadero`, `confia_en_la_voz = verdadero` |
| **E5 El eco** | `1`, `2`, `1` | Revisar señal → Continuar sin investigar → Activar sin verificar | `conoce_origen = falso`, `confia_en_la_voz = verdadero` |
| **E6 Silencio** | `1`, `2`, `2` (o `1`, `1`, `2`) | Revisar señal → (cualquiera) → Cortar comunicación | `confia_en_la_voz = falso` |

**Deshacer (solicitud de cambio):** en cualquier final escribir `d` regresa a `E3` con los valores anteriores a esa elección. Un segundo `d` no hace nada hasta realizar una nueva elección. Ejemplo: `1`, `1`, `d` → vuelve a `E2` con `conoce_origen = falso`; luego `2` → `E3` muestra "Activar sin verificar".

**Cómo una condición cambia las opciones:** en `E3`, si se investigó el archivo aparece "Activar con código"; si no, aparece "Activar sin verificar". "Cortar comunicación" aparece siempre.

**Segunda historia (`el_faro.json`):** `1`, `1` llega a **F3** (la llave del cobertizo habilita "Abrir el candado con la llave oxidada"); `2`, `1` llega a **F4** (sin llave solo se puede esperar).

## Pruebas

```bash
python -m pytest -v                  # todas las pruebas automatizadas
python scripts/verificar_rnf.py      # verificación de RNF01, RNF02 y RNF03
python scripts/generar_evidencias.py # regenera evidencias/ (pruebas, RNF, recorridos, historial)
```

| Escenario | Archivo |
|---|---|
| U1 Condiciones que habilitan opciones | `tests/test_motor.py::test_u1_*` |
| U2 Elección válida: efectos y destino | `tests/test_motor.py::test_u2_*` |
| U3 Opción inexistente o no habilitada | `tests/test_motor.py::test_u3_*` |
| U4 Errores de contenido (parametrizada) | `tests/test_u4_validacion.py` |
| U5 Reiniciar | `tests/test_motor.py::test_u5_*` |
| U6 Deshacer (solicitud de cambio) | `tests/test_cambio_deshacer.py` |
| I1 Archivo real + motor hasta un final | `tests/test_i1_integracion.py` |
| RNF01-RNF03 | `tests/test_rnf.py`, `scripts/verificar_rnf.py` |

Los resultados de la última ejecución están en `evidencias/`.

## Formato de contenido

Se usa el contrato JSON de referencia de la guía, sin cambios.

```json
{
  "titulo": "Texto del título",
  "inicio": "ID de la escena inicial",
  "variables": { "nombre_variable": false },
  "escenas": [
    {
      "id": "E1",
      "texto": "Texto visible de la escena",
      "final": false,
      "opciones": [
        {
          "id": "id_unico_en_la_escena",
          "texto": "Etiqueta visible",
          "destino": "ID de una escena existente",
          "condiciones": { "nombre_variable": true },
          "efectos": { "nombre_variable": false }
        }
      ]
    }
  ]
}
```

**Reglas**

- Una opción se muestra solo si **todas** sus `condiciones` se cumplen. Un mapa vacío `{}` la habilita siempre.
- Al elegir una opción se asignan sus `efectos` y se pasa a `destino`. Un mapa de efectos vacío conserva las variables.
- Las escenas con `"final": true` deben tener `"opciones": []`; las no finales, al menos una opción.
- Condiciones y efectos solo pueden usar variables declaradas en `variables` y valores `true` o `false`.

**Errores que se detectan antes de jugar** (cada mensaje indica la categoría entre corchetes y el lugar exacto, por ejemplo `escenas[E3].opciones[cortar].destino`):

| Categoría | Ejemplo en `historias/invalidas/` |
|---|---|
| `ARCHIVO_ILEGIBLE` | `archivo_ilegible.json` (JSON mal formado, archivo inexistente o no UTF-8) |
| `ESTRUCTURA_INCORRECTA` | `estructura_incorrecta.json` (tipo de campo incorrecto) |
| `CAMPO_FALTANTE` | `campo_faltante.json` |
| `INICIO_INEXISTENTE` | `inicio_inexistente.json` |
| `ESCENA_DUPLICADA` / `OPCION_DUPLICADA` | `escena_duplicada.json`, `opcion_duplicada.json` |
| `DESTINO_INEXISTENTE` | `destino_inexistente.json` (destino `E99`) |
| `VARIABLE_NO_DECLARADA` | `variable_no_declarada.json` |
| `VALOR_NO_BOOLEANO` | `valor_no_booleano.json` |
| `FINAL_CON_OPCIONES` / `NO_FINAL_SIN_OPCIONES` | `final_con_opciones.json`, `no_final_sin_opciones.json` |

Si durante una partida una escena no final se queda sin opciones habilitadas, el programa muestra `BLOQUEO` y permite reiniciar o salir. Ejemplo: `python jugar.py historias/pruebas/bloqueo_en_partida.json`, entradas `1`, `2`.

## Versiones

| Tag | Descripción |
|---|---|
| `v1.0` | Versión disponible al recibir la solicitud de cambio (sin retroceso) |
| `v2.0` | Versión final con deshacer la última decisión (SC01) |

## Estructura del proyecto

```
jugar.py                 punto de entrada (argumentos, manejo de errores)
interfaz/consola.py      capa de interfaz: muestra escenas y lee comandos
motor/sesion.py          capa de reglas: estado, condiciones, efectos, reinicio, deshacer
motor/modelo.py          capa de contenido: Historia, Escena, Opcion (inmutables)
motor/cargador.py        lectura del archivo y construcción del modelo
motor/validador.py       reglas del contrato de contenido
motor/errores.py         Problema y ErrorContenido
historias/               historias jugables, inválidas (pruebas) y de bloqueo
tests/                   pruebas automatizadas (pytest)
scripts/                 verificación de RNF y generación de evidencias
docs/                    fuentes del informe y del anexo
evidencias/              registros de ejecución, historial de Git, recorridos
```

## Bibliotecas y licencias

| Biblioteca | Licencia | Uso |
|---|---|---|
| Biblioteca estándar de Python (`json`, `dataclasses`, `argparse`, `pathlib`, `hashlib`, `random`, `subprocess`) | PSF License | Programa y scripts |
| pytest | MIT | Pruebas automatizadas (solo desarrollo) |
| Mermaid, PlantUML (MIT) y Graphviz (EPL) | MIT / EPL | Solo para dibujar los diagramas del anexo (`docs/anexo/`); no se necesitan para ejecutar |

## Limitaciones conocidas

- Deshacer es de un solo nivel y no existe "rehacer", tal como define la solicitud de cambio.
- Solo hay interfaz de consola; no hay guardado entre ejecuciones (está fuera del alcance).
- No se analizan automáticamente todos los caminos del relato. Los bloqueos se informan cuando ocurren durante la partida.
- Los mensajes de JSON mal formado incluyen la descripción técnica en inglés que entrega Python (por ejemplo, `Illegal trailing comma`). La línea, la columna y la categoría sí se muestran en español.
