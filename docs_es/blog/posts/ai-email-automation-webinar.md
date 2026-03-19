---
title: Automatización de email con IA - del caos a la acción
date: 2025-01-01
pin: true
authors:
  - aesanfiel
categories:
  - Ponencias
  - Delivery
tags:
  - pydanticai
  - rag
  - fastapi
  - automation
description: Mira mi charla de Datamecum Webinar 2025 sobre cómo construí un sistema GenAI de automatización de email en producción con PydanticAI, RAG y FastAPI.
image: assets/diagrams/email-automation-architecture.png
---

# Automatización de email con IA: del caos a la acción

Tuve la oportunidad de presentar en Datamecum Webinar 2025, donde expliqué cómo construí un sistema GenAI de automatización de email en producción que redujo el triaje diario de 100+ items a 10-15 accionables.

<!-- more -->

## Por qué conectó esta charla

El sistema atacaba un problema que muchos equipos reconocen al instante: trabajo operativo repetitivo y de alto volumen que parece sencillo por fuera pero se vuelve caótico cuando entran en juego la urgencia, el contexto de negocio y las reglas de handoff.

## Qué cubre la sesión

- **El problema**: por qué el triaje manual consume horas de tiempo productivo cada día
- **La capa de decisión**: cómo PydanticAI ayudó a mantener outputs estructurados y fiables
- **La capa de grounding**: cómo retrieval mejoró la calidad de clasificación
- **La capa de entrega**: cómo FastAPI convirtió el workflow en un servicio operativo

## Ver la presentación completa

[![Watch on YouTube](https://img.youtube.com/vi/cECPFYFLAVw/maxresdefault.jpg)](https://youtu.be/cECPFYFLAVw?si=dh9k_iqe5bDFC_fv&t=472){ target="_blank" rel="noopener" }

*Haz clic en la imagen para ver la presentación completa en YouTube.*

## Puntos destacados de arquitectura

=== "Contrato de decisión"
    ```python
    class EmailDecision(BaseModel):
        category: str
        priority: str
        next_action: str
    ```

=== "Límite de servicio"
    ```python
    @app.post("/emails/triage")
    async def triage(payload: EmailBatch) -> list[EmailDecision]:
        return await triage_service.run(payload)
    ```

## Ideas clave

1. Las salidas estructuradas importan porque los sistemas en producción necesitan decisiones predecibles, no solo texto bonito.
2. Retrieval mejora la confianza cuando el modelo debe clasificar usando contexto y políticas específicas de la compañía.
3. El workflow debe diseñarse como un servicio de aplicación, no como un prompt aislado.

Si te interesa construir sistemas parecidos de automatización con IA, puedes [reservar una llamada gratuita](https://calendly.com/andresesanfiel/introduction-call){ .track-conversion data-conversion-label="post_email_intro_call_es" target="_blank" rel="noopener" }.
