## 9. Aportes, fuentes y herramientas de apoyo

**Declaración de aportes** (verificable en `evidencias/historial_git.txt`, por autor de cada commit).

| Integrante | Aportes | Evidencia en el historial |
|---|---|---|
| Camilo Conde Corrales | Alcance, riesgos y proceso; requisitos y su corrección tras la revisión; modelos y arquitectura; implementación de las capas de contenido, reglas e interfaz; pruebas U1-U6 e I1; verificación de RNF; análisis e implementación del cambio SC01; README e informe | Commits de "Estructura inicial…" a "SC01: actualiza modelos…", la corrección D2 y la generación de evidencias |
| Miguel Jacome y Yanez | Revisión cruzada de requisitos (D1 de RF04 en programación en pareja, y D2: criterios de RF09 y RF14 desactualizados tras SC01); redacción final de la segunda historia; ejecución de pruebas y RNF en un segundo equipo (Windows, Python 3.12); tablero Kanban en Trello y sus capturas; grabación del video | Commits "Revisión cruzada de requisitos RF01-RF17", "Ajusta redacción de El faro de Punta Gris" y "Ejecución en segundo equipo: pruebas y RNF" |

Ambos integrantes revisaron el informe final y prepararon la demostración.

**Fuentes.** Documentación oficial de Python 3 (`json`, `dataclasses`, `argparse`); documentación de pytest (parametrización y `tmp_path`); sintaxis de diagramas de Mermaid y de PlantUML. No se reutilizaron fragmentos de código de tutoriales ni de otros proyectos.

**Herramientas de IA.** Se utilizó un asistente de IA conversacional (Claude, de Anthropic) para: (a) proponer alternativas de proceso, arquitectura, RNF y mecanismo de deshacer, que los integrantes evaluaron y aprobaron; (b) redactar borradores de la documentación y los diagramas; (c) generar una primera versión del código, las pruebas y los scripts de verificación. **Cómo se verificaron sus resultados:** cada artefacto se contrastó con la guía y con el anexo de la hora 6; se ejecutaron las 70 pruebas automatizadas y el script de RNF en dos equipos; se recorrieron a mano los tres finales, la segunda historia y el error `E99`; y la revisión cruzada (D1, D2) y la verificación de RNF03 (dígitos Unicode) encontraron defectos que se corrigieron. El trabajo de los integrantes consistió en las decisiones, la revisión y la verificación; el material generado con apoyo de la herramienta se distingue en esta declaración.
