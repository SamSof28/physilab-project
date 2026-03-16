# Guía de comandos

En esta página tienes una referencia práctica de los comandos disponibles en la CLI de PhysiLab.

## Resumen de comandos

| Comando | Propósito |
| --- | --- |
| mru | Crea y resuelve un ensayo de Movimiento Rectilíneo Uniforme |
| listar | Muestra todos los ensayos guardados en formato tabla |
| eliminar | Elimina un ensayo por su ID |

## Comando mru

Registra un ensayo MRU y calcula automáticamente la variable faltante.

### Sintaxis

```bash
uv run python main.py mru --id <int> --nombre <texto> [--velocidad <float>] [--tiempo <float>] [--distancia <float>]
```

### Parámetros

| Opción | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| --id | int | Sí | Identificador único del experimento |
| --nombre | str | Sí | Nombre descriptivo del ensayo |
| --velocidad | float | No | Velocidad en m/s |
| --tiempo | float | No | Tiempo en segundos |
| --distancia | float | No | Distancia en metros |

!!! info "Regla de cálculo"
    Debes proporcionar exactamente dos de las tres variables físicas para que el sistema calcule la tercera.

### Ejemplo: calcular distancia

```bash
uv run python main.py mru --id 1 --nombre "MRU base" --velocidad 10 --tiempo 5
```

### Ejemplo: calcular velocidad

```bash
uv run python main.py mru --id 2 --nombre "MRU velocidad" --distancia 120 --tiempo 12
```

## Comando listar

Muestra una tabla con el historial de experimentos almacenados.

```bash
uv run python main.py listar
```

## Comando eliminar

Elimina un experimento por su identificador.

```bash
uv run python main.py eliminar --id 2
```

## Errores comunes

| Escenario | Mensaje esperado |
| --- | --- |
| ID repetido | Error por ID duplicado |
| ID inválido (<= 0) | Error de validación de ID |
| Datos insuficientes en MRU | Error por información incompleta |

!!! tip "Buenas prácticas"
    Ejecuta listar después de crear o eliminar ensayos para verificar el estado actual de tu base de datos.