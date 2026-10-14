"""I1. La lectura de un archivo real y el motor funcionan juntos: carga y decisiones hasta un final."""

import pytest

from interfaz.consola import Consola
from motor.cargador import cargar_historia
from motor.sesion import Sesion
from tests.conftest import REFERENCIA

RUTAS_A_FINALES = [
    (["revisar", "investigar", "activar_codigo"], "E4", {"conoce_origen": True, "confia_en_la_voz": True}),
    (["revisar", "continuar", "activar_sin_verificar"], "E5", {"conoce_origen": False, "confia_en_la_voz": True}),
    (["revisar", "continuar", "cortar"], "E6", {"conoce_origen": False, "confia_en_la_voz": False}),
]


@pytest.mark.parametrize("camino, final, variables", RUTAS_A_FINALES, ids=["E4_rescate", "E5_eco", "E6_silencio"])
def test_i1_archivo_real_hasta_cada_final(camino, final, variables):
    sesion = Sesion(cargar_historia(REFERENCIA))
    assert sesion.escena_actual.id == "E1"
    for id_opcion in camino:
        assert sesion.elegir(id_opcion).aceptada
    assert sesion.escena_actual.id == final
    assert sesion.terminada is True
    assert sesion.opciones_disponibles() == []
    assert sesion.variables == variables


class ConsolaGuionada:
    """Simula al lector: entrega las líneas del guion y guarda todo lo impreso."""

    def __init__(self, lineas):
        self.lineas = list(lineas)
        self.impreso: list[str] = []

    def entrada(self, _indicador):
        if not self.lineas:
            raise EOFError
        return self.lineas.pop(0)

    def salida(self, texto=""):
        self.impreso.append(texto)

    @property
    def texto(self):
        return "\n".join(self.impreso)


def test_i1_consola_completa_con_entradas_invalidas_reinicio_y_final():
    sesion = Sesion(cargar_historia(REFERENCIA))
    lector = ConsolaGuionada(["1", "abc", "9", "1", "activar_sin_verificar", "1", "1", "r", "1", "2", "2", "s"])
    Consola(sesion, entrada=lector.entrada, salida=lector.salida).ejecutar()
    texto = lector.texto
    assert "La última transmisión" in texto
    assert "La opción 'abc' no existe en esta escena" in texto  # texto libre: lo rechaza el motor
    assert "Entrada no válida: '9'" in texto
    assert "no está habilitada" in texto  # activar_sin_verificar tras investigar
    assert "*** FIN — desenlace E4 ***" in texto
    assert "Partida reiniciada." in texto
    assert "*** FIN — desenlace E6 ***" in texto  # revisar, continuar, cortar
    assert sesion.escena_actual.id == "E6"
