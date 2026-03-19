---
title: Production Playbook for Agentic AI Workflows
date: 2025-03-14
authors:
  - aesanfiel
categories:
  - Agentic AI
  - Architecture
tags:
  - agentic-ai
  - orchestration
  - langchain
  - pydanticai
description: A practical playbook for deciding what should stay deterministic, what can be delegated to the model, and how to keep agentic workflows testable.
image: assets/diagrams/ai-api-platform-architecture.png
---

# Production Playbook for Agentic AI Workflows

The fastest way to create a fragile AI system is to treat every step as an open-ended model decision. The fastest way to create a usable one is to decide, explicitly, where determinism should live and where the model is actually adding value.

<!-- more -->

## Start from workflow boundaries, not prompts

Most teams begin with prompts because they are the easiest part to prototype. In production, the real questions are different:

- What events start the workflow?
- Which decisions need typed outputs?
- Which paths require human review?
- What should happen when a tool call or retrieval step fails?

If those questions are unresolved, adding another agent usually makes the system harder to reason about, not better.

## The minimum production shape

I look for four layers:

1. A deterministic application workflow that owns routing, retries, and escalation.
2. A model layer used for judgment tasks where language understanding adds real value.
3. Typed contracts between steps so downstream logic is stable.
4. Observability around latency, failure modes, and user-visible outcomes.

## A useful split of responsibilities

=== "Workflow control"
    ```python
    workflow = Workflow(
        classify=classify_request,
        route=route_by_policy,
        escalate=send_to_human_review
    )
    ```

=== "Model judgment"
    ```python
    agent = Agent(
        model="gpt-4o-mini",
        output_type=ClassificationResult,
        system_prompt="Return a typed decision with rationale."
    )
    ```

## What to keep deterministic

- Entry conditions and routing
- Tool permissions
- Retry limits and timeout behavior
- Confidence thresholds that change user experience
- Audit logging and event emission

These are product and system decisions. Leaving them inside prompts usually makes the behavior harder to test and harder to defend.

## Where the model should help

- Interpreting messy user input
- Summarizing ambiguous evidence
- Proposing candidate actions for a human reviewer
- Extracting structure from unstructured text

The model is most useful when it narrows uncertainty, not when it owns every branch of the application.

## Implementation checkpoint

Before shipping, I want to see:

- A typed input and output contract for each major step
- One or two clear escalation paths
- A place to inject retrieval or policy context without rewriting the workflow
- Enough traces and logs to explain why a result was produced

That does not make the system perfect. It makes it operable.

If your workflow is already useful in a prototype but still feels too opaque for production, [book an intro call](https://calendly.com/andresesanfiel/introduction-call){ .track-conversion data-conversion-label="post_agentic_intro_call" target="_blank" rel="noopener" }. That transition point is usually where architecture matters most.
