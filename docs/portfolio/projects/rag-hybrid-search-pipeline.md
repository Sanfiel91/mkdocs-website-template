---
title: Hybrid Search RAG Pipeline
description: Enterprise hybrid RAG pipeline combining OpenSearch and Qdrant, achieving a 40% improvement in retrieval accuracy.
image: assets/diagrams/rag-hybrid-search-architecture.png
tags:
  - rag
  - hybrid-search
  - opensearch
  - qdrant
  - langchain
---

# Hybrid Search RAG Pipeline

!!! abstract "Delivery snapshot"
    **Role**: AI Engineer  
    **Sector**: Knowledge-intensive services
    **Goal**: Improve retrieval accuracy across domain-heavy document collections

!!! success "Measured impact"
    - **40% improvement** in domain-specific retrieval accuracy
    - Better handling of exact business terms and semantic intent in the same system
    - Production-grade pipeline serving live knowledge-intensive applications
    - Modular architecture that kept the LLM layer decoupled

!!! info "Core stack"
    <span class="tech-badge">LangChain</span>
    <span class="tech-badge">OpenSearch</span>
    <span class="tech-badge">Qdrant</span>
    <span class="tech-badge">FastAPI</span>
    <span class="tech-badge">Python</span>

<div class="metric-highlight">
  <div class="metric-highlight-item">
    <span class="metric-number">40%</span>
    <span class="metric-label">improvement in domain-specific retrieval accuracy</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">2 engines</span>
    <span class="metric-label">keyword + vector working in fusion</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">Decoupled</span>
    <span class="metric-label">LLM layer independent of retrieval</span>
  </div>
</div>

## Business challenge

Knowledge-intensive applications require highly accurate retrieval from large, domain-specific document collections. Traditional keyword search missed semantic relationships, while pure vector search struggled with exact term matching and structured queries. The client needed a retrieval system that could reliably surface the most relevant information across diverse document types and query patterns.

## Solution overview

![Architecture diagram - Hybrid Search RAG Pipeline](../../assets/diagrams/rag-hybrid-search-architecture.png)
*High-level architecture covering query routing, hybrid retrieval, fusion, and downstream LLM integration.*

I engineered a retrieval architecture that combines vector and keyword search without locking the system into a single strategy:

- **OpenSearch** handles exact terms, BM25 ranking, and structured query patterns.
- **Qdrant** captures semantic similarity and intent beyond literal phrasing.
- **Fusion and re-ranking** combine both result sets to improve relevance for real user questions.
- **LangChain orchestration** manages retrieval, prompting, and downstream LLM interactions.

## Key design decisions

- Retrieval logic lives behind clear interfaces so search strategies can evolve independently of the API layer.
- Exact-match and semantic retrieval are treated as complementary signals, not competing implementations.
- Evaluation focused on query classes and failure modes, making it easier to explain where each improvement came from.

## Results in production

- 40% improvement in domain-specific retrieval accuracy
- Better support for both semantic and keyword-driven questions
- Faster iteration on ranking strategy without changing the API contract
- Cleaner LLM decoupling and easier future model upgrades

## Retrieval playbook

=== "Hybrid retrieval"
    ```python
    bm25_hits = opensearch_client.search(query)
    vector_hits = qdrant_client.search(query_embedding)
    ranked_hits = rerank_and_fuse(bm25_hits, vector_hits)
    ```

=== "API contract"
    ```python
    @app.post("/search")
    async def search(payload: SearchRequest) -> SearchResponse:
        documents = await retrieval_service.retrieve(payload.query)
        return SearchResponse(matches=documents)
    ```

## Why it mattered

This system gave the client a cleaner path from document chaos to grounded answers. It also reduced long-term risk by avoiding over-coupling between retrieval, prompt templates, and the rest of the application.

<div class="cta-panel" markdown>

## Need better retrieval quality before you scale the LLM layer?

If your answers are still inconsistent because search quality is unstable, hybrid retrieval is often the highest-leverage part of the system to fix first.

<div class="cta-actions" markdown>
[Book a free intro call :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="case_rag_intro_call" target="_blank" rel="noopener" }
[Read the RAG playbook :material-arrow-right:](../../blog/posts/hybrid-rag-retrieval-playbook.md){ .md-button }
</div>

</div>
