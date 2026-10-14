"""Interfaz de consola: muestra la escena, lee comandos y los traduce a operaciones del motor.

No contiene reglas de la historia; toda decisión sobre opciones y efectos la
toma `Sesion`. Las funciones de entrada y salida se inyectan para poder probarla.
"""

from typing import Callable

from motor.sesion import Sesion

LINEA = "=" * 60


class Consola:
    def __init__(
        self,
        sesion: Sesion,
        entrada: Callable[[str], str] = input,
        salida: Callable[[str], None] = print,
        depurar: bool = False,
    ):
        self.sesion = sesion
        self._entrada = entrada
        self._salida = salida
        self._depurar = depurar

    # --- Bucle principal ---------------------------------------------------
    def ejecutar(self) -> None:
        self._salida(LINEA)
        self._salida(f"  {self.sesion.historia.titulo}")
        self._salida(LINEA)
        self.mostrar_escena()
        while True:
            try:
                texto = self._entrada("> ")
            except (EOFError, KeyboardInterrupt):
                self._salida("\nHasta pronto.")
                return
            if not self.procesar(texto):
                self._salida("Hasta pronto.")
                return

    def procesar(self, texto: str) -> bool:
        """Atiende una línea de entrada. Devuelve False si el lector pidió salir."""
        comando = (texto or "").strip()
        clave = comando.lower()
        if clave in ("s", "salir"):
            return False
        if clave in ("d", "deshacer"):
            resultado = self.sesion.deshacer()
            self._salida(resultado.mensaje)
            if resultado.aceptada:
                self.mostrar_escena()
            return True
        if clave in ("r", "reiniciar"):
            self._salida(self.sesion.reiniciar().mensaje)
            self.mostrar_escena()
            return True

        id_opcion = self._traducir_opcion(comando)
        if id_opcion is None:
            self._salida(f"Entrada no válida: '{comando}'. {self._ayuda()}")
            return True
        resultado = self.sesion.elegir(id_opcion)
        self._salida(resultado.mensaje)
        if resultado.aceptada:
            self.mostrar_escena()
        return True

    # --- Presentación --------------------------------------------------------
    def mostrar_escena(self) -> None:
        escena = self.sesion.escena_actual
        self._salida("")
        self._salida(f"[{escena.id}] {escena.texto}")
        if self._depurar:
            estado = ", ".join(f"{k}={'verdadero' if v else 'falso'}" for k, v in self.sesion.variables.items())
            self._salida(f"    (estado: {estado})")

        if self.sesion.terminada:
            self._salida("")
            self._salida(f"*** FIN — desenlace {escena.id} ***")
        elif self.sesion.bloqueada:
            self._salida("")
            self._salida(
                "!!! BLOQUEO: ninguna opción está habilitada en esta escena y no es un final. "
                "Revise las condiciones del archivo de la historia."
            )
        else:
            self._salida("")
            for numero, opcion in enumerate(self.sesion.opciones_disponibles(), start=1):
                self._salida(f"  {numero}. {opcion.texto}")
        self._salida(self._ayuda())

    def _ayuda(self) -> str:
        comandos = [] if self.sesion.terminada or self.sesion.bloqueada else ["número de opción"]
        if self.sesion.puede_deshacer:
            comandos.append("d = deshacer")
        comandos += ["r = reiniciar", "s = salir"]
        return "Comandos: " + " · ".join(comandos)

    def _traducir_opcion(self, comando: str) -> str | None:
        """Convierte '2' en el ID de la segunda opción visible. Un ID escrito se pasa tal cual."""
        disponibles = self.sesion.opciones_disponibles()
        if comando.isascii() and comando.isdigit():  # '²'.isdigit() es True pero int('²') falla
            indice = int(comando) - 1
            if 0 <= indice < len(disponibles):
                return disponibles[indice].id
            return None
        if comando and not self.sesion.terminada and not self.sesion.bloqueada:
            return comando  # el motor decide si existe y está habilitada
        return None
