# Persistencia

La persistencia de PhysiLab se implementa con un archivo JSON local y una clase de almacenamiento dedicada.

## Archivo JSON

Ubicacion por defecto:

```text
data/database.json
```

Cada vez que registras o eliminas un ensayo desde la CLI, la operacion termina leyendo y escribiendo este archivo.

## Estructura de los datos

Ejemplo de registro persistido:

```json
{
  "id": 1,
  "nombre": "Ensayo Carrito Madera",
  "tipo": "Movimiento Rectilineo Uniforme",
  "fecha": "2026-02-22 10:00",
  "velocidad": 10.5,
  "distancia": 52.5,
  "tiempo": 5.0
}
```

Campos de uso general:

- `id`: identificador unico.
- `nombre`: nombre del ensayo.
- `tipo`: tipo de movimiento.
- `fecha`: marca temporal del experimento.

Campos fisicos:

- para MRU: `velocidad`, `distancia`, `tiempo`.
- para MRUA: `posicion_inicial`, `velocidad_inicial`, `aceleracion`, `tiempo`, `posicion_final`, `velocidad_final`.

## Serializacion y deserializacion

El flujo en `JsonStorage` sigue este patron:

1. `load()` abre el JSON y convierte cada item en su dataclass de dominio.
2. `save(...)` recibe una lista de modelos y serializa con `experiment.__dict__`.

Ventajas del enfoque:

- simple de inspeccionar y depurar;
- sin dependencia de base de datos externa;
- desacoplado por una interfaz de almacenamiento, lo que permite migrar a SQL sin romper la capa de servicios.

## Consideraciones de calidad

- Si el archivo no existe, `load()` devuelve lista vacia.
- Si el tipo de experimento no coincide con uno valido, se lanza una excepcion de dominio.
