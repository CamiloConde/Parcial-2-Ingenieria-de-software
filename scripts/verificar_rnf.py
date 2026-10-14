"""Verificación reproducible de los requisitos no funcionales RNF01, RNF02 y RNF03.

Uso:  python scripts/verificar_rnf.py
Termina con código 0 si los tres RNF se cumplen y 1 si alguno falla.
"""

import copy
import hashlib
import json
import random
import subprocess
import sys
from collections import deque
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from interfaz.consola import Consola  # noqa: E402
from motor.cargador import cargar_historia, historia_desde_dict, leer_archivo  # noqa: E402
from motor.sesion import Sesion  # noqa: E402

HISTORIAS = RAIZ / "historias"
REFERENCIA = HISTORIAS / "la_ultima_transmision.json"
SEGUNDA = HISTORIAS / "el_faro.json"
SEMILLA = 2026
CANTIDAD_ENTRADAS = 1000

# Archivo inválido -> (categoría esperada, ID o campo que debe mencionar el mensaje)
ESPERADOS_RNF02 = {
    "archivo_ilegible.json": ("ARCHIVO_ILEGIBLE", "línea"),
    "estructura_incorrecta.json": ("ESTRUCTURA_INCORRECTA", "escenas"),
    "campo_faltante.json": ("CAMPO_FALTANTE", "escenas[E2]"),
    "inicio_inexistente.json": ("INICIO_INEXISTENTE", "E0"),
    "escena_duplicada.json": ("ESCENA_DUPLICADA", "E2"),
    "opcion_duplicada.json": ("OPCION_DUPLICADA", "investigar"),
    "destino_inexistente.json": ("DESTINO_INEXISTENTE", "E99"),
    "variable_no_declarada.json": ("VARIABLE_NO_DECLARADA", "conoce_origin"),
    "valor_no_booleano.json": ("VALOR_NO_BOOLEANO", "conoce_origen"),
    "final_con_opciones.json": ("FINAL_CON_OPCIONES", "escenas[E6]"),
    "no_final_sin_opciones.json": ("NO_FINAL_SIN_OPCIONES", "escenas[E2]"),
}


# ----------------------------------------------------------------- RNF01
def hash_codigo() -> str:
    """Huella SHA-256 de todo el código del motor y de la interfaz."""
    h = hashlib.sha256()
    for carpeta in ("motor", "interfaz"):
        for archivo in sorted((RAIZ / carpeta).rglob("*.py")):
            h.update(archivo.relative_to(RAIZ).as_posix().encode())
            h.update(archivo.read_bytes())
    return h.hexdigest()


def finales_alcanzables(historia) -> set[str]:
    """Explora todas las decisiones posibles desde el inicio y devuelve los finales a los que se llega."""
    alcanzados, pendientes, vistos = set(), deque([()]), set()
    while pendientes:
        camino = pendientes.popleft()
        sesion = Sesion(historia)
        for id_opcion in camino:
            sesion.elegir(id_opcion)
        estado = (sesion.escena_actual.id, tuple(sorted(sesion.variables.items())))
        if estado in vistos:
            continue
        vistos.add(estado)
        if sesion.terminada:
            alcanzados.add(sesion.escena_actual.id)
        for opcion in sesion.opciones_disponibles():
            pendientes.append(camino + (opcion.id,))
    return alcanzados


def verificar_rnf01() -> dict:
    antes = hash_codigo()

    segunda = cargar_historia(SEGUNDA)
    finales_declarados = {e.id for e in segunda.escenas.values() if e.final}
    finales_segunda = finales_alcanzables(segunda)

    datos = copy.deepcopy(leer_archivo(REFERENCIA))
    datos["escenas"].append(
        {"id": "E7", "texto": "La operadora apaga la radio y se va a dormir.", "final": True, "opciones": []}
    )
    datos["escenas"][0]["opciones"].append(
        {"id": "ignorar", "texto": "Ignorar la señal", "destino": "E7", "condiciones": {}, "efectos": {}}
    )
    ampliada = Sesion(historia_desde_dict(datos))
    llega_e7 = ampliada.elegir("ignorar").aceptada and ampliada.escena_actual.id == "E7" and ampliada.terminada

    despues = hash_codigo()
    return {
        "segunda_historia_finales_declarados": sorted(finales_declarados),
        "segunda_historia_finales_alcanzados": sorted(finales_segunda),
        "escena_E7_agregada_jugable": llega_e7,
        "hash_codigo_antes": antes,
        "hash_codigo_despues": despues,
        "lineas_de_codigo_modificadas": 0 if antes == despues else "DISTINTO",
        "cumple": finales_segunda == finales_declarados and llega_e7 and antes == despues,
    }


