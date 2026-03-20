---
title: Sobre Andrés Espinosa Sanfiel
description: Sobre Andrés Espinosa Sanfiel, AI Engineer con 4+ años entre data science, data engineering y entrega de IA en producción.
image: assets/andres-espinosa-cover.jpg
tags:
  - ai-engineering
  - consulting
  - production-ai
hide:
  - footer
---

<div class="about-hero grid-container" markdown>

<div class="text-intro-grid" markdown>

# Sobre Andrés Espinosa Sanfiel

## La versión corta

Ayudo a equipos a llevar sistemas de IA desde "funciona en un notebook" hasta "funciona en producción y confiamos en él."

Si tu prototipo ya demuestra el valor pero el camino hacia un sistema fiable y mantenible todavía no está claro - ahí es exactamente donde mejor trabajo.

</div>

<div class="profile-image-grid" markdown>

![Andrés Espinosa Sanfiel, AI Engineer](assets/andres-espinosa.jpg){ .profile-image alt="Retrato de Andrés Espinosa Sanfiel, AI Engineer" }

</div>

</div>

## Cómo llegué aquí

Estudié Economía antes de tocar una línea de Python. En su momento parecía no tener relación. No era así. La Economía me entrenó para pensar en trade-offs, incentivos y resultados medibles - que es exactamente lo que importa cuando un negocio está a punto de apostar dinero real en un sistema de IA.

Primero pasé a data engineering, construyendo pipelines con Spark y aprendiendo lo que realmente hace falta para mantener datos fluyendo de forma fiable a escala. Después data science - modelos de ML, servicios cloud de IA, MLOps. Y finalmente AI engineering, donde encontré el trabajo que me hace querer seguir resolviendo problemas: llevar una IA que impresiona en una demo a algo en lo que la gente pueda confiar cada día.

Esto es lo que ese camino me enseñó. El modelo rara vez es la parte difícil. Lo que rompe los proyectos es todo lo que lo rodea - el enrutamiento, los reintentos, los límites del sistema que nadie definió, el retrieval que funciona perfecto con datos de test y falla con queries reales. He estado en ambos lados de ese problema las veces suficientes como para saber dónde se esconden los riesgos.

Tengo un Máster en Inteligencia Artificial Avanzada y Aplicada por la Universidad de Valencia, y un Grado en Economía. Uno me da la profundidad técnica, el otro me da el hábito de preguntar "¿esto tiene sentido para el negocio?" antes de escribir una sola línea de código. Uso ambos a diario.

## Lo que he estado construyendo

Ahora mismo, mi trabajo se sitúa en la brecha entre un prototipo de IA funcional y un sistema en el que un equipo pueda depender de verdad.

Los proyectos recientes incluyen workflows agénticos que redujeron el procesamiento manual un 70%, pipelines de RAG híbrido que mejoraron la precisión de retrieval específico de dominio un 40%, y servicios FastAPI gestionando más de 500 peticiones API diarias para cargas de trabajo de IA en vivo.

