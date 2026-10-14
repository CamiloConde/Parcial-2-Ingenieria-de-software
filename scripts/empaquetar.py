"""Genera el ZIP de entrega con los archivos versionados del proyecto.

Uso:  python scripts/empaquetar.py
Resultado: entrega/Parcial_CondeCamilo_JacomeMiguel.zip
"""

import subprocess
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
NOMBRE = "Parcial_CondeCamilo_JacomeMiguel"
EXCLUIDOS = ("entrega/",)


def archivos_versionados() -> list[str]:
    salida = subprocess.run(["git", "ls-files"], capture_output=True, text=True, encoding="utf-8", cwd=RAIZ, check=True)
    return [a for a in salida.stdout.splitlines() if a and not a.startswith(EXCLUIDOS)]


def main() -> int:
    destino = RAIZ / "entrega" / f"{NOMBRE}.zip"
    destino.parent.mkdir(exist_ok=True)
    archivos = archivos_versionados()
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zipf:
        for relativo in archivos:
            zipf.write(RAIZ / relativo, f"{NOMBRE}/{relativo}")
    with zipfile.ZipFile(destino) as zipf:
        assert zipf.testzip() is None
    print(f"{destino.relative_to(RAIZ)}: {len(archivos)} archivos, {destino.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
