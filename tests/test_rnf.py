"""Verificación automatizada de los requisitos no funcionales (ver scripts/verificar_rnf.py)."""

from scripts.verificar_rnf import REFERENCIA, SEGUNDA, verificar_rnf01, verificar_rnf02, verificar_rnf03


def test_rnf01_historias_nuevas_sin_modificar_el_codigo():
    r = verificar_rnf01()
    assert r["segunda_historia_finales_alcanzados"] == r["segunda_historia_finales_declarados"] == ["F3", "F4"]
    assert r["escena_E7_agregada_jugable"] is True
    assert r["hash_codigo_antes"] == r["hash_codigo_despues"]
    assert r["cumple"] is True


def test_rnf02_todos_los_errores_de_contenido_son_claros():
    r = verificar_rnf02()
    assert r["archivos"] == 11
    assert r["porcentaje"] == 100.0, "\n".join(r["detalle"])


def test_rnf03_mil_entradas_aleatorias_sin_fallos_ni_alteraciones():
    for ruta in (REFERENCIA, SEGUNDA):
        r = verificar_rnf03(ruta)
        assert r["entradas"] >= 950
        assert r["rechazadas"] > 0 and r["aceptadas"] > 0
        assert r["excepciones_no_controladas"] == 0
        assert r["rechazadas_que_alteraron_estado"] == 0


def test_rnf03_regresion_digitos_unicode_no_cierran_la_consola():
    """Defecto hallado por RNF03: '²'.isdigit() es True pero int('²') lanzaba ValueError."""
    from interfaz.consola import Consola
    from motor.cargador import cargar_historia
    from motor.sesion import Sesion

    impreso = []
    sesion = Sesion(cargar_historia(REFERENCIA))
    consola = Consola(sesion, salida=impreso.append)
    for texto in ["²", "١", "¾", "①"]:
        assert consola.procesar(texto) is True
        assert sesion.escena_actual.id == "E1"
    assert all("no existe" in linea for linea in impreso)