Uno de esos - un sistema de automatización de email en producción construido con PydanticAI, RAG y FastAPI - lo [presenté públicamente en el Datamecum Webinar 2025](https://youtu.be/cECPFYFLAVw?si=AfFpwbT-skWP5LGp){ target="_blank" rel="noopener" }. Fue mi primera charla técnica delante de una audiencia, y sinceramente, fue un punto de inflexión. Hablar públicamente sobre lo que construyo me obligó a ser más claro sobre por qué cada decisión de diseño importaba - y esa claridad ahora se nota en cada proyecto.

Puedes explorar los detalles completos en mis [casos de estudio](portfolio/index.md).

## Certificaciones y divulgación

<div class="grid cards" markdown>

-   :material-microsoft:{ .lg .middle } **Certificaciones Microsoft**

    ---

    [Azure AI Engineer Associate](https://learn.microsoft.com/en-us/users/andrsespinosasanfiel-16/credentials/b82aae16722c94fe){ target="_blank" rel="noopener" }
    [Azure Data Scientist Associate](https://learn.microsoft.com/en-us/users/andrsespinosasanfiel-16/credentials/b5e0bd45059b634a){ target="_blank" rel="noopener" }
    [Fabric Analytics Engineer Associate](https://learn.microsoft.com/en-us/users/andrsespinosasanfiel-16/credentials/b5d62cfc3a86d3a4){ target="_blank" rel="noopener" }
    [Azure Fundamentals](https://learn.microsoft.com/en-us/users/andrsespinosasanfiel-16/credentials/b223548422651062){ target="_blank" rel="noopener" }

-   :fontawesome-solid-database:{ .lg .middle } **Certificaciones Databricks**

    ---

    [Machine Learning Associate](https://credentials.databricks.com/6b2bbbc2-c75f-4ec9-9540-89d1879a3b98){ target="_blank" rel="noopener" }
    [Apache Spark Developer](https://credentials.databricks.com/9e374e9e-e49d-47e2-966f-581d521c2f5a){ target="_blank" rel="noopener" }

-   :material-microphone:{ .lg .middle } **[Ponente técnico](https://youtu.be/cECPFYFLAVw?si=AfFpwbT-skWP5LGp){ target="_blank" rel="noopener" }**

    ---

    Ponente en Datamecum Webinar 2025, presentando un sistema GenAI de automatización de email en producción construido con PydanticAI, RAG y FastAPI.

</div>

## Stack principal

<div class="grid cards" markdown>

-   :material-robot-outline:{ .lg .middle } **Agentic AI y orquestación**

    ---

    LangChain, LangGraph, PydanticAI, Agno, MCP protocol, workflows deterministas, agentes multi-step y orquestación de tools.

-   :material-database-search:{ .lg .middle } **Retrieval y datos**

    ---

    OpenSearch, Qdrant, PostgreSQL, pgVector, PySpark, SQL y arquitecturas de búsqueda por dominio que combinan vector y keyword retrieval.

-   :material-api:{ .lg .middle } **Plataformas y cloud**

    ---

    Python, FastAPI, WebSockets, AWS (ECS, Lambda, S3, DynamoDB, EventBridge), Azure, Docker, Redis y APIs backend construidas para uso real.

-   :material-chart-box-outline:{ .lg .middle } **Delivery y MLOps**

    ---

    CI/CD, MLflow, Langfuse, LangSmith, model tracking, workflows de despliegue y arquitectura hexagonal para mantenibilidad y desacoplamiento.

</div>

## Cómo trabajo

Cada proyecto empieza con una pregunta simple: ¿cómo se ve el éxito y cómo lo mediremos? La arquitectura se deriva de la respuesta - no al revés.

Tengo opiniones claras sobre algunas cosas. Prefiero workflows deterministas antes que magia de caja negra. Si el comportamiento del sistema no se puede testear y observar, no está listo para producción. Eso significa que pienso con cuidado sobre dónde el LLM aporta valor real y dónde la lógica simple hace mejor el trabajo - y no me da miedo decir "para esa parte no necesitas IA."

Construyo pensando en producción desde el primer día. La observabilidad, la mantenibilidad y los límites claros del sistema no son cosas que añado al final - dan forma al diseño inicial. Cuando el proyecto termina, el objetivo siempre es un sistema que tu equipo pueda operar, extender y evaluar sin necesitarme en la sala.

Trabajo bien por mi cuenta y también integrado en un equipo interno de ingeniería o producto. En cualquier caso, te diré lo que creo que funcionará, lo que no, y cuáles son los trade-offs. Prefiero tener una conversación honesta ahora que una dolorosa tres meses dentro de la entrega.

## Idiomas y disponibilidad

- Trabajo en inglés y español.
- Basado en España y disponible para colaboración remota en toda Europa.
- Abierto a oportunidades freelance, contract y colaboraciones seleccionadas a largo plazo.

<div class="cta-panel" markdown>

## ¿Quieres comentar un proyecto?

Si ya tienes el caso de negocio pero el camino de entrega todavía se siente frágil, hablemos. Puedo ayudarte a evaluar la forma técnica, los riesgos y los próximos pasos antes de que tu equipo se comprometa con la implementación.

<div class="cta-actions" markdown>
[Reserva una llamada :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="about_intro_call_es" target="_blank" rel="noopener" }
[Conecta en LinkedIn :fontawesome-brands-linkedin:](https://www.linkedin.com/in/aesanfiel/){ .md-button .track-conversion data-conversion-label="about_linkedin_es" target="_blank" rel="noopener" }
</div>

</div>
