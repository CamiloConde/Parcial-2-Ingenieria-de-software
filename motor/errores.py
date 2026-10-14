"""Errores de contenido detectados al cargar o validar una historia."""

from dataclasses import dataclass

# Categorías de error de contenido. Se muestran entre corchetes en los mensajes.
ARCHIVO_ILEGIBLE = "ARCHIVO_ILEGIBLE"
ESTRUCTURA_INCORRECTA = "ESTRUCTURA_INCORRECTA"
CAMPO_FALTANTE = "CAMPO_FALTANTE"
INICIO_INEXISTENTE = "INICIO_INEXISTENTE"
ESCENA_DUPLICADA = "ESCENA_DUPLICADA"
OPCION_DUPLICADA = "OPCION_DUPLICADA"
DESTINO_INEXISTENTE = "DESTINO_INEXISTENTE"
VARIABLE_NO_DECLARADA = "VARIABLE_NO_DECLARADA"
VALOR_NO_BOOLEANO = "VALOR_NO_BOOLEANO"
FINAL_CON_OPCIONES = "FINAL_CON_OPCIONES"
NO_FINAL_SIN_OPCIONES = "NO_FINAL_SIN_OPCIONES"


@dataclass(frozen=True)
class Problema:
    """Un error concreto del archivo: categoría, causa y lugar donde ocurre."""

    categoria: str
    mensaje: str
    ubicacion: str = ""

    def __str__(self) -> str:
        lugar = f" (en {self.ubicacion})" if self.ubicacion else ""
        return f"[{self.categoria}] {self.mensaje}{lugar}"


class ErrorContenido(Exception):
    """La historia no puede jugarse. Contiene todos los problemas encontrados."""

    def __init__(self, problemas: list[Problema]):
        self.problemas = list(problemas)
        super().__init__(self.descripcion())

    def descripcion(self) -> str:
        cantidad = len(self.problemas)
        encabezado = f"La historia no es válida: {cantidad} problema(s) encontrado(s)."
        return "\n".join([encabezado] + [f"  - {p}" for p in self.problemas])

    @property
    def categorias(self) -> set[str]:
        return {p.categoria for p in self.problemas}
