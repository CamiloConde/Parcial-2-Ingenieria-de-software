"""U6 (solicitud de cambio SC01). Deshacer restaura escena y variables y consume la posibilidad de retroceder."""

import pytest

from tests.conftest import ids

INICIALES = {"conoce_origen": False, "confia_en_la_voz": False}


def test_u6_deshacer_restaura_y_consume_el_retroceso(sesion):
    """Ejemplo del anexo: E2 → investigar → E3; deshacer → E2; segundo deshacer no cambia nada."""
    sesion.elegir("revisar")
    assert sesion.elegir("investigar").aceptada
    assert (sesion.escena_actual.id, sesion.variables["conoce_origen"]) == ("E3", True)

    resultado = sesion.deshacer()
    assert resultado.aceptada
    assert sesion.escena_actual.id == "E2"
    assert sesion.variables == INICIALES
    assert sesion.puede_deshacer is False

    segundo = sesion.deshacer()
    assert segundo.aceptada is False
    assert "No hay una decisión para deshacer" in segundo.mensaje
    assert sesion.escena_actual.id == "E2"
    assert sesion.variables == INICIALES

    sesion.elegir("continuar")
    assert sesion.escena_actual.id == "E3"
    assert ids(sesion.opciones_disponibles()) == ["activar_sin_verificar", "cortar"]


def test_u6_al_comenzar_no_hay_retroceso(sesion):
    assert sesion.puede_deshacer is False
    assert sesion.deshacer().aceptada is False
    assert sesion.escena_actual.id == "E1"
    assert sesion.variables == INICIALES


@pytest.mark.parametrize(
    "entrada_invalida",
    ["activar_sin_verificar", "no_existe", "revisar", ""],
    ids=["no_habilitada", "inexistente", "de_otra_escena", "vacia"],
)
def test_u6_variante_entrada_invalida_preserva_el_historial(sesion, entrada_invalida):
    sesion.elegir("revisar")
    sesion.elegir("investigar")  # última elección válida: E2 -> E3

    assert sesion.elegir(entrada_invalida).aceptada is False
    assert sesion.puede_deshacer is True

    assert sesion.deshacer().aceptada
    assert sesion.escena_actual.id == "E2"  # no E3: la entrada inválida no sustituyó el historial
    assert sesion.variables == INICIALES


def test_u6_variante_nueva_eleccion_vuelve_a_habilitar_el_retroceso(sesion):
    sesion.elegir("revisar")
    sesion.elegir("investigar")
    sesion.deshacer()
    assert sesion.puede_deshacer is False

    assert sesion.elegir("continuar").aceptada
    assert sesion.puede_deshacer is True
    assert sesion.deshacer().aceptada
    assert sesion.escena_actual.id == "E2"
    assert sesion.variables == INICIALES


def test_u6_variante_solo_un_nivel(sesion):
    for id_opcion in ["revisar", "investigar", "cortar"]:
        sesion.elegir(id_opcion)
    assert sesion.deshacer().aceptada
    assert sesion.escena_actual.id == "E3"
    assert sesion.deshacer().aceptada is False
    assert sesion.escena_actual.id == "E3"  # no retrocede a E2


def test_u6_variante_efecto_que_no_cambia_el_valor_se_restaura_exactamente(sesion):
    """cortar asigna confia_en_la_voz = falso cuando ya era falso: la instantánea restaura igual."""
    for id_opcion in ["revisar", "continuar", "cortar"]:
        sesion.elegir(id_opcion)
    sesion.deshacer()
    assert sesion.escena_actual.id == "E3"
    assert sesion.variables == INICIALES
