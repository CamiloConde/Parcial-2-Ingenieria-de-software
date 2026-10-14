"""Validación del contrato de contenido antes de abrir una sesión.

`validar` recorre todo el documento y acumula los problemas encontrados en
lugar de detenerse en el primero (ver ADR-02). No conoce ninguna historia
concreta: solo aplica las reglas del contrato descrito en el README.
"""

from motor import errores as E
from motor.errores import Problema

_TIPOS = {str: "texto", bool: "booleano (true o false)", dict: "objeto {…}", list: "lista […]"}

_CAMPOS_HISTORIA = (("titulo", str), ("inicio", str), ("variables", dict), ("escenas", list))
_CAMPOS_ESCENA = (("id", str), ("texto", str), ("final", bool), ("opciones", list))
_CAMPOS_OPCION = (
    ("id", str),
    ("texto", str),
    ("destino", str),
    ("condiciones", dict),
    ("efectos", dict),
)


def _resumen(valor, largo: int = 60) -> str:
    """Representación corta de un valor para no inundar el mensaje de error."""
    texto = repr(valor)
    return texto if len(texto) <= largo else texto[: largo - 1] + "…"


def _es_booleano(valor) -> bool:
    return isinstance(valor, bool)


def _revisar_campos(objeto: dict, campos, ubicacion: str, problemas: list) -> dict:
    """Comprueba presencia y tipo de los campos; devuelve solo los campos correctos."""
    correctos = {}
    for nombre, tipo in campos:
        lugar = f"{ubicacion}.{nombre}" if ubicacion else nombre
        if nombre not in objeto:
            problemas.append(Problema(E.CAMPO_FALTANTE, f"Falta el campo obligatorio '{nombre}'.", ubicacion or "raíz"))
            continue
        valor = objeto[nombre]
        valido = _es_booleano(valor) if tipo is bool else isinstance(valor, tipo)
        if not valido:
            categoria = E.VALOR_NO_BOOLEANO if tipo is bool else E.ESTRUCTURA_INCORRECTA
            problemas.append(
                Problema(categoria, f"El campo '{nombre}' debe ser {_TIPOS[tipo]}; se encontró {_resumen(valor)}.", lugar)
            )
            continue
        if tipo is str and not valor.strip():
            problemas.append(Problema(E.ESTRUCTURA_INCORRECTA, f"El campo '{nombre}' no puede estar vacío.", lugar))
            continue
        correctos[nombre] = valor
    return correctos


def _etiqueta(objeto: dict, coleccion: str, indice: int) -> str:
    """Ubicación legible: usa el ID del elemento si existe; si no, su posición."""
    ident = objeto.get("id")
    if isinstance(ident, str) and ident.strip():
        return f"{coleccion}[{ident}]"
    return f"{coleccion}[{indice}]"


def _revisar_mapa_booleano(mapa: dict, tipo_mapa: str, declaradas, ubicacion: str, problemas: list) -> None:
    for variable, valor in mapa.items():
        lugar = f"{ubicacion}.{variable}"
        if declaradas is not None and variable not in declaradas:
            problemas.append(
                Problema(
                    E.VARIABLE_NO_DECLARADA,
                    f"La variable '{variable}' usada en {tipo_mapa} no está declarada en 'variables'.",
                    lugar,
                )
            )
        if not _es_booleano(valor):
            problemas.append(
                Problema(
                    E.VALOR_NO_BOOLEANO,
                    f"El valor de '{variable}' en {tipo_mapa} debe ser true o false; se encontró {_resumen(valor)}.",
                    lugar,
                )
            )


