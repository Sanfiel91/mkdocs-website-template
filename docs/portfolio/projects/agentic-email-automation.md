---
title: AI-Powered Email Automation System
description: Production GenAI pipeline that reduced daily email triage from 100+ items to 10-15 actionable items using PydanticAI, RAG, FastAPI, and Slack integration with full observability via Langfuse.
image: assets/diagrams/email-automation-architecture.png
tags:
  - agentic-ai
  - ai-engineering
  - rag
  - production-ai
---

# AI-Powered Email Automation System

!!! abstract "Delivery snapshot"
    **Role**: AI Engineer<br>
    **Sector**: Productivity and operations automation<br>
    **Goal**: Turn chaotic email inboxes into structured, automated workflows with traceability and human control

!!! success "Measured impact"
    - Reduced daily email triage from **100+ items to 10-15 actionable items**
    - Automated classification, routing, and response generation across multiple email categories
    - Two delivery channels: **smart notifications** and **conversational assistant via Slack + RAG**
    - Full production observability with **Langfuse** (traces, cost per email, quality tracking)
    - Presented as Technical Speaker at **[Datamecum Webinar 2025](https://youtu.be/cECPFYFLAVw?si=AfFpwbT-skWP5LGp){ target="_blank" rel="noopener" }**

!!! info "Core stack"
    <span class="tech-badge">PydanticAI</span>
    <span class="tech-badge">OpenAI</span>
    <span class="tech-badge">FastAPI</span>
    <span class="tech-badge">Celery</span>
    <span class="tech-badge">PostgreSQL + pgvector</span>
    <span class="tech-badge">Redis</span>
    <span class="tech-badge">Slack</span>
    <span class="tech-badge">Langfuse</span>
    <span class="tech-badge">Docker</span>

<div class="metric-highlight">
  <div class="metric-highlight-item">
    <span class="metric-number">85%</span>
    <span class="metric-label">reduction in manual triage effort</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">2</span>
    <span class="metric-label">delivery channels (notifications + RAG assistant)</span>
  </div>
  <div class="metric-highlight-item">
    <span class="metric-number">Real-time</span>
    <span class="metric-label">observability with Langfuse</span>
  </div>
</div>

## Challenge

The average professional receives over 120 emails per day and spends roughly 28% of their working time managing them. Critical messages get buried, responses are delayed, and the constant context-switching drains productivity.

The goal was to build a system that could automatically ingest incoming emails, understand their content, classify them by type and urgency, and execute the right action - all with full traceability and human oversight when needed. Not a filtering tool. A production pipeline that reads, decides, and acts.

## Solution overview

![Architecture diagram - AI-Powered Email Automation System](../../assets/diagrams/email-automation-solution-overview-version-english.svg)
*End-to-end solution diagram from the Datamecum Webinar 2025 presentation.*

![How the AI classifies emails](../../assets/diagrams/email-classification-flow-en.svg)
*Classification flow: how the AI processes, classifies, and routes each email.*

The system follows four stages: **Ingestion → AI Engine → Smart Decisions → Autonomous Actions**.

### Ingestion

- **Gmail integration via Nylas** webhooks captures incoming emails in real time.
- Raw email events are stored asynchronously and queued for processing.
- An **email filter** pre-screens messages before any LLM processing, keeping inference costs predictable and avoiding wasted computation on irrelevant traffic.

### AI Engine

- An **LLM classifier** (powered by OpenAI) analyzes filtered emails and extracts structured content using **PydanticAI**, producing validated, type-safe outputs - no free-form text leaves this stage.
- Extracted content is embedded into **PostgreSQL + pgvector** for semantic search and long-term context retrieval.

### Smart Decisions

A **deterministic smart router** classifies each email and sends it down the right path:

- **Auto-reply** - The LLM generates and sends a context-aware response using RAG, grounded in availability and email content.
- **Draft and label** - Generates a polite draft when no specific template exists or context is insufficient, and labels the email for human review.
- **Filter and discard** - Detects spam, moves it to the spam folder, and logs evidence (sender, domain, score).
- **Extract and forward** - Pulls structured fields (JSON via Pydantic) from invoices and operational emails, then routes them downstream.

### Autonomous Actions and Delivery

The system delivers results through **two channels**:

- **Smart notifications** - Proactive alerts pushed to Slack: urgent email detected, new invoice amount, spam moved, email snippets for quick context.
- **Conversational assistant** - A Slack-based RAG interface where the user can ask questions like "What invoices are pending?", "Summarize the last email from X", or "What did Y say about Z?" - all grounded in pgvector context.

## Key design decisions

- **LLM only where it adds value.** Email filtering, routing logic, and storage are deterministic. The LLM handles classification, extraction, and response generation - the parts where unstructured language understanding is genuinely needed.
- **Structured outputs everywhere.** PydanticAI ensures every LLM response is validated against a schema before the workflow continues. If the output does not conform, the system retries or flags - it never silently passes bad data.
- **Privacy and data control by design.** Minimal OAuth scopes via Nylas, PII redaction and encryption, no vendor lock-in. The entire system runs on a Hetzner VM at a fraction of what enterprise suites cost.
- **Full observability with Langfuse.** Every email processed generates a trace: latency per node, LLM cost per email, token usage, model version, and quality annotations. Langfuse acts as the open black box of the pipeline - if something breaks or drifts, the trace shows exactly where and why.
- **Horizontally scalable.** Docker + FastAPI + Celery means the system can scale workers independently as email volume grows, without re-architecting.

## Results in production

- Daily email triage reduced from 100+ items to 10-15 actionable items
- Automated classification and routing across multiple email categories
- Context-aware auto-replies generated and sent without manual intervention
- Conversational assistant enabling natural language queries over email history
- Full cost and quality observability per email processed
- Significantly lower infrastructure cost compared to enterprise email automation platforms

## Tech Stack

| Layer | Technology |
|---|---|
| LLM & structured outputs | OpenAI, PydanticAI |
| Orchestration | Python, FastAPI, Celery |
| Email integration | Nylas (Gmail webhooks, minimal OAuth scopes) |
| Vector storage & RAG | PostgreSQL + pgvector, semantic hybrid search |
| Caching | Redis |
| Delivery channels | Slack (notifications + conversational assistant) |
| Observability | Langfuse (traces, cost tracking, quality annotations) |
| Infrastructure | Docker, Hetzner VM |

## Watch the technical talk

This system was presented publicly at **Datamecum Webinar 2025**, walking through the full production architecture, the smart router design, the cost comparison with enterprise alternatives, and a live demo.

<div class="embedded-video">
  <a href="https://youtu.be/cECPFYFLAVw?si=dh9k_iqe5bDFC_fv&t=472" target="_blank" rel="noopener" aria-label="Watch Datamecum Webinar 2025 on YouTube">
    <img src="https://img.youtube.com/vi/cECPFYFLAVw/maxresdefault.jpg" alt="Watch Datamecum Webinar 2025 - AI-Powered Email Automation" loading="lazy">
  </a>
</div>

<div class="cta-panel" markdown>

## Losing hours to email triage every day?

If your team is manually sorting, classifying, and responding to high volumes of structured communications - and the decision logic is clear but the execution is still manual - this is the type of production pipeline I build.

<div class="cta-actions" markdown>
[Book a free intro call :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="case_email_intro_call" target="_blank" rel="noopener" }
[Read the related blog post :material-arrow-right:](../../blog/posts/ai-email-automation-webinar.md){ .md-button }
</div>

</div>