# ----------------------------------------------------------------- RNF02
def verificar_rnf02() -> dict:
    detalle, correctos = [], 0
    archivos = sorted((HISTORIAS / "invalidas").glob("*.json"))
    for archivo in archivos:
        categoria, texto = ESPERADOS_RNF02.get(archivo.name, ("?", "?"))
        proceso = subprocess.run(
            [sys.executable, str(RAIZ / "jugar.py"), "--validar", str(archivo)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=RAIZ,
        )
        salida = proceso.stdout + proceso.stderr
        ok = (
            proceso.returncode == 1
            and f"[{categoria}]" in salida
            and texto in salida
            and "Traceback" not in salida
        )
        correctos += ok
        primera = next((l.strip() for l in salida.splitlines() if l.strip().startswith("- [")), salida.strip()[:120])
        detalle.append(f"{'OK ' if ok else 'FALLA'} {archivo.name:30} código={proceso.returncode}  {primera}")
    porcentaje = 100.0 * correctos / len(archivos) if archivos else 0.0
    return {"archivos": len(archivos), "correctos": correctos, "porcentaje": porcentaje, "detalle": detalle,
            "cumple": bool(archivos) and correctos == len(archivos)}


# ----------------------------------------------------------------- RNF03
def _generar_entradas(historia, cantidad: int, semilla: int) -> list[str]:
    azar = random.Random(semilla)
    ids_opciones = sorted({o.id for e in historia.escenas.values() for o in e.opciones})
    basura = ["", " ", "abc", "-1", "0", "99", "1.5", "R R", "∞", "SELECT *", "\t", "ñandú", "--", "None", "1 2"]
    entradas = []
    for _ in range(cantidad):
        tipo = azar.random()
        if tipo < 0.35:
            entradas.append(str(azar.randint(-3, 6)))
        elif tipo < 0.65:
            entradas.append(azar.choice(ids_opciones))
        elif tipo < 0.72:
            entradas.append(azar.choice(["r", "R", " reiniciar ", "d", "D", "deshacer", "d", "d"]))
        elif tipo < 0.85:
            entradas.append(azar.choice(basura))
        else:
            largo = azar.randint(1, 12)
            entradas.append("".join(chr(azar.randint(33, 0x24F)) for _ in range(largo)))
    return [e for e in entradas if e.strip().lower() not in ("s", "salir")]


def _sera_aceptada(sesion: Sesion, texto: str) -> bool:
    """Predicción independiente de si una entrada debe cambiar el estado."""
    comando = texto.strip()
    if comando.lower() in ("r", "reiniciar"):
        return True
    if comando.lower() in ("d", "deshacer"):
        return sesion.puede_deshacer
    disponibles = [o.id for o in sesion.opciones_disponibles()]
    if comando.isascii() and comando.isdigit():
        return 1 <= int(comando) <= len(disponibles)
    return comando in disponibles


def verificar_rnf03(ruta: Path = REFERENCIA, cantidad: int = CANTIDAD_ENTRADAS, semilla: int = SEMILLA) -> dict:
    historia = cargar_historia(ruta)
    sesion = Sesion(historia)
    consola = Consola(sesion, entrada=lambda _: "s", salida=lambda *_: None)
    entradas = _generar_entradas(historia, cantidad, semilla)
    excepciones, rechazadas, alteradas, aceptadas = 0, 0, 0, 0
    for texto in entradas:
        antes = (sesion.escena_actual.id, sesion.variables)
        aceptada = _sera_aceptada(sesion, texto)
        try:
            consola.procesar(texto)
        except Exception:  # noqa: BLE001 - el objetivo es contar cualquier excepción
            excepciones += 1
            continue
        despues = (sesion.escena_actual.id, sesion.variables)
        if aceptada:
            aceptadas += 1
        else:
            rechazadas += 1
            alteradas += antes != despues
    return {
        "historia": ruta.name,
        "semilla": semilla,
        "entradas": len(entradas),
        "aceptadas": aceptadas,
        "rechazadas": rechazadas,
        "excepciones_no_controladas": excepciones,
        "rechazadas_que_alteraron_estado": alteradas,
        "cumple": excepciones == 0 and alteradas == 0,
    }


# ----------------------------------------------------------------- Informe
def main() -> int:
    r1, r2 = verificar_rnf01(), verificar_rnf02()
    r3 = [verificar_rnf03(REFERENCIA), verificar_rnf03(SEGUNDA)]

    print("RNF01 Modificabilidad del contenido")
    for clave, valor in r1.items():
        print(f"  {clave}: {valor}")
    print("\nRNF02 Claridad de errores")
    for linea in r2["detalle"]:
        print(f"  {linea}")
    print(f"  resultado: {r2['correctos']}/{r2['archivos']} = {r2['porcentaje']:.0f} %  cumple: {r2['cumple']}")
    print("\nRNF03 Confiabilidad ante entradas inválidas")
    for r in r3:
        print("  " + json.dumps(r, ensure_ascii=False))

    cumple = r1["cumple"] and r2["cumple"] and all(r["cumple"] for r in r3)
    print(f"\nRESULTADO GLOBAL: {'CUMPLE' if cumple else 'NO CUMPLE'}")
    return 0 if cumple else 1


if __name__ == "__main__":
    sys.exit(main())
