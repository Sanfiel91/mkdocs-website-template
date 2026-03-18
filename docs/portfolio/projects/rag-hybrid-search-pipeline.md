---
title: Hybrid Search RAG Pipeline
description: Enterprise RAG pipeline combining OpenSearch and Qdrant vector databases with hybrid search, achieving 40% improvement in retrieval accuracy.
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

## Approach

I engineered a hybrid search RAG pipeline that combines the strengths of both vector and keyword search:

- **OpenSearch** for full-text keyword search with BM25 scoring, handling exact matches and structured queries
- **Qdrant vector database** for semantic similarity search using dense embeddings, capturing meaning beyond keywords
- **Hybrid search fusion** strategy that combines results from both engines, re-ranking to optimize relevance
- **LangChain** orchestration for managing the retrieval pipeline, prompt templates, and LLM interaction
- **Hexagonal architecture** principles to decouple the LLM layer from retrieval logic, enabling easy swapping of models and search backends

The architecture was designed with clean ports-and-adapters patterns, allowing each component (embedding model, vector store, search engine, LLM) to be independently tested and replaced.

## Results & Impact

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

-   :material-linkedin:{ .lg .middle } Need better search accuracy?

    ---

    If your application struggles with information retrieval or you need a production-ready RAG pipeline, let's connect and explore how hybrid search can improve your results.

    [Let's Connect :material-arrow-top-right:](https://www.linkedin.com/in/aesanfiel/){ .md-button .md-button--primary }

</div>
