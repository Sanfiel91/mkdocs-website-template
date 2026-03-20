---
title: Agente conversacional de IA para asignación de mesas
description: Backend conversacional en tiempo real que procesa archivos Excel de reservas vía WebSocket, extrae datos de reservas y mesas, ejecuta asignaciones de asientos y responde consultas operativas en lenguaje natural.
image: assets/diagrams/seating-agent-architecture.png
tags:
  - agentic-ai
  - ai-engineering
  - fastapi
  - production-ai
---

# Agente conversacional de IA para asignación de mesas

!!! abstract "Resumen de entrega"
    **Rol**: AI Engineer(con un equipo de producto multifuncional)<br>
    **Sector**: Hostelería y operaciones de restauración<br>
    **Objetivo**: Reemplazar workflows manuales de asignación de mesas con un backend conversacional de IA que procesa archivos, aplica reglas de negocio y responde consultas operativas en tiempo real

!!! success "Impacto medible"
    - **Procesamiento de archivos en tiempo real** - Uploads de Excel parseados, validados y estructurados en una sola interacción WebSocket
    - **IA híbrida + lógica determinista** - El LLM gestiona interpretación y extracción; las reglas de negocio gestionan la asignación
    - **Operaciones conversacionales** - Personal no técnico consulta estado de reservas, disponibilidad de mesas y asignaciones en lenguaje natural
    - **Continuidad de sesión** - Historial de conversación completo persistido en DynamoDB entre sesiones

!!! info "Stack principal"
    <span class="tech-badge">PydanticAI</span>
    <span class="tech-badge">Gemini 2.5 Flash</span>
    <span class="tech-badge">FastAPI</span>
    <span class="tech-badge">WebSockets</span>
    <span class="tech-badge">DynamoDB</span>
    <span class="tech-badge">Keycloak</span>
    <span class="tech-badge">Docker</span>

<div class="metric-highlight">
  <div class="metric-highlight-item">
    <span class="metric-number">Tiempo real</span>
    <span class="metric-label">procesamiento de Excel vía WebSocket</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">Híbrido</span>
    <span class="metric-label">extracción IA + asignación determinista</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">Persistente</span>
    <span class="metric-label">continuidad de sesión entre reconexiones</span>
  </div>
</div>

## Reto

Los equipos de operaciones de restaurantes y venues gestionan el seating a través de una mezcla de hojas de cálculo, coordinación manual y conocimiento institucional. El workflow típico implica recibir archivos Excel con reservas y layouts de mesas, cruzar manualmente nombres y tamaños de grupo, aplicar restricciones de capacidad, gestionar registros duplicados y comunicar asignaciones - todo bajo presión de tiempo antes de que empiece el servicio.

Los pain points eran consistentes: formatos Excel heterogéneos con estructuras variables y múltiples hojas, registros duplicados de comensales dispersos entre entradas, ninguna forma estructurada de consultar el estado actual de las asignaciones, y un proceso que dependía enteramente de la memoria y atención al detalle del operador.

Necesitaban un sistema capaz de ingestar archivos Excel desordenados, extraer datos limpios de reservas y mesas, ejecutar asignaciones basadas en reglas, y permitir al equipo de operaciones hacer preguntas en lenguaje natural - todo a través de una sola interfaz, en tiempo real.

## Resumen de la solución

![Diagrama de arquitectura - Agente conversacional de IA para asignación de mesas](../../assets/diagrams/seating-agent-architecture.png)

Diseñé el sistema como un **backend conversacional de IA** que combina inteligencia LLM para comprensión y extracción con lógica determinista para decisiones de asignación críticas de negocio.

### Interfaz WebSocket en tiempo real

- El equipo de operaciones se conecta vía **WebSocket** (FastAPI + Uvicorn) y envía mensajes con archivos Excel/CSV opcionales adjuntos.
- Cada conexión se autentica vía **JWT validado por Keycloak** antes de que comience cualquier procesamiento.
- El sistema soporta tanto interacciones basadas en archivos (subir y procesar) como consultas puramente conversacionales (preguntar sobre el estado actual) a través de la misma interfaz.

### Agente de IA con tools de dominio

- Un **agente PydanticAI impulsado por Gemini 2.5 Flash** orquesta el workflow, decidiendo qué tools de dominio invocar según la intención del usuario y los archivos adjuntos.
- **Prompts dinámicos vía Jinja2** adaptan el comportamiento del agente al contexto actual - ya sea que el usuario esté subiendo un nuevo archivo, preguntando sobre una reserva específica, o solicitando una asignación de mesas.
- El agente tiene acceso a tools especializados para análisis de Excel, extracción de reservas, extracción de mesas, asignación de asientos y consultas operativas.

