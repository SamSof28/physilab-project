# Primeros pasos 🚀

Sigue estas instrucciones para configurar tu laboratorio digital en pocos segundos.

## Instalación con `uv`

Este proyecto utiliza **uv** para una gestión de dependencias extremadamente rápida.

=== "Windows"
    ```bash
    uv sync
    uv run main.py --help
    ```
=== "macOS / Linux"
    ```bash
    uv sync
    source .venv/bin/activate
    python main.py --help
    ```

## Sincronización de dependencias
Asegúrate de tener el entorno actualizado ejecutando:
`uv sync`