---
title: Automatización de emails de reservas con IA
description: Workflow GenAI en producción que automatizó el procesamiento de emails de reservas para un equipo de operaciones turísticas, reduciendo el triaje manual diario de 100+ emails a 10-15 items accionables usando Gemini, Instructor, Pydantic y AWS.
image: assets/diagrams/booking-email-automation-architecture.png
tags:
  - agentic-ai
  - ai-engineering
  - aws
  - production-ai
---

# Automatización de emails de reservas con IA

!!! abstract "Resumen de entrega"
    **Rol**: AI Engineer<br>
    **Sector**: Turismo y operaciones de actividades<br>
    **Objetivo**: Automatizar el procesamiento, clasificación y enrutamiento de emails de reservas de alto volumen con generación de respuestas a proveedores

!!! success "Impacto medible"
    - Reducción del triaje diario de **100+ emails a 10-15 items accionables**
    - Extracción, clasificación y comunicación con proveedores automatizadas en **4 categorías de reserva**
    - Procesamiento idempotente con cero mensajes duplicados a proveedores
    - Operaciones self-service vía **panel de administración Streamlit** - sin necesidad de ingeniería para cambios del día a día

!!! info "Stack principal"
    <span class="tech-badge">Gemini</span>
    <span class="tech-badge">Instructor</span>
    <span class="tech-badge">Pydantic</span>
    <span class="tech-badge">Python</span>
    <span class="tech-badge">AWS SQS</span>
    <span class="tech-badge">AWS SES</span>
    <span class="tech-badge">AWS S3</span>
    <span class="tech-badge">Streamlit</span>

## Reto

El equipo de operaciones de una empresa de turismo y actividades procesaba más de 100 emails de reservas al día - nuevas reservas, cancelaciones, modificaciones y consultas generales - todo manualmente. Cada email tenía que leerse, entenderse, cruzarse con el catálogo de actividades actual, clasificarse por tipo y enrutarse al proveedor o equipo interno correcto.

El proceso era lento, inconsistente y apartaba al personal cualificado de trabajo operativo de mayor valor. Se perdían emails, se enviaban duplicados a proveedores y no había registro estructurado de qué se había procesado ni por qué.

Necesitaban un sistema capaz de entender automáticamente los emails de reservas, extraer datos estructurados, clasificar el tipo de solicitud y generar la comunicación correcta al proveedor - sin romperse cuando aparecían edge cases o reintentos.

## Resumen de la solución

![Diagrama de arquitectura - Automatización de emails de reservas con IA](../../assets/diagrams/booking-email-automation-architecture.png)

Diseñé el sistema como un **workflow LLM orquestado en AWS**, construido alrededor de seis etapas de procesamiento con control determinista en cada paso.

### Ingestión

- **Los emails de reservas entrantes** llegan y se encolan vía **AWS SQS**, desacoplando la llegada del email del procesamiento y dando al sistema control de backpressure y seguridad en reintentos desde el primer paso.

### Pre-validación

- Antes de cualquier procesamiento LLM, el sistema filtra emails entrantes por **tipo de actividad, canal y código de reserva**.
- Esto mantiene los costes de inferencia predecibles y evita que la capa de IA desperdicie tokens en mensajes irrelevantes o malformados.

### Extracción estructurada

- **Gemini** con **Instructor** y modelos **Pydantic** extrae datos de reserva validados y tipados del texto desestructurado del email.
- Cada campo se valida contra un esquema antes de que el workflow continúe - ninguna salida LLM en texto libre pasa.
- Los datos extraídos alimentan el **Sales Report en S3** para tracking operativo.

### Grounding operativo

- Las decisiones de clasificación se anclan a un **catálogo de actividades en vivo almacenado en S3**, de modo que el sistema enruta basándose en lo que realmente es reservable hoy - no en contexto obsoleto o alucinado.
- Cuando el catálogo cambia, el sistema se adapta inmediatamente sin redespliegue.

### Clasificación y enrutamiento

