---
title: Sistema de automatización de email con IA
description: Workflow GenAI de automatización de email en producción usando PydanticAI, RAG y FastAPI que redujo el triaje diario de 100+ a 10-15 items accionables.
image: assets/diagrams/email-automation-architecture.png
tags:
  - agentic-ai
  - pydanticai
  - fastapi
  - automation
  - rag
---

# Sistema de automatización de email con IA

!!! abstract "Resumen de entrega"
    **Rol**: AI Engineer
    **Sector**: Turismo y hostelería
    **Objetivo**: Reducir el tiempo dedicado a revisar y priorizar un alto volumen de emails

!!! success "Impacto medible"
    - Reducción del triaje diario de **100+ emails a 10-15 items accionables**
    - Clasificación y priorización automatizada en operaciones reales
    - Sistema desplegado en producción y usado por usuarios
    - Presentado públicamente en **Datamecum Webinar 2025**

!!! info "Stack principal"
    <span class="tech-badge">PydanticAI</span>
    <span class="tech-badge">FastAPI</span>
    <span class="tech-badge">RAG</span>
    <span class="tech-badge">Python</span>
    <span class="tech-badge">Docker</span>
    <span class="tech-badge">Hetzner</span>

<div class="metric-highlight">
  <div class="metric-highlight-item">
    <span class="metric-number">100+ → 15</span>
    <span class="metric-label">emails diarios que requieren revisión humana</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">85%</span>
    <span class="metric-label">reducción en esfuerzo de triaje manual</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">Tiempo real</span>
    <span class="metric-label">clasificación en producción</span>
  </div>
</div>

## Reto de negocio

El cliente estaba desbordado por un alto volumen de emails diarios que requerían revisión manual, clasificación y respuesta. El proceso era lento, propenso a errores y apartaba a perfiles cualificados de tareas de mayor valor. Necesitaban un sistema capaz de entender el contenido del email, clasificar la urgencia y sacar a la superficie solo los items que realmente requerían atención humana.

## Resumen de la solución

![Diagrama de arquitectura - Automatización de email con IA](../../assets/diagrams/email-automation-architecture.png)
*Arquitectura de alto nivel cubriendo ingestión, retrieval, decisiones estructuradas y entrega vía API.*

![Resumen de la solución - Sistema de automatización de email](../../assets/diagrams/email-automation-solution-overview.svg)
*Diagrama de solución end-to-end de la presentación en Datamecum Webinar 2025.*

![Cómo clasifica la IA los emails](../../assets/diagrams/email-classification-flow-es.svg)
*Flujo de clasificación: cómo la IA procesa, clasifica y enruta cada email.*

Diseñé la solución como un workflow de producción y no como un clasificador aislado:

- **Contratos de salida estructurada** con PydanticAI para que el sistema devuelva decisiones validadas y tipadas, no texto libre.
- **Clasificación con RAG** para apoyar las decisiones en políticas, ejemplos y contexto histórico del dominio.
- **Capa de entrega con FastAPI** para procesamiento en tiempo real e integración limpia con sistemas alrededor.
- **Routing determinista** para que la priorización sea consistente entre categorías y edge cases.

## Decisiones clave de diseño

- El workflow separa ingestión, clasificación, formateo de decisiones y entrega para que cada límite se pueda testear y evolucionar de forma independiente.
- Las reglas de negocio y la gestión de confianza viven fuera de la capa de prompt, reduciendo el riesgo de regresiones accidentales.
- La arquitectura sigue principios hexagonales, lo que facilita cambiar estrategias de retrieval o proveedores de modelo sin reescribir el servicio.

## Resultados en producción

- Triaje diario reducido de 100+ items a 10-15 accionables
- Mayor consistencia en clasificación y priorización
- Procesamiento en tiempo real suficientemente rápido para uso operativo
- Arquitectura preparada para futura expansión multi-tenant

## Recorrido técnico

=== "Capa de decisión"
    ```python
    from pydantic import BaseModel
    from pydantic_ai import Agent

    class TriageDecision(BaseModel):
        priority: str
        category: str
        requires_human_review: bool

    agent = Agent(
        model="gpt-4o-mini",
        output_type=TriageDecision,
        system_prompt="Clasifica el email usando políticas y ejemplos de la compañía."
    )
    ```

=== "Capa API"
    ```python
    @app.post("/triage")
    async def triage_email(payload: EmailPayload) -> TriageDecision:
        decision = await triage_service.classify(payload)
        return decision
    ```

## Ver la charla técnica

El proyecto se presentó públicamente en Datamecum Webinar 2025, cubriendo arquitectura de producción, tradeoffs de implementación y resultados operativos.

<div class="embedded-video">
  <a href="https://youtu.be/cECPFYFLAVw?si=dh9k_iqe5bDFC_fv&t=472" target="_blank" rel="noopener" aria-label="Ver Datamecum Webinar 2025 en YouTube">
    <img src="https://img.youtube.com/vi/cECPFYFLAVw/maxresdefault.jpg" alt="Ver Datamecum Webinar 2025 — Automatización de email con IA" loading="lazy">
  </a>
</div>

<div class="cta-panel" markdown>

## ¿Quieres reducir tareas manuales de triaje u operaciones intensivas en documentos?

Si tu equipo dedica demasiado tiempo a revisar comunicaciones entrantes o a priorizar trabajo repetitivo, este es el tipo de patrón de automatización que puedo ayudarte a implementar con seguridad.

<div class="cta-actions" markdown>
[Reserva una llamada gratuita :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="case_email_intro_call_es" target="_blank" rel="noopener" }
[Leer el post relacionado :material-arrow-right:](../../blog/posts/ai-email-automation-webinar.md){ .md-button }
</div>

</div>
