# Primeros pasos

En esta guía configurarás PhysiLab y ejecutarás tu primer experimento desde cero.

## Requisitos

- Python 3.11 o superior.
- [uv](https://docs.astral.sh/uv/) para gestionar entorno y dependencias.
- Una terminal (PowerShell, Bash o similar).

## 1. Instalar dependencias

Desde la raíz del proyecto:

```bash
uv sync
```

Este comando crea o actualiza el entorno virtual e instala paquetes necesarios.

## 2. Verificar que la CLI funciona

=== "Linux / macOS"
    ```bash
    source .venv/bin/activate
    uv run python main.py --help
    ```

=== "Windows"
    ```powershell
    .venv\Scripts\activate
    uv run python main.py --help
    ```

Si todo está correcto, verás comandos como mru, listar y eliminar.

## 3. Crear tu primer ensayo MRU

```bash
uv run python main.py mru --id 1 --nombre "Ensayo inicial" --velocidad 10 --tiempo 5
```

Qué ocurre al ejecutar:

- Se valida la entrada.
- Se calcula la variable faltante.
- Se guarda el experimento en JSON.
- Se imprime confirmación en consola.

## 4. Listar experimentos guardados

```bash
uv run python main.py listar
```

Verás una tabla con ID, nombre, tipo y resultado.

## 5. Eliminar un experimento

```bash
uv run python main.py eliminar --id 1
```

!!! warning "Regla de ID"
    El ID debe ser positivo y único. Si repites un ID existente, se produce un error de dominio.

## Solución de problemas

| Problema | Solución |
| --- | --- |
| uv no reconocido | Instala uv y reinicia la terminal |
| Error de importación | Ejecuta nuevamente uv sync |
| Opción inválida en comando | Revisa ayuda con uv run python main.py --help |