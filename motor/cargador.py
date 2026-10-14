"""Lectura de archivos de historia y construcción del modelo validado."""

import json
from pathlib import Path

from motor import errores as E
from motor.errores import ErrorContenido, Problema
from motor.modelo import Historia, historia_desde_datos
from motor.validador import validar


def leer_archivo(ruta: str | Path):
    """Lee un archivo JSON. Cualquier fallo de lectura se convierte en ErrorContenido."""
    ruta = Path(ruta)
    try:
        with ruta.open(encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        causa = "No existe el archivo."
    except IsADirectoryError:
        causa = "La ruta corresponde a una carpeta, no a un archivo."
    except UnicodeDecodeError:
        causa = "El archivo no está codificado en UTF-8."
    except json.JSONDecodeError as error:
        causa = f"JSON mal formado: {error.msg} (línea {error.lineno}, columna {error.colno})."
    except OSError as error:
        causa = f"No se pudo leer el archivo: {error.strerror or error}."
    raise ErrorContenido([Problema(E.ARCHIVO_ILEGIBLE, causa, str(ruta))])


def historia_desde_dict(datos) -> Historia:
    """Valida un documento ya leído y construye la Historia, o lanza ErrorContenido."""
    problemas = validar(datos)
    if problemas:
        raise ErrorContenido(problemas)
    return historia_desde_datos(datos)


def cargar_historia(ruta: str | Path) -> Historia:
    """Lee, valida y construye una historia. No devuelve nada jugable si hay errores."""
    return historia_desde_dict(leer_archivo(ruta))
