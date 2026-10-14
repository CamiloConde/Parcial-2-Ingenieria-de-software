"""U4. Los errores de contenido obligatorios producen rechazo o diagnóstico controlado.

Cada variante indica el archivo de entrada, la categoría esperada y el ID o campo
que el mensaje debe mencionar.
"""

import pytest

from motor import errores as E
from motor.cargador import cargar_historia, historia_desde_dict
from motor.errores import ErrorContenido
from tests.conftest import HISTORIAS, REFERENCIA

INVALIDAS = HISTORIAS / "invalidas"

CASOS_ARCHIVO = [
    # (archivo, categoría esperada, textos que deben aparecer en el mensaje)
    ("archivo_ilegible.json", E.ARCHIVO_ILEGIBLE, ["JSON mal formado", "línea"]),
    ("estructura_incorrecta.json", E.ESTRUCTURA_INCORRECTA, ["escenas", "lista"]),
    ("campo_faltante.json", E.CAMPO_FALTANTE, ["texto", "escenas[E2]", "destino", "opciones[cortar]"]),
    ("inicio_inexistente.json", E.INICIO_INEXISTENTE, ["E0", "inicio"]),
    ("escena_duplicada.json", E.ESCENA_DUPLICADA, ["E2"]),
    ("opcion_duplicada.json", E.OPCION_DUPLICADA, ["investigar", "escenas[E2]"]),
    ("destino_inexistente.json", E.DESTINO_INEXISTENTE, ["E99", "escenas[E3].opciones[cortar].destino"]),
    ("variable_no_declarada.json", E.VARIABLE_NO_DECLARADA, ["conoce_origin", "activar_codigo"]),
    ("valor_no_booleano.json", E.VALOR_NO_BOOLEANO, ["conoce_origen", "'si'", "investigar"]),
    ("final_con_opciones.json", E.FINAL_CON_OPCIONES, ["escenas[E6]"]),
    ("no_final_sin_opciones.json", E.NO_FINAL_SIN_OPCIONES, ["escenas[E2]"]),
]


@pytest.mark.parametrize("archivo, categoria, textos", CASOS_ARCHIVO, ids=[c[0] for c in CASOS_ARCHIVO])
def test_u4_archivo_invalido_se_rechaza_con_categoria_y_ubicacion(archivo, categoria, textos):
    with pytest.raises(ErrorContenido) as info:
        cargar_historia(INVALIDAS / archivo)
    error = info.value
    assert categoria in error.categorias
    mensaje = error.descripcion()
    assert f"[{categoria}]" in mensaje
    for texto in textos:
        assert texto in mensaje, f"El mensaje no menciona {texto!r}:\n{mensaje}"


def test_u4_archivo_inexistente(tmp_path):
    with pytest.raises(ErrorContenido) as info:
        cargar_historia(tmp_path / "no_existe.json")
    assert info.value.categorias == {E.ARCHIVO_ILEGIBLE}
    assert "No existe el archivo" in info.value.descripcion()


def test_u4_archivo_no_utf8(tmp_path):
    ruta = tmp_path / "latin1.json"
    ruta.write_bytes('{"titulo": "Transmisión"}'.encode("latin-1"))
    with pytest.raises(ErrorContenido) as info:
        cargar_historia(ruta)
    assert info.value.categorias == {E.ARCHIVO_ILEGIBLE}
    assert "UTF-8" in info.value.descripcion()


@pytest.mark.parametrize(
    "mutar, categoria, texto",
    [
        (lambda d: ["no", "es", "objeto"], E.ESTRUCTURA_INCORRECTA, "raíz"),
        (lambda d: {k: v for k, v in d.items() if k != "inicio"}, E.CAMPO_FALTANTE, "'inicio'"),
        (lambda d: {**d, "escenas": []}, E.ESTRUCTURA_INCORRECTA, "al menos una escena"),
        (lambda d: {**d, "variables": {"conoce_origen": 0, "confia_en_la_voz": False}}, E.VALOR_NO_BOOLEANO, "variables.conoce_origen"),
        (lambda d: {**d, "titulo": 7}, E.ESTRUCTURA_INCORRECTA, "titulo"),
    ],
    ids=["raiz_no_objeto", "falta_inicio", "sin_escenas", "variable_inicial_no_booleana", "titulo_no_texto"],
)
def test_u4_variantes_en_memoria(datos_referencia, mutar, categoria, texto):
    with pytest.raises(ErrorContenido) as info:
        historia_desde_dict(mutar(datos_referencia))
    assert categoria in info.value.categorias
    assert texto in info.value.descripcion()


def test_u4_se_acumulan_todos_los_problemas(datos_referencia):
    """Un archivo con varios errores los informa todos en una sola validación (ADR-02)."""
    datos_referencia["inicio"] = "E0"
    datos_referencia["escenas"][2]["opciones"][2]["destino"] = "E99"
    with pytest.raises(ErrorContenido) as info:
        historia_desde_dict(datos_referencia)
    assert {E.INICIO_INEXISTENTE, E.DESTINO_INEXISTENTE} <= info.value.categorias


def test_u4_historia_de_referencia_es_valida():
    historia = cargar_historia(REFERENCIA)
    assert historia.inicio == "E1"
    assert len(historia.escenas) == 6
