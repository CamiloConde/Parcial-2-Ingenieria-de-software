## A1. Diagrama de contexto

```mermaid
flowchart LR
  ESC(["Escritora / Diseñador"])
  LEC(["Lector"])
  COO(["Coordinadora del festival"])
  SIS[["Motor de historias interactivas<br/>(programa de consola local)"]]
  ARC[("Archivos de historia<br/>historias/*.json")]
  ESC -- "escribe y edita" --> ARC
  ESC -- "valida archivo (--validar)" --> SIS
  LEC -- "elige opciones, reinicia" --> SIS
  COO -- "ejecuta en el evento" --> SIS
  SIS -- "lee y valida" --> ARC
  SIS -- "escena, opciones, desenlace, errores" --> LEC
  SIS -- "lista de errores con categoría e ID" --> ESC
```

## A2. Diagrama de casos de uso

```mermaid
flowchart LR
  ESC(("Escritora"))
  LEC(("Lector"))
  subgraph S["Sistema: motor de historias"]
    CU1(["CU01 Validar historia"])
    CU2(["CU02 Iniciar partida"])
    CU3(["CU03 Elegir opción"])
    CU4(["CU04 Reiniciar partida"])
    CU5(["CU05 Reconocer desenlace"])
    CU7(["CU07 Cargar historia"])
  end
  ESC --- CU1
  LEC --- CU2
  LEC --- CU3
  LEC --- CU4
  LEC --- CU5
  CU2 -. "«include»" .-> CU7
  CU7 -. "«include»" .-> CU1
  CU5 -. "«extend»" .-> CU3
```

| Caso de uso | RF relacionados |
|---|---|
| CU01 Validar historia | RF11, RF12, RF13 |
| CU02 Iniciar partida / CU07 Cargar historia | RF01, RF02, RF03, RF04 |
| CU03 Elegir opción | RF04, RF05, RF06, RF07, RF08, RF14 |
| CU04 Reiniciar partida | RF10, RF14 |
| CU05 Reconocer desenlace | RF09 |

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
    +escena_actual Escena
    +variables dict
    +terminada bool
    +bloqueada bool
    +opciones_disponibles() list[Opcion]
    +elegir(id_opcion) Resultado
    +reiniciar() Resultado
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
    S->>S: aplica efectos (conoce_origen = verdadero)
    S->>S: escena_id = destino (E3)
    S-->>C: Resultado(aceptada = verdadero)
    C-->>L: muestra E3 y sus opciones habilitadas
  else inexistente o no habilitada
    S-->>C: Resultado(aceptada = falso, motivo)
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
  EnCurso --> EnCurso : opción válida hacia escena no final / aplica efectos
  EnCurso --> EnCurso : entrada inválida / sin cambios
  EnCurso --> Finalizada : opción válida hacia escena final
  EnCurso --> Bloqueada : escena no final sin opciones habilitadas
  EnCurso --> EnCurso : reiniciar
  Finalizada --> EnCurso : reiniciar
  Bloqueada --> EnCurso : reiniciar
  Finalizada --> [*] : salir
  Bloqueada --> [*] : salir
  EnCurso --> [*] : salir
```
