"""Punto de entrada del programa.

Uso:
    python jugar.py historias/la_ultima_transmision.json
    python jugar.py historias/el_faro.json --depurar
    python jugar.py --validar historias/invalidas/destino_inexistente.json
"""

import argparse
import sys

from interfaz.consola import Consola
from motor.cargador import cargar_historia
from motor.errores import ErrorContenido
from motor.sesion import Sesion


def _configurar_utf8() -> None:
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main(argumentos: list[str] | None = None) -> int:
    _configurar_utf8()
    parser = argparse.ArgumentParser(description="Motor de historias interactivas.")
    parser.add_argument("ruta", help="archivo JSON de la historia")
    parser.add_argument("--validar", action="store_true", help="solo valida el archivo, sin jugar")
    parser.add_argument("--depurar", action="store_true", help="muestra el valor de las variables")
    args = parser.parse_args(argumentos)

    try:
        historia = cargar_historia(args.ruta)
    except ErrorContenido as error:
        print(error.descripcion(), file=sys.stderr)
        print("Corrija el archivo y vuelva a intentarlo. No se abrió ninguna partida.", file=sys.stderr)
        return 1

    if args.validar:
        finales = sum(1 for e in historia.escenas.values() if e.final)
        print(f"La historia '{historia.titulo}' es válida: {len(historia.escenas)} escenas, {finales} finales.")
        return 0

    Consola(Sesion(historia), depurar=args.depurar).ejecutar()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:  # último recurso: nunca mostrar una traza al lector
        print(f"Error inesperado del programa: {error}. Informe este mensaje al equipo.", file=sys.stderr)
        sys.exit(2)
