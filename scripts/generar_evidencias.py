"""Regenera la carpeta evidencias/ con resultados reales de ejecución.

Uso:  python scripts/generar_evidencias.py

Produce:
  evidencias/registro_pruebas.txt     salida de `python -m pytest -v`
  evidencias/rnf_resultados.txt       salida de `python scripts/verificar_rnf.py`
  evidencias/recorridos/*.txt         transcripciones de partidas y errores
  evidencias/historial_git.txt        historial de Git con autores, fechas y mensajes

Con --segundo-equipo solo escribe evidencias/ejecucion_segundo_equipo.txt
(pruebas y RNF ejecutados en el equipo de otro integrante).
"""

import os
import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from interfaz.consola import Consola  # noqa: E402
from motor.cargador import cargar_historia  # noqa: E402
from motor.sesion import Sesion  # noqa: E402

EVIDENCIAS = RAIZ / "evidencias"
RECORRIDOS = EVIDENCIAS / "recorridos"


def _limpiar(texto: str) -> str:
    """Quita rutas absolutas del equipo para que el registro sea legible y portable."""
    return texto.replace(str(RAIZ.parent) + "/", "").replace(str(RAIZ.parent) + "\\", "").replace(sys.executable, "python")


def _encabezado(comando: str) -> str:
    return (
        f"Fecha: {datetime.now().astimezone():%Y-%m-%d %H:%M %Z}\n"
        f"Commit: {_git('rev-parse', '--short', 'HEAD').strip() or 'sin git'}\n"
        f"Python: {platform.python_version()}  Sistema: {platform.system()}\n"
        f"Comando: {comando}\n\n"
    )


def _git(*args: str) -> str:
    entorno = dict(os.environ, TZ="America/Bogota")  # fechas del historial en hora de Colombia
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, encoding="utf-8", cwd=RAIZ, env=entorno
        ).stdout
    except FileNotFoundError:
        return ""


def _ejecutar(args: list[str]) -> tuple[int, str]:
    proceso = subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, encoding="utf-8", cwd=RAIZ
    )
    return proceso.returncode, _limpiar(proceso.stdout + proceso.stderr)


def recorrido(nombre: str, historia: str, entradas: list[str], depurar: bool = True) -> None:
    """Juega una partida con entradas fijas y guarda la transcripción, incluidas las entradas."""
    lineas: list[str] = []
    pendientes = list(entradas)

    def entrada(indicador: str) -> str:
        if not pendientes:
            raise EOFError
        valor = pendientes.pop(0)
        lineas.append(f"{indicador}{valor}")
        return valor

    sesion = Sesion(cargar_historia(RAIZ / historia))
    Consola(sesion, entrada=entrada, salida=lambda t="": lineas.append(t), depurar=depurar).ejecutar()
    comando = f"python jugar.py {historia}{' --depurar' if depurar else ''}   (entradas: {', '.join(entradas)})"
    (RECORRIDOS / nombre).write_text(_encabezado(comando) + "\n".join(lineas) + "\n", encoding="utf-8")


def segundo_equipo() -> int:
    codigo_pruebas, pruebas = _ejecutar(["-m", "pytest", "-v", "-p", "no:cacheprovider"])
    codigo_rnf, rnf = _ejecutar(["scripts/verificar_rnf.py"])
    usuario = _git("config", "user.name").strip() or "sin configurar"
    (EVIDENCIAS / "ejecucion_segundo_equipo.txt").write_text(
        f"Ejecución en un segundo equipo (usuario Git: {usuario})\n"
        + _encabezado("python -m pytest -v  y  python scripts/verificar_rnf.py")
        + pruebas
        + "\n" + "=" * 70 + "\n\n"
        + rnf,
        encoding="utf-8",
    )
    print(f"Pruebas: {'OK' if codigo_pruebas == 0 else 'CON FALLOS'} · RNF: {'OK' if codigo_rnf == 0 else 'CON FALLOS'}")
    print("Escrito evidencias/ejecucion_segundo_equipo.txt")
    return 0 if codigo_pruebas == 0 and codigo_rnf == 0 else 1


def main() -> int:
    if "--segundo-equipo" in sys.argv:
        return segundo_equipo()
    RECORRIDOS.mkdir(parents=True, exist_ok=True)

    codigo_pruebas, salida = _ejecutar(["-m", "pytest", "-v", "-p", "no:cacheprovider"])
    (EVIDENCIAS / "registro_pruebas.txt").write_text(_encabezado("python -m pytest -v") + salida, encoding="utf-8")

    codigo_rnf, salida = _ejecutar(["scripts/verificar_rnf.py"])
    (EVIDENCIAS / "rnf_resultados.txt").write_text(
        _encabezado("python scripts/verificar_rnf.py") + salida, encoding="utf-8"
    )

    ref = "historias/la_ultima_transmision.json"
    recorrido("final_E4.txt", ref, ["1", "1", "1", "s"])
    recorrido("final_E5.txt", ref, ["1", "2", "1", "s"])
    recorrido("final_E6.txt", ref, ["1", "2", "2", "s"])
    recorrido("condicion_cambia_opciones.txt", ref, ["1", "1", "r", "1", "2", "s"])
    recorrido("entradas_invalidas.txt", ref, ["abc", "9", "1", "2", "activar_codigo", "", "s"])
    recorrido("reinicio.txt", ref, ["1", "1", "1", "r", "s"])
    recorrido("deshacer.txt", ref, ["d", "1", "1", "d", "d", "2", "1", "d", "2", "s"])
    recorrido("segunda_historia.txt", "historias/el_faro.json", ["1", "1", "r", "2", "1", "s"])
    recorrido("bloqueo.txt", "historias/pruebas/bloqueo_en_partida.json", ["1", "2", "1", "r", "s"])

    codigo, salida = _ejecutar(["jugar.py", "--validar", "historias/invalidas/destino_inexistente.json"])
    (RECORRIDOS / "error_destino_E99.txt").write_text(
        _encabezado("python jugar.py --validar historias/invalidas/destino_inexistente.json")
        + salida
        + f"\n(código de salida: {codigo})\n",
        encoding="utf-8",
    )

    historial = _git("log", "--date=format-local:%Y-%m-%d %H:%M:%S (hora de Colombia)", "--format=%h | %ad | %aN <%aE> | %s%d")
    estadisticas = _git("log", "--date=format-local:%Y-%m-%d %H:%M", "--format=%n%h %ad %aN%n    %s", "--stat")
    versiones = _git("tag", "-n1", "--sort=creatordate")
    (EVIDENCIAS / "historial_git.txt").write_text(
        _encabezado("git log")
        + "Autores unificados con .mailmap (un integrante hizo commits con más de una configuración de Git).\n\n"
        + "VERSIONES (tags)\n"
        + versiones
        + "\nHISTORIAL (hash | fecha | autor | mensaje)\n"
        + historial
        + "\nDETALLE DE ARCHIVOS POR COMMIT (git log --stat)\n"
        + estadisticas,
        encoding="utf-8",
    )

    print(f"Pruebas: {'OK' if codigo_pruebas == 0 else 'CON FALLOS'} · RNF: {'OK' if codigo_rnf == 0 else 'CON FALLOS'}")
    print(f"Evidencias escritas en {EVIDENCIAS.relative_to(RAIZ)}/")
    return 0 if codigo_pruebas == 0 and codigo_rnf == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
