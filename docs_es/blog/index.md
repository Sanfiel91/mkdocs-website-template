---
title: Blog e ideas prácticas
description: Notas prácticas sobre agentic AI, retrieval híbrido y entrega de IA en producción.
image: assets/diagrams/ai-api-platform-architecture.png
tags:
  - blog
  - agentic-ai
  - rag
  - fastapi
---

# Blog e ideas prácticas

Aquí publico notas de implementación, lecciones de arquitectura y heurísticas de entrega extraídas de construir sistemas de IA que tienen que funcionar fuera del entorno demo.

El foco es práctico: cómo hacer workflows agentic más fiables, cómo mejorar la calidad de retrieval y cómo poner en producción APIs de IA que un equipo interno pueda operar.

## Qué vas a encontrar aquí

<div class="grid cards" markdown>

-   :material-robot:{ .lg .middle } **Diseño de workflows agentic**

    ---

    Patrones de orquestación determinista, límites de uso de tools, revisión humana y contención de fallos.

-   :material-database-search:{ .lg .middle } **RAG y retrieval híbrido**

    ---

    Decisiones prácticas sobre ranking, fusión, evaluación y por qué muchos sistemas RAG rinden por debajo de lo esperado en producción.

-   :material-api:{ .lg .middle } **Entrega de IA en producción**

    ---

    Contratos API, diseño de servicios con FastAPI, límites de despliegue, observabilidad y qué cambia cuando llegan usuarios reales.

</div>

<div class="topic-links">
  <a href="../tags/">Todos los temas</a>
  <a href="../portfolio/">Casos de estudio</a>
  <a href="posts/agentic-ai-workflows-production-playbook/">Agentic AI</a>
  <a href="posts/hybrid-rag-retrieval-playbook/">RAG</a>
  <a href="posts/shipping-ai-apis-with-fastapi/">Entrega</a>
</div>

## Posts destacados

<div class="grid cards" markdown>

-   [Automatización de email con IA: del caos a la acción](posts/ai-email-automation-webinar.md)

    ---

    La versión pública, vía webinar, de un sistema de automatización de email en producción construido con PydanticAI, RAG y FastAPI.

-   [Playbook de producción para workflows agentic AI](posts/agentic-ai-workflows-production-playbook.md)

    ---

    Una checklist práctica para decidir qué debe seguir siendo determinista, qué puede delegarse al modelo y cómo mantener el sistema testeable.

-   [Playbook de retrieval para RAG híbrido](posts/hybrid-rag-retrieval-playbook.md)

    ---

    Por qué el retrieval híbrido suele funcionar mejor que la búsqueda vectorial pura y cómo estructurar el sistema para evolucionar el ranking con seguridad.

-   [Cómo poner en producción APIs de IA con FastAPI](posts/shipping-ai-apis-with-fastapi.md)

    ---

    Límites de servicio, contratos streaming, procesamiento en background y detalles operativos que importan cuando el tráfico ya es real.

</div>

<div class="cta-panel" markdown>

## ¿Quieres aplicar estas ideas a un sistema real en vez de dejarlas en un hilo de blog?

Si tu equipo ya está experimentando con IA pero necesita decisiones de arquitectura más sólidas, ese es exactamente el gap que ayudo a cerrar.

<div class="cta-actions" markdown>
[Reserva una llamada inicial :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="blog_intro_call_es" target="_blank" rel="noopener" }
[Ver el portfolio :material-arrow-right:](../portfolio/index.md){ .md-button }
</div>

</div>

## Últimos posts
