## A8. Mapa narrativo de las historias (datos de entrada, no modelo del software)

```mermaid
flowchart LR
  E1["E1 La señal"] -- "revisar" --> E2["E2 El archivo"]
  E2 -- "investigar<br/>conoce_origen = V" --> E3["E3 La respuesta"]
  E2 -- "continuar" --> E3
  E3 -- "activar_codigo<br/>[conoce_origen = V]<br/>confia_en_la_voz = V" --> E4(["E4 Rescate (final)"])
  E3 -- "activar_sin_verificar<br/>[conoce_origen = F]<br/>confia_en_la_voz = V" --> E5(["E5 El eco (final)"])
  E3 -- "cortar<br/>confia_en_la_voz = F" --> E6(["E6 Silencio (final)"])
  F1["F1 La tormenta"] -- "cobertizo<br/>tiene_llave = V" --> F2["F2 La puerta"]
  F1 -- "correr" --> F2
  F2 -- "abrir [tiene_llave = V]" --> F3(["F3 La luz vuelve (final)"])
  F2 -- "esperar" --> F4(["F4 Amanecer (final)"])
```

## A9. Tablero Kanban: capturas inicial y final

Tablero en GitHub Projects con las columnas *Backlog → Por hacer → En progreso (WIP 2) → Revisión → Hecho* y las tarjetas B01-B14 de la sección 2 del informe, cada una con su responsable.

**Captura inicial** (inicio del parcial, todas las tarjetas en *Backlog* o *Por hacer*):

![Tablero inicial](../../evidencias/capturas/tablero_inicial.png)

**Captura final** (cierre, tarjetas en *Hecho*; B12 y B13 agregadas al recibir la solicitud de cambio):

![Tablero final](../../evidencias/capturas/tablero_final.png)