def validar(datos) -> list[Problema]:
    """Devuelve la lista de problemas del documento. Lista vacía = historia válida."""
    problemas: list[Problema] = []
    if not isinstance(datos, dict):
        problemas.append(
            Problema(
                E.ESTRUCTURA_INCORRECTA,
                "El archivo debe contener un objeto JSON con 'titulo', 'inicio', 'variables' y 'escenas'.",
                "raíz",
            )
        )
        return problemas

    historia = _revisar_campos(datos, _CAMPOS_HISTORIA, "", problemas)

    declaradas = None
    if "variables" in historia:
        declaradas = set(historia["variables"])
        for variable, valor in historia["variables"].items():
            if not _es_booleano(valor):
                problemas.append(
                    Problema(
                        E.VALOR_NO_BOOLEANO,
                        f"El valor inicial de '{variable}' debe ser true o false; se encontró {_resumen(valor)}.",
                        f"variables.{variable}",
                    )
                )

    ids_escenas: set[str] = set()
    destinos: list[tuple[str, str]] = []  # (destino, ubicación)
    for indice, escena in enumerate(historia.get("escenas", [])):
        ubicacion = f"escenas[{indice}]"
        if not isinstance(escena, dict):
            problemas.append(Problema(E.ESTRUCTURA_INCORRECTA, "Cada escena debe ser un objeto JSON.", ubicacion))
            continue
        ubicacion = _etiqueta(escena, "escenas", indice)
        campos = _revisar_campos(escena, _CAMPOS_ESCENA, ubicacion, problemas)
        if "id" in campos:
            if campos["id"] in ids_escenas:
                problemas.append(
                    Problema(E.ESCENA_DUPLICADA, f"El ID de escena '{campos['id']}' está repetido.", ubicacion)
                )
            ids_escenas.add(campos["id"])

        opciones = campos.get("opciones")
        if opciones is not None and "final" in campos:
            if campos["final"] and opciones:
                problemas.append(
                    Problema(
                        E.FINAL_CON_OPCIONES,
                        f"Una escena final debe tener 0 opciones; tiene {len(opciones)}.",
                        ubicacion,
                    )
                )
            if not campos["final"] and not opciones:
                problemas.append(
                    Problema(E.NO_FINAL_SIN_OPCIONES, "Una escena no final debe tener al menos una opción.", ubicacion)
                )

        ids_opciones: set[str] = set()
        for indice_op, opcion in enumerate(opciones or []):
            lugar_op = f"{ubicacion}.opciones[{indice_op}]"
            if not isinstance(opcion, dict):
                problemas.append(Problema(E.ESTRUCTURA_INCORRECTA, "Cada opción debe ser un objeto JSON.", lugar_op))
                continue
            lugar_op = f"{ubicacion}.{_etiqueta(opcion, 'opciones', indice_op)}"
            campos_op = _revisar_campos(opcion, _CAMPOS_OPCION, lugar_op, problemas)
            if "id" in campos_op:
                if campos_op["id"] in ids_opciones:
                    problemas.append(
                        Problema(
                            E.OPCION_DUPLICADA,
                            f"El ID de opción '{campos_op['id']}' está repetido dentro de la escena.",
                            lugar_op,
                        )
                    )
                ids_opciones.add(campos_op["id"])
            if "destino" in campos_op:
                destinos.append((campos_op["destino"], f"{lugar_op}.destino"))
            if "condiciones" in campos_op:
                _revisar_mapa_booleano(
                    campos_op["condiciones"], "condiciones", declaradas, f"{lugar_op}.condiciones", problemas
                )
            if "efectos" in campos_op:
                _revisar_mapa_booleano(campos_op["efectos"], "efectos", declaradas, f"{lugar_op}.efectos", problemas)

    if "escenas" in historia and not historia["escenas"]:
        problemas.append(Problema(E.ESTRUCTURA_INCORRECTA, "La historia debe tener al menos una escena.", "escenas"))

    for destino, lugar in destinos:
        if destino not in ids_escenas:
            problemas.append(
                Problema(E.DESTINO_INEXISTENTE, f"El destino '{destino}' no corresponde a ninguna escena.", lugar)
            )

    if "inicio" in historia and "escenas" in historia and historia["inicio"] not in ids_escenas:
        problemas.append(
            Problema(
                E.INICIO_INEXISTENTE,
                f"La escena inicial '{historia['inicio']}' no existe en 'escenas'.",
                "inicio",
            )
        )

    return problemas
