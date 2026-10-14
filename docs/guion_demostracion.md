# Guion de la demostración (video MP4, máximo 6 minutos)

Grabación de pantalla de la consola con letra grande (tamaño 18 o más), sin cámara. Se explica con voz o con rótulos. Antes de grabar: `python -m pip install -r requirements.txt` y abrir una terminal en la carpeta del proyecto.

| # | Tiempo | Quién | Qué mostrar (comando y entradas) | Qué decir o rotular |
|---|---|---|---|---|
| 1 | 0:00-0:20 | Camilo | Pantalla con el README abierto | "Motor de historias interactivas en Python, por consola. Integrantes: Camilo Conde y Miguel Jacome." |
| 2 | 0:20-1:30 | Camilo | `python jugar.py historias/la_ultima_transmision.json --depurar` → `1` `1` `1` (E4); `r`; `1` `2` `1` (E5); `r`; `1` `2` `2` (E6) | "Los tres finales. `--depurar` muestra las variables. Al reiniciar todo vuelve a E1 en falso." |
| 3 | 1:30-2:10 | Miguel | Mismo programa: `1` `1` (en E3 aparece "Activar con código"); `r`; `1` `2` (en E3 aparece "Activar sin verificar"); escribir `activar_codigo` | "La condición `conoce_origen` cambia las opciones de E3. Si se envía el ID de una opción no habilitada, el motor la rechaza y el estado no cambia (CA02)." |
| 4 | 2:10-2:50 | Miguel | `python jugar.py historias/el_faro.json --depurar` → `1` `1` (F3); `r`; `2` `1` (F4) | "Segunda historia con otros IDs y otra variable, con el mismo motor y sin cambiar código." |
| 5 | 2:50-3:25 | Miguel | `python jugar.py --validar historias/invalidas/destino_inexistente.json` | "Error de destino inexistente: indica la categoría, la escena, la opción y E99, y no abre la partida (CA03)." |
| 6 | 3:25-4:05 | Camilo | `python -m pytest` y luego `python scripts/verificar_rnf.py` | "70 pruebas aprobadas: U1 a U6 e I1, más la verificación de los tres RNF." |
| 7 | 4:05-5:05 | Camilo | `python jugar.py historias/la_ultima_transmision.json --depurar` → `1` `1` (E3, conoce_origen verdadero) → `d` (E2, falso) → `d` ("No hay una decisión para deshacer") → `2` (E3 con "Activar sin verificar") → `2` (E6) → `d` (vuelve a E3) | "Solicitud de cambio: deshacer restaura la escena y todas las variables, es de un solo nivel y funciona desde un final." |
| 8 | 5:05-5:50 | Miguel | Diagrama de componentes (Anexo A6) | "Decisión de arquitectura ADR-01: contenido, reglas e interfaz separados. Impacto del cambio: solo se tocó `motor/sesion.py` y la consola; el cargador, el validador y el formato JSON no cambiaron (sección 7)." |
