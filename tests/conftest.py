import copy
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
HISTORIAS = RAIZ / "historias"
REFERENCIA = HISTORIAS / "la_ultima_transmision.json"


@pytest.fixture
def datos_referencia():
    """Copia nueva del documento de la historia de referencia para cada prueba."""
    with REFERENCIA.open(encoding="utf-8") as archivo:
        return copy.deepcopy(json.load(archivo))


@pytest.fixture
def sesion():
    """Sesión nueva sobre la historia de referencia cargada desde su archivo."""
    from motor.cargador import cargar_historia
    from motor.sesion import Sesion

    return Sesion(cargar_historia(REFERENCIA))


def ids(opciones):
    return [o.id for o in opciones]
