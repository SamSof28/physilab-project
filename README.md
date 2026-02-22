# 🚀 PhysiLab: Cuaderno de Laboratorio Digital

Enlace del proyecto: [https://github.com/SamSof28/physilab-project](https://github.com/SamSof28/physilab-project)

![Python](https://img.shields.io/badge/python-3.14+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![UV](https://img.shields.io/badge/managed%20by-uv-de5fe9?style=for-the-badge&logo=uv&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![JSON](https://img.shields.io/badge/data-JSON-000000?style=for-the-badge&logo=json&logoColor=white)
![Typer](https://img.shields.io/badge/CLI-Typer-009688?style=for-the-badge&logo=typer&logoColor=white)

PhysiLab es una aplicación de línea de comandos (CLI) de alto rendimiento diseñada para la simulación y registro de fenómenos físicos. Permite a estudiantes e investigadores gestionar ensayos experimentales con precisión científica, aplicando principios de **Clean Code** y **Arquitectura por Capas**.

## 🎯 Propósito y Alcance
El objetivo principal es proporcionar un entorno digital persistente donde los usuarios puedan:
* **Registrar** ensayos de cinemática (MRU, Tiro Parabólico).
* **Automatizar** cálculos complejos mediante el motor matemático de **NumPy**.
* **Gestionar** un historial de experimentos mediante un sistema de persistencia en archivos **JSON**.
* **Validar** datos experimentales mediante un sistema robusto de excepciones personalizadas.

---

## 📂 Estructura del Proyecto (Arquitectura)
El proyecto utiliza una estructura de tipo `src` para garantizar la separación de responsabilidades:

* **`models/`**: Definiciones de entidades físicas utilizando `dataclasses` y Tipado Estricto.
* **`storage/`**: Capa de persistencia encargada de la serialización y deserialización de datos.
* **`services/`**: El cerebro del sistema. Contiene la lógica física y validaciones de negocio.
* **`cli/`**: Interfaz de usuario construida con `Typer` y embellecida con `Rich`.

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

## 🖥️ Manual de Uso (CLI)

Una vez instalado, puedes interactuar con el laboratorio mediante los siguientes comandos:

### 1. Registrar un ensayo MRU
El sistema calculará automáticamente la variable faltante (distancia, tiempo o velocidad):
```bash
uv run python main.py mru --id 1 --nombre "Prueba Inicial" --velocidad 10.5 --tiempo 5
```
### 2. Listar experimentos registrados
Visualiza una tabla formateada con todos tus registros:

```Bash
uv run python main.py listar
```

### 3. Eliminar un registro
```Bash
uv run python main.py eliminar --id 1
```

## **🧪 Pruebas y Calidad**
Para ejecutar la suite de pruebas unitarias y verificar la integridad de los cálculos físicos:

```Bash
uv run pytest
```
---

Desarrollado por: Samuel Romaña Acevedo - Estudiante de Ingeniería de Sistemas y Computación Científica.