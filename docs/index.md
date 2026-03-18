# 🔬 PhysiLab: Laboratorio de Cinemática por CLI

Bienvenido a la documentación oficial de PhysiLab, una aplicación de línea de comandos para registrar, calcular y persistir ensayos de movimiento rectilíneo.

Está pensada para aprendizaje, práctica de ingeniería de software y experimentación rápida en terminal.

---

## ✨ Qué puedes hacer con PhysiLab

- Registrar ensayos con identificador y nombre.
- Calcular automáticamente la variable faltante en MRU.
- Mantener historial persistente en JSON local.
- Consultar y eliminar experimentos desde la CLI.
- Trabajar con una arquitectura modular y mantenible.

---

## 🧠 Conceptos que aprenderás

- Modelado de dominio con dataclasses.
- Validación de datos físicos y reglas de negocio.
- Arquitectura por capas aplicada a una CLI real.
- Persistencia desacoplada usando almacenamiento JSON.
- Documentación técnica con MkDocs + Material.

---

## 🏗️ Arquitectura del sistema

```mermaid
flowchart LR
    CLI[Capa CLI] --> Servicio[Capa de Servicios]
    Servicio --> Modelos[Modelos de Dominio]
    Servicio --> Almacenamiento[Persistencia JSON]
    Modelos --> Validacion[Validación de datos]
    Almacenamiento --> BaseDatos[(data/database.json)]
```

---

## 🚀 Flujo general de ejecución

```mermaid
sequenceDiagram
    participant Usuario
    participant CLI
    participant Servicio
    participant Modelo
    participant Almacenamiento

    Usuario->>CLI: Ejecuta comando mru
    CLI->>Modelo: Construye objeto de experimento
    Modelo->>Modelo: Valida datos de entrada
    CLI->>Servicio: calcular_mru(modelo)
    Servicio->>Servicio: Resuelve variable faltante
    Servicio->>Almacenamiento: guardar(experimento)
    Almacenamiento-->>Usuario: Resultado y confirmación
```

---

## 📚 Navegación de la documentación

| Sección | Contenido |
| --- | --- |
| Primeros pasos | Instalación, configuración y primera ejecución |
| Guía de usuario | Uso práctico de comandos y persistencia |
| Arquitectura | Diseño técnico, capas y decisiones clave |
| Referencia | Documentación API generada desde el código |

!!! tip "Recomendación"
    Si es tu primera vez con el proyecto, comienza por Primeros pasos y luego continúa con Guía de usuario.