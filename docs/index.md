# 🔬 PhysiLab: Cuaderno de Laboratorio Digital

Bienvenido a la documentación oficial de **PhysiLab**, una plataforma web modular para registrar, analizar y persistir ensayos de movimiento rectilíneo uniforme (MRU) y uniformemente acelerado (MRUA).

PhysiLab está construido como una arquitectura escalable con **Frontend** (Streamlit), **API REST** (FastAPI) y **Base de datos** (Supabase), ideal para aprendizaje en ingeniería de software, experimentación educativa y prácticas de laboratorio digital.

---

## ✨ Qué puedes hacer con PhysiLab

- **Registrar ensayos** de MRU y MRUA con interfaz web amigable.
- **Calcular automáticamente** variables faltantes usando motor matemático con NumPy.
- **Gestionar historial persistente** en Supabase con sincronización en tiempo real.
- **Acceder a la API REST** para integración con otras herramientas.
- **Analizar resultados** con visualizaciones interactivas mediante Plotly.
- **Escalar a nuevos modelos** de física (fuerzas, energías) sin romper la arquitectura.

---

## 🧠 Conceptos clave del proyecto

- Modelado de dominio con Pydantic (validación y serialización).
- Arquitectura por capas (Presentación, Lógica de Negocio, Persistencia).
- Separación de responsabilidades entre Frontend y API.
- Validación temprana de datos físicos y reglas de negocio.
- Persistencia desacoplada mediante repositorios abstractos.
- Documentación técnica con MkDocs + Material y OpenAPI automático.

---

## 🏗️ Arquitectura del sistema

```mermaid
graph TB
    Streamlit["🎨 Frontend<br/>Streamlit"]
    FastAPI["⚡ API REST<br/>FastAPI"]
    PhysicsService["🔬 Lógica de Física<br/>PhysicsService"]
    Repository["💾 Repositorio<br/>ExperimentRepository"]
    Supabase[("📦 Supabase<br/>PostgreSQL")]
    
    Streamlit -->|HTTP| FastAPI
    FastAPI --> PhysicsService
    PhysicsService --> Repository
    Repository -->|queries| Supabase
    Supabase -->|responses| Repository
```

---

## 🚀 Flujo general de una operación

```mermaid
sequenceDiagram
    participant Usuario
    participant Streamlit as Streamlit<br/>Frontend
    participant FastAPI as FastAPI<br/>API
    participant Service as PhysicsService<br/>Lógica
    participant Repo as Repository<br/>Persistencia
    participant DB as Supabase<br/>DB

    Usuario->>Streamlit: Ingresa datos MRU
    Streamlit->>FastAPI: POST /experiments/calculate/mru
    FastAPI->>Service: resolver_y_guardar_mru()
    Service->>Service: Calcula variable faltante
    Service->>Repo: create_mru_experiment()
    Repo->>DB: INSERT into experiments
    DB-->>Repo: Confirmación + ID
    Repo-->>Service: Experimento guardado
    Service-->>FastAPI: ExperimentResponse
    FastAPI-->>Streamlit: JSON con resultado
    Streamlit-->>Usuario: Visualización en interfaz
```

---

## 📚 Navegación de la documentación

| Sección | Contenido |
| --- | --- |
| **Primeros pasos** | Instalación, configuración de Supabase y primera ejecución |
| **Guía de usuario** | Uso del Frontend, API REST y consulta de resultados |
| **Arquitectura** | Diseño técnico, capas, patrones y decisiones clave |
| **Referencia** | Documentación API (OpenAPI), esquemas y servicios |

!!! tip "Recomendación"
    Si es tu primera vez, comienza por **Primeros pasos**, luego explora la **Guía de usuario**. Para entender el diseño interno, consulta **Arquitectura**.