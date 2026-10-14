"""Reglas de una partida: estado actual, opciones habilitadas, elección y reinicio.

La sesión no conoce ninguna historia concreta: evalúa condiciones y aplica
efectos a partir de los datos del modelo.
"""

from dataclasses import dataclass

from motor.modelo import Escena, Historia, Opcion


@dataclass(frozen=True)
class Resultado:
    """Respuesta de una operación sobre la sesión."""

    aceptada: bool
    mensaje: str = ""


class Sesion:
    def __init__(self, historia: Historia):
        self._historia = historia
        self.reiniciar()

    # --- Consultas -------------------------------------------------------
    @property
    def historia(self) -> Historia:
        return self._historia

    @property
    def escena_actual(self) -> Escena:
        return self._historia.escena(self._escena_id)

    @property
    def variables(self) -> dict[str, bool]:
        """Copia del estado: modificarla no altera la sesión."""
        return dict(self._variables)

    @property
    def terminada(self) -> bool:
        return self.escena_actual.final

    @property
    def bloqueada(self) -> bool:
        """Escena no final sin ninguna opción habilitada con el estado actual."""
        return not self.terminada and not self.opciones_disponibles()

    def opciones_disponibles(self) -> list[Opcion]:
        return [o for o in self.escena_actual.opciones if o.habilitada(self._variables)]

    # --- Operaciones -----------------------------------------------------
    def elegir(self, id_opcion: str) -> Resultado:
        """Aplica la opción si existe y está habilitada; si no, el estado no cambia."""
        opcion = self._opcion_habilitada(id_opcion)
        if isinstance(opcion, Resultado):
            return opcion
        self._aplicar(opcion)
        return Resultado(True, f"Elegiste: {opcion.texto}")

    def reiniciar(self) -> Resultado:
        """Vuelve a la escena inicial y a los valores iniciales de todas las variables."""
        self._escena_id = self._historia.inicio
        self._variables = dict(self._historia.variables)
        return Resultado(True, "Partida reiniciada.")

    # --- Internos ----------------------------------------------------------
    def _opcion_habilitada(self, id_opcion: str) -> Opcion | Resultado:
        escena = self.escena_actual
        if escena.final:
            return Resultado(False, "La partida terminó: solo puedes reiniciar o salir.")
        opcion = escena.opcion(id_opcion)
        if opcion is None:
            return Resultado(False, f"La opción '{id_opcion}' no existe en esta escena.")
        if not opcion.habilitada(self._variables):
            return Resultado(False, f"La opción '{id_opcion}' no está habilitada con lo ocurrido hasta ahora.")
        return opcion

    def _aplicar(self, opcion: Opcion) -> None:
        self._variables.update(opcion.efectos)
        self._escena_id = opcion.destino
