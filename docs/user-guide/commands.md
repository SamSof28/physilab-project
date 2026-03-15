# Comandos CLI

PhysiLab expone una interfaz CLI con tres comandos principales.

## Ver ayuda

```bash
uv run main.py --help
```

Muestra los comandos disponibles y su descripcion.

## Crear ensayo MRU

Comando:

```bash
uv run main.py mru --id 10 --nombre "Carrito" --velocidad 12 --tiempo 4
```

Parametros:

- `--id`: identificador unico del ensayo.
- `--nombre`: nombre descriptivo.
- `--velocidad`: velocidad en m/s.
- `--tiempo`: tiempo en segundos.
- `--distancia`: distancia en metros.

Regla clave:

- Debes proporcionar dos de las tres variables (`velocidad`, `tiempo`, `distancia`).
- La variable faltante se calcula en la capa de servicios.

Ejemplo de salida:

```text
✔ Ensayo registrado.
Resultados: V=12.0 m/s, T=4.0 s, D=48.0 m
```

## Listar ensayos

Comando:

```bash
uv run main.py listar
```

Que hace:

- Carga los datos desde `data/database.json`.
- Muestra una tabla con ID, nombre, tipo, resultado y fecha.

Salida posible cuando no hay datos:

```text
No hay experimentos registrados.
```

## Eliminar ensayo

Comando:

```bash
uv run main.py eliminar --id 10
```

Salida esperada:

```text
✔ Ensayo 10 borrado
```

Error comun:

```text
Error: No se encontro un experimento con id 10
```
