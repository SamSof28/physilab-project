# 🔬 PhysiLab: Laboratorio de Física Virtual

Bienvenido a la documentación oficial de **PhysiLab**, una plataforma educativa y profesional diseñada para la simulación, cálculo y gestión de ensayos físicos. 

Este proyecto aplica **Ingeniería de Software** de alto nivel para resolver problemas de cinemática y dinámica, utilizando principios de **Clean Code**, **SOLID** y **Arquitectura por Capas**.

---

## 🚀 Características del Laboratorio

- 🛰️ **Cálculos Cinemáticos:** Resolución inteligente de MRU, MRUA y Tiro Parabólico.
- 📐 **Motor Matemático:** Implementación de despejes automáticos y manejo de vectores con **NumPy**.
- 💻 **CLI Profesional:** Interfaz de línea de comandos robusta basada en **Typer** y **Rich**.
- 🧪 **Calidad Garantizada:** Cobertura de pruebas unitarias al 100% con `pytest` y aislamiento mediante **Mocks**.
- 🏗️ **Diseño Robusto:** Arquitectura `src layout` con separación estricta de responsabilidades.
- 🛡️ **Seguridad Física:** Validaciones de dominio para prevenir estados físicamente imposibles (tiempos negativos, divisiones por cero).

---

## 🧠 Pilares de Ingeniería

!!! info "Conceptos Avanzados Aplicados"

    - **Inyección de Dependencias:** Desacoplamiento total entre la lógica física y el almacenamiento.
    - **Encapsulamiento Post-Init:** Modelos de datos (`dataclasses`) con integridad física garantizada.
    - **Manejo de Excepciones de Dominio:** Jerarquía de errores clara para fallos matemáticos y de negocio.
    - **Persistencia Atómica:** Gestión segura de datos en formato JSON (preparado para SQL/Supabase).

---

## 🏗️ Arquitectura del Sistema

PhysiLab separa la "Inteligencia Física" del "Almacenamiento de Datos", permitiendo que el laboratorio crezca sin romper lo existente.

``` mermaid
graph TD
    subgraph Interfaz
        CLI[CLI - Typer/Rich]
    end

    subgraph Nucleo_Fisico
        Service[LaboratorioService]
        Model[Modelos: MRU, MRUA, Parabólico]
    end

    subgraph Persistencia
        Storage[JSONStorage]
        DB[(database.json)]
    end

    CLI --> Service
    Service --> Model
    Service --> Storage
    Storage --> DB

```