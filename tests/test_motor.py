"""Pruebas unitarias del motor de sesión: U1, U2, U3 y U5."""

import pytest

from motor.modelo import Opcion
from motor.sesion import Sesion
from tests.conftest import ids


# ---------------------------------------------------------------- U1
@pytest.mark.parametrize(
    "conoce_origen, esperadas",
    [
        (True, ["activar_codigo", "cortar"]),
        (False, ["activar_sin_verificar", "cortar"]),
    ],
    ids=["conoce_origen_verdadero", "conoce_origen_falso"],
)
def test_u1_condiciones_habilitan_solo_opciones_correspondientes(sesion, conoce_origen, esperadas):
    sesion.elegir("revisar")
    sesion.elegir("investigar" if conoce_origen else "continuar")
    assert sesion.escena_actual.id == "E3"
    assert sesion.variables["conoce_origen"] is conoce_origen
    assert ids(sesion.opciones_disponibles()) == esperadas  # exactamente dos opciones


@pytest.mark.parametrize(
    "condiciones, variables, habilitada",
    [
        ({}, {"a": False, "b": False}, True),  # mapa vacío habilita
        ({"a": True}, {"a": True, "b": False}, True),
        ({"a": True}, {"a": False, "b": False}, False),
        ({"a": True, "b": False}, {"a": True, "b": False}, True),  # todas se cumplen
        ({"a": True, "b": False}, {"a": True, "b": True}, False),  # basta una que falle
    ],
)
def test_u1_evaluacion_de_condiciones(condiciones, variables, habilitada):
    opcion = Opcion(id="x", texto="X", destino="D", condiciones=condiciones, efectos={})
    assert opcion.habilitada(variables) is habilitada


# ---------------------------------------------------------------- U2
@pytest.mark.parametrize(
    "camino, escena_esperada, variables_esperadas",
    [
        (["revisar"], "E2", {"conoce_origen": False, "confia_en_la_voz": False}),
        (["revisar", "investigar"], "E3", {"conoce_origen": True, "confia_en_la_voz": False}),  # CA01
        (["revisar", "continuar"], "E3", {"conoce_origen": False, "confia_en_la_voz": False}),
        (["revisar", "investigar", "activar_codigo"], "E4", {"conoce_origen": True, "confia_en_la_voz": True}),
        (["revisar", "continuar", "activar_sin_verificar"], "E5", {"conoce_origen": False, "confia_en_la_voz": True}),
        (["revisar", "investigar", "cortar"], "E6", {"conoce_origen": True, "confia_en_la_voz": False}),
    ],
)
def test_u2_eleccion_valida_aplica_efectos_y_avanza(sesion, camino, escena_esperada, variables_esperadas):
    for id_opcion in camino:
        resultado = sesion.elegir(id_opcion)
        assert resultado.aceptada, resultado.mensaje
    assert sesion.escena_actual.id == escena_esperada
    assert sesion.variables == variables_esperadas


# ---------------------------------------------------------------- U3
@pytest.mark.parametrize(
    "camino_previo, id_invalido, motivo",
    [
        ([], "no_existe", "no existe"),
        ([], "investigar", "no existe"),  # existe en otra escena, no en E1
        (["revisar", "continuar"], "activar_codigo", "no está habilitada"),  # CA02
        (["revisar", "investigar"], "activar_sin_verificar", "no está habilitada"),
        (["revisar", "investigar", "cortar"], "revisar", "terminó"),  # desde un final
        ([], "", "no existe"),
    ],
    ids=["inexistente", "de_otra_escena", "CA02_no_habilitada", "no_habilitada_inversa", "en_final", "vacia"],
)
def test_u3_opcion_invalida_deja_intacto_el_estado(sesion, camino_previo, id_invalido, motivo):
    for id_opcion in camino_previo:
        sesion.elegir(id_opcion)
    escena_antes, variables_antes = sesion.escena_actual.id, sesion.variables

    resultado = sesion.elegir(id_invalido)

    assert resultado.aceptada is False
    assert motivo in resultado.mensaje
    assert sesion.escena_actual.id == escena_antes
    assert sesion.variables == variables_antes


def test_u3_modificar_la_copia_de_variables_no_altera_la_sesion(sesion):
    copia = sesion.variables
    copia["conoce_origen"] = True
    assert sesion.variables["conoce_origen"] is False


# ---------------------------------------------------------------- U5
@pytest.mark.parametrize(
    "camino",
    [[], ["revisar"], ["revisar", "investigar"], ["revisar", "investigar", "activar_codigo"], ["revisar", "continuar", "activar_sin_verificar"]],
    ids=["inicio", "E2", "E3", "final_E4", "final_E5"],
)
def test_u5_reiniciar_restaura_escena_y_variables_iniciales(sesion, camino):
    for id_opcion in camino:
        assert sesion.elegir(id_opcion).aceptada
    resultado = sesion.reiniciar()
    assert resultado.aceptada
    assert sesion.escena_actual.id == "E1"
    assert sesion.variables == {"conoce_origen": False, "confia_en_la_voz": False}
    assert ids(sesion.opciones_disponibles()) == ["revisar"]


@pytest.mark.parametrize("camino", [["revisar"], ["revisar", "investigar"], ["revisar", "investigar", "activar_codigo"]])
def test_u5_reiniciar_elimina_historial(sesion, camino):
    """Extensión de U5 por SC01: tras reiniciar no hay retroceso disponible."""
    for id_opcion in camino:
        sesion.elegir(id_opcion)
    assert sesion.puede_deshacer is True
    sesion.reiniciar()
    assert sesion.puede_deshacer is False
    assert sesion.deshacer().aceptada is False
    assert sesion.escena_actual.id == "E1"
    assert sesion.variables == {"conoce_origen": False, "confia_en_la_voz": False}


# ---------------------------------------------------------------- Bloqueo
def test_bloqueo_en_partida_se_detecta_y_reiniciar_lo_resuelve():
    from motor.cargador import cargar_historia
    from tests.conftest import HISTORIAS

    sesion = Sesion(cargar_historia(HISTORIAS / "pruebas" / "bloqueo_en_partida.json"))
    sesion.elegir("revisar")
    sesion.elegir("continuar")
    assert sesion.escena_actual.id == "E3"
    assert sesion.bloqueada is True
    assert sesion.terminada is False
    sesion.reiniciar()
    assert sesion.bloqueada is False
    assert sesion.escena_actual.id == "E1"
