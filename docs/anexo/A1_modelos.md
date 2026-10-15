## A1. Diagrama de contexto

![Diagrama de contexto](diagramas/contexto.svg)

*Fuente: `docs/anexo/diagramas/contexto.puml` (PlantUML).*

## A2. Diagrama de casos de uso

![Diagrama de casos de uso](diagramas/casos_de_uso.svg)

*Fuente: `docs/anexo/diagramas/casos_de_uso.puml` (PlantUML). La Coordinadora del festival no tiene casos de uso propios: opera el programa (diagrama de contexto).*

| Caso de uso | RF relacionados |
|---|---|
| CU01 Validar historia | RF11, RF12, RF13 |
| CU02 Iniciar partida / CU07 Cargar historia | RF01, RF02, RF03, RF04 |
| CU03 Elegir opción | RF04, RF05, RF06, RF07, RF08, RF14 |
| CU04 Reiniciar partida | RF10, RF14 |
| CU05 Reconocer desenlace | RF09 |
| CU06 Deshacer última decisión (SC01) | RF15, RF16, RF17 |

## A3. Diagrama de clases del dominio

```mermaid
classDiagram
  direction LR
  class Historia {
    +titulo: str
    +inicio: str
    +variables: dict[str, bool]
    +escenas: dict[str, Escena]
    +escena(id) Escena
  }
  class Escena {
    +id: str
    +texto: str
    +final: bool
    +opciones: tuple[Opcion]
  }
  class Opcion {
    +id: str
    +texto: str
    +destino: str
    +condiciones: dict[str, bool]
    +efectos: dict[str, bool]
    +habilitada(variables) bool
  }
  class Sesion {
    -historia: Historia
    -escena_id: str
    -variables: dict[str, bool]
    -anterior: EstadoSesion | None
    +escena_actual Escena
    +variables dict
    +terminada bool
    +bloqueada bool
    +puede_deshacer bool
    +opciones_disponibles() list[Opcion]
    +elegir(id_opcion) Resultado
    +deshacer() Resultado
    +reiniciar() Resultado
  }
  class EstadoSesion {
    <<inmutable>>
    +escena_id: str
    +variables: tuple
  }
  class Resultado {
    +aceptada: bool
    +mensaje: str
  }
  class Problema {
    +categoria: str
    +mensaje: str
    +ubicacion: str
  }
  class ErrorContenido {
    +problemas: list[Problema]
  }
  Historia "1" *-- "1..*" Escena
  Escena "1" *-- "0..*" Opcion
  Sesion "0..*" --> "1" Historia : interpreta
  Sesion ..> Resultado : devuelve
  Sesion "1" o-- "0..1" EstadoSesion : anterior
  ErrorContenido "1" o-- "1..*" Problema
```

## A4. Diagrama de secuencia: elegir una opción

```mermaid
sequenceDiagram
  actor L as Lector
  participant C as Consola
  participant S as Sesion
  participant O as Opcion
  L->>C: escribe "1"
  C->>S: opciones_disponibles()
  S-->>C: [investigar, continuar]
  C->>C: traduce "1" a id "investigar"
  C->>S: elegir("investigar")
  S->>S: busca opción en escena actual
  S->>O: habilitada(variables)
  O-->>S: verdadero
  alt opción existe y está habilitada
    S->>S: anterior = EstadoSesion(E2, variables)
    S->>S: aplica efectos (conoce_origen = verdadero)
    S->>S: escena_id = destino (E3)
    S-->>C: Resultado(aceptada = verdadero)
    C-->>L: muestra E3 y sus opciones habilitadas
  else inexistente o no habilitada
    S-->>C: Resultado(aceptada = falso, motivo) · anterior sin cambios
    C-->>L: muestra motivo, escena sin cambios
  end
```

## A5. Diagrama de estados de una sesión

```mermaid
stateDiagram-v2
  [*] --> Validando : cargar archivo
  Validando --> Rechazada : errores de contenido
  Rechazada --> [*]
  Validando --> EnCurso : historia válida / escena = inicio, variables iniciales
  EnCurso --> EnCurso : opción válida a escena no final / aplica efectos<br/>entrada inválida / sin cambios<br/>reiniciar / borra historial<br/>deshacer [hay anterior] / restaura instantánea
  EnCurso --> Finalizada : opción válida a escena final
  EnCurso --> Bloqueada : escena no final sin opciones habilitadas
  Finalizada --> EnCurso : reiniciar / borra historial<br/>deshacer [hay anterior] / restaura instantánea
  Bloqueada --> EnCurso : reiniciar / borra historial<br/>deshacer [hay anterior] / restaura instantánea
  EnCurso --> [*] : salir
  Finalizada --> [*] : salir
  Bloqueada --> [*] : salir
```