- Cada email se clasifica en uno de cuatro caminos: **nueva reserva, cancelación, modificación o consulta**.
- Cada camino dispara lógica downstream diferente y plantillas de comunicación con proveedores.

### Idempotencia y control de reintentos

- **Marcadores de estado en S3** previenen el procesamiento duplicado cuando los emails se reintentan o reenvían por SQS.
- Ninguna reserva se procesa dos veces. Ningún proveedor recibe un mensaje duplicado.

### Generación y entrega de mensajes a proveedores

- El sistema genera **comunicaciones listas para proveedores** restringidas por plantillas y reglas de negocio.
- **AWS SES** entrega los mensajes a proveedores y produce un **resumen interno** para el equipo de operaciones.

### Capa de operaciones

- Un **panel de administración Streamlit** da al equipo de operaciones control directo sobre el catálogo de actividades y acceso a informes de ventas.
- Los cambios de configuración del día a día requieren cero intervención de ingeniería.

## Decisiones clave de diseño

- **LLM solo donde aporta valor.** Pre-validación, lógica de enrutamiento, control de idempotencia y entrega son completamente deterministas. El LLM se encarga de extracción y generación de mensajes - las partes donde realmente se necesita comprensión de lenguaje no estructurado.
- **Salidas estructuradas en todas partes.** Gemini con Instructor y modelos Pydantic significa que cada respuesta del LLM se valida antes de que el workflow continúe. Si la salida no cumple, el sistema reintenta o marca para revisión - nunca deja pasar datos incorrectos downstream.
- **Grounding contra datos operativos en vivo.** La clasificación se ancla al catálogo de actividades real en S3, no a los datos de entrenamiento del modelo. Esto elimina disponibilidad alucinada y mantiene el enrutamiento preciso conforme cambia el negocio.
- **Idempotencia como requisito de primer nivel.** Los sistemas de email reintentan. SQS reenvía. El workflow gestiona todo esto de forma elegante mediante marcadores de estado en S3, para que el equipo de operaciones nunca tenga que comprobar manualmente si hay mensajes duplicados a proveedores.
- **Operaciones self-service.** El panel de administración Streamlit significa que el equipo de operaciones es dueño de su catálogo y reporting sin depender de ingeniería para cada cambio. Esto reduce fricción y mantiene el sistema mantenible a largo plazo.

## Resultados en producción

- Triaje diario de emails reducido de 100+ items a 10-15 accionables
- Extracción y clasificación automatizadas en cuatro categorías de reserva
- Respuestas a proveedores generadas y enviadas sin intervención manual
- Cero mensajes duplicados a proveedores gracias al procesamiento idempotente
- El equipo de operaciones gestiona catálogo y reporting a través del panel de administración self-service
- El sistema gestiona reintentos y edge cases sin recuperación manual

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| LLM y extracción | Gemini, Instructor, Pydantic |
| Orquestación | Python, control determinista de workflow |
| Ingestión y colas | AWS SQS |
| Almacenamiento y estado | AWS S3 (catálogo de actividades, informes de ventas, marcadores de idempotencia) |
| Entrega de email | AWS SES |
| Interfaz de administración | Streamlit |
| Infraestructura | AWS (SQS, SES, S3) |

<div class="cta-panel" markdown>

## ¿Procesando grandes volúmenes de emails operativos manualmente?

Si tu equipo dedica horas cada día a leer, clasificar y responder comunicaciones estructuradas - solicitudes de reserva, coordinación con proveedores, confirmaciones de pedidos, tickets de soporte - y la lógica de decisión está clara pero la ejecución sigue siendo manual, este es el tipo de sistema que construyo.

<div class="cta-actions" markdown>
[Reserva una llamada gratuita :material-arrow-top-right:](https://calendly.com/andresesanfiel/introduction-call){ .md-button .md-button--primary .track-conversion data-conversion-label="case_booking_intro_call_es" target="_blank" rel="noopener" }
</div>

</div>
