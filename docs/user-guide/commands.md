# Guía de Comandos 💻

Aprende a ejecutar cálculos físicos directamente desde tu terminal.

## Cálculo de MRU
Para calcular una variable de Movimiento Rectilíneo Uniforme, deja la variable que buscas como `None`.

**Ejemplo: Calcular distancia**
`uv run main.py mru --velocidad 10 --tiempo 5`

!!! example "Salida esperada"
    ```text
    ✅ Ensayo MRU guardado:
    ID: 1 | Velocidad: 10.0 m/s | Tiempo: 5.0 s | Distancia: 50.0 m
    ```

## Cálculo de MRUA
`uv run main.py mrua --v_inicial 0 --aceleracion 9.8 --tiempo 2`