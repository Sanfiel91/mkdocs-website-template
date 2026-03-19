---
title: Pipeline RAG con búsqueda híbrida
description: Pipeline RAG híbrido para entorno enterprise que combina OpenSearch y Qdrant, logrando una mejora del 40% en precisión de retrieval.
image: assets/diagrams/rag-hybrid-search-architecture.png
tags:
  - rag
  - hybrid-search
  - opensearch
  - qdrant
  - langchain
---

# Pipeline RAG con búsqueda híbrida

!!! abstract "Resumen de entrega"
    **Rol**: AI Engineer
    **Sector**: Servicios intensivos en conocimiento
    **Objetivo**: Mejorar la precisión de retrieval sobre colecciones documentales muy orientadas a dominio

!!! success "Impacto medible"
    - **40% de mejora** en precisión de retrieval por dominio
    - Mejor gestión de términos exactos de negocio e intención semántica en el mismo sistema
    - Pipeline de nivel producción sirviendo aplicaciones reales intensivas en conocimiento
    - Arquitectura modular que mantuvo desacoplada la capa LLM

!!! info "Stack principal"
    <span class="tech-badge">LangChain</span>
    <span class="tech-badge">OpenSearch</span>
    <span class="tech-badge">Qdrant</span>
    <span class="tech-badge">FastAPI</span>
    <span class="tech-badge">Python</span>

<div class="metric-highlight">
  <div class="metric-highlight-item">
    <span class="metric-number">40%</span>
    <span class="metric-label">mejora en precisión de retrieval por dominio</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">2 motores</span>
    <span class="metric-label">keyword + vector en fusión</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">Desacoplado</span>
    <span class="metric-label">capa LLM independiente del retrieval</span>
  </div>
</div>

## Reto de negocio

Las aplicaciones intensivas en conocimiento requieren retrieval muy preciso sobre grandes colecciones documentales de dominio específico. La keyword search tradicional perdía relaciones semánticas, mientras que la búsqueda vectorial pura sufría con términos exactos y consultas estructuradas. El cliente necesitaba un sistema de retrieval que sacara con fiabilidad la información más relevante para distintos tipos de documentos y patrones de consulta.

## Resumen de la solución

![Diagrama de arquitectura - Pipeline RAG híbrido](../../assets/diagrams/rag-hybrid-search-architecture.png)
*Arquitectura de alto nivel cubriendo query routing, retrieval híbrido, fusión e integración downstream con LLM.*

Diseñé una arquitectura de retrieval que combina vector y keyword search sin bloquear el sistema en una sola estrategia:

- **OpenSearch** gestiona términos exactos, ranking BM25 y patrones de consulta estructurados.
- **Qdrant** captura similitud semántica e intención más allá del texto literal.
- **Fusión y re-ranking** combinan ambos conjuntos de resultados para mejorar la relevancia en preguntas reales.
- **Orquestación con LangChain** gestiona retrieval, prompting e interacciones downstream con el LLM.

## Decisiones clave de diseño

- La lógica de retrieval vive detrás de interfaces claras para que las estrategias de búsqueda evolucionen de forma independiente a la capa API.
- El matching exacto y el retrieval semántico se tratan como señales complementarias, no como implementaciones en competencia.
- La evaluación se centró en clases de consulta y failure modes, lo que facilitó explicar de dónde venía cada mejora.

## Resultados en producción

- 40% de mejora en precisión de retrieval por dominio
- Mejor soporte para preguntas tanto semánticas como guiadas por keywords
- Iteración más rápida sobre estrategia de ranking sin cambiar el contrato API
- Desacoplamiento más limpio del LLM y mayor facilidad para futuras mejoras de modelo

## Playbook de retrieval

=== "Retrieval híbrido"
    ```python
    bm25_hits = opensearch_client.search(query)
    vector_hits = qdrant_client.search(query_embedding)
    ranked_hits = rerank_and_fuse(bm25_hits, vector_hits)
    ```

=== "Contrato API"
    ```python
    @app.post("/search")
    async def search(payload: SearchRequest) -> SearchResponse:
        documents = await retrieval_service.retrieve(payload.query)
        return SearchResponse(matches=documents)
    ```

## Por qué importó

Este sistema dio al cliente un camino mucho más limpio desde el caos documental hasta respuestas mejor fundamentadas. También redujo riesgo a largo plazo al evitar un acoplamiento excesivo entre retrieval, prompt templates y el resto de la aplicación.

<div class="cta-panel" markdown>

## ¿Necesitas mejorar la calidad de retrieval antes de escalar la capa LLM?

Si tus respuestas siguen siendo inconsistentes porque la calidad de búsqueda es inestable, el retrieval híbrido suele ser la parte de mayor impacto para arreglar primero.

<div class="cta-actions" markdown>
[Reserva una llamada gratuita :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="case_rag_intro_call_es" target="_blank" rel="noopener" }
[Leer el playbook de RAG :material-arrow-right:](../../blog/posts/hybrid-rag-retrieval-playbook.md){ .md-button }
</div>

</div>
