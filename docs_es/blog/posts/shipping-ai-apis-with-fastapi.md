---
title: Cómo poner en producción APIs de IA con FastAPI
date: 2025-07-18
authors:
  - aesanfiel
categories:
  - Delivery
  - Arquitectura
tags:
  - fastapi
  - ai-api
  - streaming
  - production-ai
description: Límites de servicio, contratos streaming y detalles operativos que importan cuando un endpoint de IA pasa del tráfico de prototipo al uso real.
image: assets/diagrams/ai-api-platform-architecture.png
---

# Cómo poner en producción APIs de IA con FastAPI

FastAPI hace fácil levantar un endpoint de IA con rapidez. La parte difícil es decidir cómo debe ser el contrato cuando el workflow incluye retrieval, tareas de larga duración, respuestas parciales y failure modes operativos.

<!-- more -->

## La primera pregunta no es la latencia

Es tentador empezar por la velocidad del modelo. En la práctica, la primera pregunta es si el contrato API refleja con honestidad el workflow:

- ¿Esta petición es síncrona o asíncrona?
- ¿El cliente necesita eventos de progreso?
- ¿El resultado puede ser parcial, streaming o diferido?
- ¿Qué debe ocurrir cuando falla un paso del workflow de IA?

## Los contratos que más importan

=== "Request-response tipado"
    ```python
    class AnalysisRequest(BaseModel):
        company_name: str
        question: str

    class AnalysisResponse(BaseModel):
        summary: str
        sources: list[str]
        confidence: float
    ```

=== "Endpoint streaming"
    ```python
    @app.websocket("/analysis/{job_id}")
    async def analysis_stream(websocket: WebSocket, job_id: str) -> None:
        await websocket.accept()
        async for event in service.stream(job_id):
            await websocket.send_json(event.model_dump())
    ```

## Detalles de producción que cambian el diseño

- Los workflows de IA suelen necesitar ejecución en background, no solo handlers request-response.
- El streaming puede mejorar la UX, pero solo si la semántica de eventos es estable.
- La lógica de reintentos pertenece a application services y workers, no a route handlers sueltos.
- Logging, trazas y correlación de requests se vuelven esenciales cuando entran varios pasos.

## Una arquitectura por defecto mejor

Prefiero mantener FastAPI ligero:

- Las rutas validan y dan forma a los inputs
- Los application services son dueños de la orquestación
- Retrieval, tools y adapters de modelo quedan detrás de interfaces explícitas
- El trabajo en background se externaliza cuando el workflow supera los límites limpios de request-response

Esa arquitectura hace que la API sea más fácil de escalar, testear y evolucionar conforme crecen el tráfico y la complejidad del workflow.

## Criterios para considerarlo listo

Antes de llamar production-ready a una API de IA, quiero ver:

- contratos tipados
- comportamiento explícito ante timeouts
- semántica clara de fallos
- observabilidad a lo largo del workflow
- confianza en despliegue y rollback

Si tu endpoint de IA ya funciona pero todavía se siente frágil, [reserva una llamada inicial](https://calendly.com/andresesanfiel/introduction-call){ .track-conversion data-conversion-label="post_fastapi_intro_call_es" target="_blank" rel="noopener" }. El gap normalmente no está en el modelo, sino en el diseño del servicio que lo rodea.