### Procesamiento de archivos y extracción de datos

- El sistema analiza la **estructura del archivo Excel** incluyendo escenarios multi-hoja, detectando qué hojas contienen reservas y cuáles contienen layouts de mesas.
- La **extracción de reservas** gestiona formatos heterogéneos, identifica campos relevantes y agrupa registros que representan a la misma persona entre entradas duplicadas (matching por nombre, email o teléfono).
- La **extracción de mesas** mapea el seating disponible con restricciones de capacidad y metadatos de layout.

### Asignación determinista de mesas

- Una vez extraídas reservas y mesas, un **motor heurístico de asignación** aplica restricciones de capacidad y reglas de negocio para producir un plan de seating.
- Esta capa es completamente determinista - sin intervención del LLM en la lógica de asignación real. La IA interpreta y extrae; las reglas deciden.
- Los resultados se devuelven como datos estructurados que el frontend o sistema downstream puede consumir directamente.

### Consultas conversacionales y continuidad de sesión

- Después del procesamiento, el equipo de operaciones puede consultar el sistema en lenguaje natural: "¿Cuántas reservas sin asignar quedan?", "¿Qué mesa tiene más capacidad?", "Muéstrame todas las reservas de García."
- El **historial de conversación se persiste en DynamoDB** por sesión de chat, para que el usuario pueda desconectarse y retomar después sin perder contexto.
- **Caché en memoria por chat_id** mantiene los datos de acceso frecuente rápidos para consultas de seguimiento dentro de la misma sesión.

## Decisiones clave de diseño

- **Enfoque híbrido IA + determinista.** El LLM gestiona lo que hace bien - entender inputs desordenados, extraer datos estructurados de archivos no estructurados, y habilitar interacción en lenguaje natural. Pero la asignación real de mesas es determinista. Las decisiones críticas de negocio no dependen de outputs probabilísticos del modelo.
- **Arquitectura WebSocket-first.** Upload de archivos, procesamiento e interacción conversacional ocurren a través de una única conexión persistente. Esto elimina el overhead de múltiples round-trips HTTP y permite streaming en tiempo real de resultados conforme avanza el procesamiento.
- **Autenticación antes del procesamiento.** La validación JWT vía Keycloak ocurre en el momento de la conexión, antes de que se procese ningún mensaje. Esto mantiene el perímetro de seguridad limpio y previene que requests no autenticados lleguen a la capa de IA.
- **Persistencia de sesión para continuidad operativa.** DynamoDB almacena el historial completo de conversación por chat, para que el sistema pueda restaurar contexto entre sesiones. Combinado con caché en memoria, esto significa respuestas rápidas para consultas de seguimiento sin reprocesar archivos.
- **Ingestión de archivos flexible en esquema.** El sistema no requiere una plantilla Excel fija. Analiza la estructura de cualquier archivo que se suba - incluyendo workbooks multi-hoja con formatos inconsistentes - y adapta la extracción en consecuencia. Esto es crítico en hostelería donde cada venue tiene sus propias convenciones de hoja de cálculo.

## Resultados en producción

- Procesamiento en tiempo real de archivos Excel heterogéneos a través de una única interfaz WebSocket
- Extracción automatizada y deduplicación de registros de reservas en formatos inconsistentes
- Asignación determinista de mesas con restricciones de capacidad y reglas de negocio
- Interfaz de consulta en lenguaje natural accesible para personal de operaciones no técnico
- Continuidad de sesión completa con historial de conversación persistente entre reconexiones
- Acceso autenticado con JWT/Keycloak garantizando operación segura multi-usuario

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| API y comunicación en tiempo real | FastAPI, Uvicorn, WebSockets |
| Agente IA y orquestación | PydanticAI, Gemini 2.5 Flash, prompts dinámicos Jinja2 |
| Procesamiento de archivos | pandas, openpyxl |
| Lógica de asignación | Motor heurístico determinista (Python) |
| Autenticación | JWT, Keycloak |
| Persistencia y caché | DynamoDB (historial), caché en memoria por chat_id |
| Infraestructura | Docker, despliegue containerizado |
| Calidad | pytest, pytest-asyncio, ruff |

<div class="cta-panel" markdown>

## ¿Gestionando operaciones con hojas de cálculo y coordinación manual?

Si tu equipo dedica tiempo antes de cada servicio a procesar manualmente archivos de reservas, cruzar capacidades y responder preguntas de estado de memoria - y la lógica está clara pero la ejecución sigue siendo manual - este es el tipo de sistema que construyo.

<div class="cta-actions" markdown>
[Reserva una llamada gratuita :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="case_seating_intro_call_es" target="_blank" rel="noopener" }
</div>

</div>
