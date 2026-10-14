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
