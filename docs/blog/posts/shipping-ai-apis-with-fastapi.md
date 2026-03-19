---
title: Shipping AI APIs with FastAPI
date: 2025-07-18
authors:
  - aesanfiel
categories:
  - Delivery
  - Architecture
tags:
  - fastapi
  - ai-api
  - streaming
  - production-ai
description: Service boundaries, streaming contracts, and operational details that matter when AI endpoints move from prototype traffic to real usage.
image: assets/diagrams/ai-api-platform-architecture.png
---

# Shipping AI APIs with FastAPI

FastAPI makes it easy to stand up an AI endpoint quickly. The harder part is deciding what the contract should look like once the workflow includes retrieval, longer-running tasks, partial responses, and operational failure modes.

<!-- more -->

## The first question is not latency

It is tempting to begin with model speed. In practice, the first question is whether the API contract reflects the workflow truthfully:

- Is this request synchronous or asynchronous?
- Will the client need progress events?
- Can the result be partial, streamed, or deferred?
- What should happen when one step of the AI workflow fails?

## The contracts that matter most

=== "Typed request-response"
    ```python
    class AnalysisRequest(BaseModel):
        company_name: str
        question: str

    class AnalysisResponse(BaseModel):
        summary: str
        sources: list[str]
        confidence: float
    ```

=== "Streaming endpoint"
    ```python
    @app.websocket("/analysis/{job_id}")
    async def analysis_stream(websocket: WebSocket, job_id: str) -> None:
        await websocket.accept()
        async for event in service.stream(job_id):
            await websocket.send_json(event.model_dump())
    ```

## Production details that change the design

- AI workflows often need background execution, not just request-response handlers.
- Streaming can improve UX, but only if event semantics are stable.
- Retry logic belongs in application services and workers, not in random route handlers.
- Logging, traces, and request correlation become essential once multiple steps are involved.

## A better default architecture

I prefer to keep FastAPI thin:

- Routes validate and shape inputs
- Application services own orchestration
- Retrieval, tools, and model adapters stay behind explicit interfaces
- Background work is offloaded when the workflow exceeds clean request-response limits

That architecture makes the API easier to scale, test, and evolve as traffic and workflow complexity grow.

## Shipping criteria

Before calling an AI API production-ready, I want:

- typed contracts
- explicit timeout behavior
- clear failure semantics
- observability across the workflow
- deployment and rollback confidence

If your AI endpoint already works but still feels fragile, [book an intro call](https://calendly.com/andresesanfiel/introduction-call){ .track-conversion data-conversion-label="post_fastapi_intro_call" target="_blank" rel="noopener" }. The gap is usually not the model. It is the service design around it.
