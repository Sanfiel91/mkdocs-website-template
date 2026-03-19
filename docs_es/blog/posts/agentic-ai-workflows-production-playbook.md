---
title: Playbook de producción para workflows agentic AI
date: 2025-03-14
authors:
  - aesanfiel
categories:
  - Agentic AI
  - Arquitectura
tags:
  - agentic-ai
  - orchestration
  - langchain
  - pydanticai
description: Un playbook práctico para decidir qué debe seguir siendo determinista, qué puede delegarse al modelo y cómo mantener testeables los workflows agentic.
image: assets/diagrams/ai-api-platform-architecture.png
---

# Playbook de producción para workflows agentic AI

La forma más rápida de crear un sistema de IA frágil es tratar cada paso como una decisión abierta del modelo. La forma más rápida de crear uno útil es decidir explícitamente dónde debe vivir el determinismo y dónde el modelo está aportando valor de verdad.

<!-- more -->

## Empieza por los límites del workflow, no por los prompts

La mayoría de equipos empieza por los prompts porque son la parte más fácil de prototipar. En producción, las preguntas reales son otras:

- ¿Qué eventos arrancan el workflow?
- ¿Qué decisiones necesitan salidas tipadas?
- ¿Qué caminos requieren revisión humana?
- ¿Qué debe ocurrir cuando falla una tool call o un paso de retrieval?

Si estas preguntas no están resueltas, añadir otro agente suele hacer el sistema más difícil de razonar, no mejor.

## La forma mínima de producción

Yo busco cuatro capas:

1. Un workflow de aplicación determinista que sea dueño del routing, los reintentos y la escalación.
2. Una capa de modelo para tareas de juicio donde la comprensión del lenguaje aporta valor real.
3. Contratos tipados entre pasos para que la lógica downstream sea estable.
4. Observabilidad sobre latencia, failure modes y resultados visibles para el usuario.

## Un reparto útil de responsabilidades

=== "Control del workflow"
    ```python
    workflow = Workflow(
        classify=classify_request,
        route=route_by_policy,
        escalate=send_to_human_review
    )
    ```

=== "Juicio del modelo"
    ```python
    agent = Agent(
        model="gpt-4o-mini",
        output_type=ClassificationResult,
        system_prompt="Devuelve una decisión tipada con su razonamiento."
    )
    ```

## Qué mantener determinista

- Condiciones de entrada y routing
- Permisos de tools
- Límites de reintento y comportamiento ante timeouts
- Umbrales de confianza que cambian la experiencia de usuario
- Audit logging y emisión de eventos

Estas son decisiones de producto y de sistema. Dejarlas dentro del prompt suele hacer el comportamiento más difícil de testear y más difícil de defender.

## Dónde debe ayudar el modelo

- Interpretando input desordenado del usuario
- Resumiendo evidencia ambigua
- Proponiendo acciones candidatas para revisión humana
- Extrayendo estructura desde texto no estructurado

El modelo es más útil cuando reduce incertidumbre, no cuando se adueña de cada rama de la aplicación.

## Checkpoint de implementación

Antes de ponerlo en producción, quiero ver:

- Un contrato tipado de entrada y salida para cada paso importante
- Uno o dos caminos de escalación claros
- Un punto donde inyectar retrieval o contexto de políticas sin reescribir el workflow
- Trazas y logs suficientes para explicar por qué se produjo un resultado

Eso no vuelve perfecto al sistema. Lo vuelve operable.

Si tu workflow ya aporta valor en un prototipo pero todavía se siente demasiado opaco para producción, [reserva una llamada inicial](https://calendly.com/andresesanfiel/introduction-call){ .track-conversion data-conversion-label="post_agentic_intro_call_es" target="_blank" rel="noopener" }. Ese punto de transición suele ser donde más importa la arquitectura.
