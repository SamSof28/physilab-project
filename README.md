# 🚀 PhysiLab: Cuaderno de Laboratorio Digital

Enlace del proyecto: [https://github.com/SamSof28/physilab-project](https://github.com/SamSof28/physilab-project)

![Python](https://img.shields.io/badge/python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![UV](https://img.shields.io/badge/managed%20by-uv-de5fe9?style=for-the-badge&logo=uv&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-389C5A?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/data-Supabase-03A836?style=for-the-badge&logo=supabase&logoColor=white)
![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Graphs-Plotly-3776AB?style=for-the-badge&logo=Plotly&logoColor=white)

PhysiLab evoluciona de una herramienta CLI a una plataforma web para simulación y registro de fenómenos físicos. La arquitectura actual se basa en **Streamlit** (frontend), **FastAPI** (API) y **Supabase** (backend de datos), manteniendo principios de **Clean Code** y **Arquitectura por Capas**.

## 🎯 Propósito y Alcance
El objetivo principal es proporcionar un entorno digital persistente donde los usuarios puedan:
* **Registrar** ensayos de cinemática (MRU y MRUA) desde una interfaz web.
* **Automatizar** cálculos complejos mediante el motor matemático de **NumPy**.
* **Gestionar** un historial de experimentos con persistencia en **Supabase**.
* **Validar** datos experimentales mediante un sistema robusto de excepciones personalizadas.
* **Escalar** el laboratorio para integrar nuevos modelos matemáticos, incluyendo temas de **fuerzas** y **energías**.

---

## 📂 Estructura del Proyecto (Arquitectura)
El proyecto utiliza una estructura de tipo `src` para garantizar la separación de responsabilidades:

* **`src/app/`**: Frontend en Streamlit para captura y análisis de ensayos.
* **`src/api/`**: API REST en FastAPI para exponer operaciones y cálculos.
* **`src/services/`**: Lógica física y reglas de negocio.
* **`src/storage/`**: Repositorios y acceso a datos (integración con Supabase).
* **`src/schemas/`**: Esquemas y contratos de datos.

---

## ⚙️ Instalación y Configuración

Este proyecto usa [uv](https://docs.astral.sh/uv/) para administrar dependencias y entorno.

1. Clona el repositorio.
2. Ejecuta `uv sync`.
3. Crea `.env` a partir de `.env.example` y completa tus credenciales de Supabase.

Variables de entorno requeridas:

- `SUPABASE_URL`
- `SUPABASE_KEY`
- `API_BASE_URL`
- `API_TITLE`
- `API_VERSION`
- `DEBUG`

## Ejecución

Backend FastAPI:

```bash
uvicorn src.api.main:app --reload
```

Frontend Streamlit:

```bash
uv run streamlit run src/app/main.py
```

## Pruebas y calidad

```bash
uv run pytest
uv run ruff check .
uv run radon cc src -a
```

## Estructura

- `src/api/`: API REST con FastAPI.
- `src/app/`: interfaz web en Streamlit.
- `src/services/`: lógica de negocio.
- `src/storage/`: repositorios y acceso a Supabase.
- `src/schemas/`: contratos de datos.
- `src/core/`: configuración y excepciones.

Desarrollado por: Samuel Romaña Acevedo.