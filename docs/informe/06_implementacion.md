## 6. Implementación

**Tecnología.** Python 3.10+ con interfaz de consola. El programa usa solo la biblioteca estándar y las pruebas usan pytest. El código está versionado en Git; los tags `v1.0` y `v2.0` marcan las versiones anterior y posterior al cambio.

| Funcionalidad | Dónde se implementa |
|---|---|
| Carga desde archivo y construcción del modelo | `motor/cargador.py::cargar_historia`, `motor/modelo.py::historia_desde_datos` |
| Validación con las once categorías de error | `motor/validador.py::validar`, `motor/errores.py` |
| Opciones habilitadas, elección, estado, finales, bloqueo | `motor/sesion.py::Sesion` |
| Reinicio y deshacer | `Sesion.reiniciar`, `Sesion.deshacer` |
| Presentación, comandos y entradas inválidas | `interfaz/consola.py::Consola` |
| Argumentos, `--validar` y manejo de errores sin trazas | `jugar.py` |

**Decisión de diseño detallado: las operaciones devuelven `Resultado` en lugar de lanzar excepciones o imprimir.** `Sesion.elegir`, `deshacer` y `reiniciar` devuelven un objeto inmutable `Resultado(aceptada, mensaje)`. *Alternativas consideradas:* que el motor imprima directamente (acopla las reglas a la consola) o que lance excepciones ante una opción no habilitada (obliga a la interfaz a usar `try` para un caso normal de uso). *Consecuencias:* la sesión no depende de la interfaz, así que el mismo motor serviría para una interfaz web; las pruebas U3 y U6 verifican el rechazo con `assert resultado.aceptada is False` sin capturar salida; y una entrada inválida nunca interrumpe el flujo. Las excepciones se reservan para el contenido inválido (`ErrorContenido`), que sí impide abrir la sesión. Para reducir el acoplamiento también se tomaron otras dos medidas. Primera: `Consola` recibe por parámetro las funciones de entrada y salida, lo que permite que I1 y RNF03 la ejecuten con guiones. Segunda: el modelo es inmutable (`frozen=True` y `MappingProxyType`), de modo que `Sesion` es el único lugar donde cambia el estado y el deshacer pudo agregarse en un solo punto.

**Bibliotecas y licencias.** Biblioteca estándar de Python (PSF License): `json`, `dataclasses`, `types`, `argparse`, `pathlib`, `hashlib`, `random`, `subprocess`. pytest 8+ (MIT): pruebas, solo en desarrollo. Mermaid (MIT): solo para dibujar los diagramas del anexo; no forma parte del programa. Las versiones requeridas y los comandos de instalación y ejecución están en `README.md`.
