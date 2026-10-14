"""Modelo inmutable de una historia: Historia, Escena y Opcion.

Los objetos se construyen solo a partir de datos ya validados.
"""

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class Opcion:
    id: str
    texto: str
    destino: str
    condiciones: Mapping[str, bool]
    efectos: Mapping[str, bool]

    def habilitada(self, variables: Mapping[str, bool]) -> bool:
        """Todas las condiciones deben cumplirse; sin condiciones, siempre habilitada."""
        return all(variables.get(nombre) == valor for nombre, valor in self.condiciones.items())


@dataclass(frozen=True)
class Escena:
    id: str
    texto: str
    final: bool
    opciones: tuple[Opcion, ...]

    def opcion(self, id_opcion: str) -> Opcion | None:
        for opcion in self.opciones:
            if opcion.id == id_opcion:
                return opcion
        return None


@dataclass(frozen=True)
class Historia:
    titulo: str
    inicio: str
    variables: Mapping[str, bool]
    escenas: Mapping[str, Escena]

    def escena(self, id_escena: str) -> Escena:
        return self.escenas[id_escena]


def historia_desde_datos(datos: dict) -> Historia:
    """Convierte un diccionario validado en objetos del modelo."""
    escenas = {}
    for e in datos["escenas"]:
        opciones = tuple(
            Opcion(
                id=o["id"],
                texto=o["texto"],
                destino=o["destino"],
                condiciones=MappingProxyType(dict(o["condiciones"])),
                efectos=MappingProxyType(dict(o["efectos"])),
            )
            for o in e["opciones"]
        )
        escenas[e["id"]] = Escena(id=e["id"], texto=e["texto"], final=e["final"], opciones=opciones)
    return Historia(
        titulo=datos["titulo"],
        inicio=datos["inicio"],
        variables=MappingProxyType(dict(datos["variables"])),
        escenas=MappingProxyType(escenas),
    )
