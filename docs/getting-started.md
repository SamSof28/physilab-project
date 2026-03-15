# Primeros pasos

Esta guia te ayuda a levantar el proyecto en local con uv y ejecutar tu primer comando de la CLI.

## Requisitos

- Python 3.14 o superior
- uv instalado en el sistema

## Instalacion con uv

Clona el repositorio y entra al directorio del proyecto:

```bash
git clone https://github.com/SamSof28/physilab-project.git
cd physilab-project
```

Sincroniza dependencias y entorno virtual:

```bash
uv sync
```

## Sincronizar dependencias

Si ya tienes el repositorio, usa nuevamente:

```bash
uv sync
```

Este comando crea/actualiza el entorno virtual y deja instaladas las dependencias definidas en `pyproject.toml`.

## Primer comando de la CLI

Para verificar que la aplicacion esta disponible:

```bash
uv run main.py --help
```

Salida esperada (resumen):

```text
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Commands:
  mru
  listar
  eliminar
```

## Siguiente paso recomendado

Crea tu primer ensayo MRU:

```bash
uv run main.py mru --id 3 --nombre "Ensayo inicial" --velocidad 10 --tiempo 5
```
