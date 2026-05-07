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

## ⚙️ Guía de Instalación y Configuración

Este proyecto requiere [uv](https://docs.astral.sh/uv/) para una gestión eficiente de dependencias y entornos virtuales.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/SamSof28/physilab-project.git](https://github.com/SamSof28/physilab-project.git)
    cd physilab-project
    ```

2.  **Sincronizar el entorno e instalar dependencias:**
    ```bash
    uv sync
    ```

3.  **Activar el entorno virtual (opcional):**
    ```bash
    source .venv/bin/activate  # En Linux/macOS
    .venv\Scripts\activate     # En Windows
    ```

---

## 🖥️ Ejecución del Proyecto

Una vez instalado, puedes levantar cada componente principal:

### 1. Ejecutar API (FastAPI)
```bash
uv run fastapi dev src/api/main.py
```

### 2. Ejecutar frontend (Streamlit)
```bash
uv run streamlit run src/app/main.py
```

### 3. Configurar backend de datos (Supabase)
Asegura las variables de entorno del proyecto antes de ejecutar en local o desplegar (por ejemplo, URL y key de Supabase).

## **🧪 Pruebas y Calidad**
Para ejecutar la suite de pruebas unitarias y verificar la integridad de los cálculos físicos:

```Bash
uv run pytest
```
---

Desarrollado por: Samuel Romaña Acevedo - Estudiante de Ingeniería de Sistemas y Computación Científica.