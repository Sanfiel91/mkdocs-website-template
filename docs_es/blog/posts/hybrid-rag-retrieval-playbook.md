---
title: Playbook de retrieval para RAG híbrido
date: 2025-05-09
authors:
  - aesanfiel
categories:
  - RAG
  - Arquitectura
tags:
  - rag
  - hybrid-search
  - opensearch
  - qdrant
  - retrieval
description: Por qué el retrieval híbrido suele superar a la búsqueda vectorial pura en producción y cómo estructurar el sistema para evolucionar el ranking con seguridad.
image: assets/diagrams/rag-hybrid-search-architecture.png
---

# Playbook de retrieval para RAG híbrido

Muchos sistemas RAG decepcionan por la misma razón: el equipo trata retrieval como una única decisión de implementación en lugar de como una capacidad de producto que debe evolucionar. En la práctica, distintas clases de consulta necesitan fortalezas distintas.

<!-- more -->

## Por qué la búsqueda vectorial pura se queda corta

La búsqueda vectorial es potente, pero no es suficiente por sí sola cuando los usuarios esperan:

- matching exacto de acrónimos y nombres de producto
- tratamiento fiable de terminología de negocio estructurada
- buen rendimiento en consultas cortas y poco especificadas

Ahí es donde keyword retrieval y semantic retrieval dejan de competir y empiezan a complementarse.

## El stack de retrieval en el que más confío

- **Keyword retrieval** para términos exactos, filtros y terminología explícita
- **Vector retrieval** para intención, paráfrasis y similitud semántica
- **Fusión o reranking** para reconciliar ambos conjuntos de resultados
- **Evaluación por clase de consulta** para que el trabajo de mejora sea medible

## Un patrón de arquitectura seguro

=== "Composición de retrieval"
    ```python
    keyword_results = keyword_index.search(query)
    vector_results = vector_index.search(query_embedding)
    results = rank_fusion(keyword_results, vector_results)
    ```

=== "Contrato hacia el LLM"
    ```python
    context = retrieval_service.build_context(query)
    answer = llm.generate(question=query, context=context)
    ```

## Lo que muchos equipos pasan por alto

- La calidad de retrieval debe evaluarse antes de que el prompt tuning se convierta en la respuesta por defecto.
- Los query logs importan más que ejemplos de benchmark copiados de un notebook.
- La capa LLM no debería saber si el resultado ganador vino de BM25, de vectores o de ambos.

Ese desacoplamiento es lo que hace posible mejorar search sin desestabilizar el resto de la aplicación.

## Preguntas de evaluación que merece la pena hacerse

1. ¿Qué clases de consulta siguen fallando más a menudo?
2. ¿Los fallos vienen de falta de recall o de mal ranking?
3. ¿Alguna fuente necesita mejor chunking o metadatos antes de tocar los prompts?
4. ¿Puede la capa de retrieval explicar por qué se eligió un resultado?

El objetivo del retrieval híbrido no es la complejidad por la complejidad. Es la relevancia controlable.

Si tu sistema RAG actual sigue sintiéndose inconsistente, [reserva una llamada inicial](https://calendly.com/andresesanfiel/introduction-call){ .track-conversion data-conversion-label="post_rag_intro_call_es" target="_blank" rel="noopener" }. La calidad de retrieval suele ser el punto más limpio para desbloquear valor.
