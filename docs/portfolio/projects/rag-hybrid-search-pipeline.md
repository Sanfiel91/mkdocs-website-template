---
title: Hybrid Search RAG Pipeline
description: Enterprise hybrid RAG pipeline combining OpenSearch and Qdrant, achieving a 40% improvement in retrieval accuracy.
---

# Hybrid Search RAG Pipeline

!!! abstract "Case Study Summary"
    **Role**: AI Engineer
    **Company**: Sala Scala - The Wise Dreams
    **Industry**: Knowledge-Intensive Applications

    **Impact Metrics**:

    - **40% improvement** in domain-specific information retrieval accuracy
    - Hybrid search combining vector and keyword strategies
    - Production-grade pipeline serving knowledge-intensive applications
    - Hexagonal architecture for clean LLM decoupling

## Challenge

Knowledge-intensive applications require highly accurate information retrieval from large, domain-specific document collections. Traditional keyword search missed semantic relationships, while pure vector search struggled with exact term matching and structured queries. The client needed a retrieval system that could reliably surface the most relevant information across diverse document types and query patterns.

## Approach & Architecture

![Architecture diagram — Hybrid Search RAG Pipeline](../../assets/diagrams/rag-hybrid-search-architecture.png)
*High-level architecture: query routing, hybrid retrieval (OpenSearch + Qdrant), fusion, and LLM integration.*

I engineered a retrieval architecture that combines vector and keyword search without locking the system into a single retrieval strategy:

- **OpenSearch** for keyword retrieval and exact-term matching where BM25 performs best.
- **Qdrant** for semantic similarity search that captures intent beyond literal phrasing.
- **Hybrid fusion and re-ranking** to combine both result sets and improve relevance for real user queries.
- **LangChain orchestration** to manage retrieval, prompting, and downstream LLM interaction.
- **Hexagonal architecture** to decouple retrieval logic, model choices, and integration boundaries.

This made it easier to test, replace, and iterate on each part of the stack without rewriting the entire pipeline.

## Results

- 40% improvement in domain-specific information retrieval accuracy
- Reliable handling of both semantic and keyword-based queries
- Modular architecture enabling rapid iteration on search strategies
- Production deployment serving real-time retrieval requests
- Clean LLM decoupling allowing model upgrades without pipeline changes

## Tech Stack

- LangChain for RAG orchestration
- OpenSearch for keyword search (BM25)
- Qdrant for vector similarity search
- Python backend services
- FastAPI for API endpoints
- Docker containerization
- Hexagonal architecture (ports & adapters)

<div class="grid cards" style="margin-top: 3rem" markdown>

-   :material-calendar-month-outline:{ .lg .middle } Book a free intro call

    ---

    If your application struggles with retrieval accuracy or you need a production-ready RAG pipeline, let's explore whether hybrid search is the right next step.

    [Book Free Intro Call :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary target="_blank" rel="noopener" }

</div>
