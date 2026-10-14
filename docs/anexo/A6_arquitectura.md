## A6. Diagrama de componentes por capas

```mermaid
flowchart TB
  subgraph UI["Capa de interfaz"]
    J["jugar.py<br/>argumentos: ruta, --validar, --depurar"]
    CON["interfaz/consola.py<br/>muestra escenas y opciones,<br/>traduce comandos a IDs,<br/>atrapa errores de contenido"]
  end
  subgraph REG["Capa de reglas"]
    SES["motor/sesion.py<br/>estado de la partida, condiciones,<br/>efectos, reinicio, bloqueo"]
  end
  subgraph CONT["Capa de contenido"]
    CAR["motor/cargador.py<br/>lee el archivo y construye el modelo"]
    VAL["motor/validador.py<br/>reglas del contrato, acumula problemas"]
    MOD["motor/modelo.py<br/>Historia, Escena, Opcion (inmutables)"]
    ERR["motor/errores.py<br/>Problema, ErrorContenido"]
  end
  DAT[("historias/*.json")]
  J --> CON
  J --> CAR
  CON -->|"usa"| SES
  SES -->|"consulta"| MOD
  CAR -->|"valida con"| VAL
  CAR -->|"construye"| MOD
  CAR -->|"lanza"| ERR
  VAL -->|"produce"| ERR
  CAR -->|"lee"| DAT
```

Regla de dependencia: las flechas solo apuntan hacia capas inferiores. `motor/` no importa nada de `interfaz/` ni conoce IDs de escenas o nombres de variables de una historia concreta.
