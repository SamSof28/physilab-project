# Persistencia de datos

PhysiLab guarda los experimentos en un archivo JSON local para que no pierdas resultados entre ejecuciones.

## Ubicación del archivo

Por defecto, la aplicación utiliza:

```text
data/database.json
```

Si el archivo no existe, se crea automáticamente cuando guardas el primer experimento.

## Flujo de persistencia

1. Ejecutas un comando en la CLI.
2. El servicio valida y calcula valores faltantes.
3. El experimento se convierte a diccionario.
4. Se escribe la colección completa de ensayos en JSON.

## Estructura JSON esperada

Ejemplo de un registro MRU:

```json
[
  {
    "id": 1,
    "nombre": "MRU base",
    "tipo": "Movimiento Rectilineo Uniforme",
    "fecha": "2026-03-15T10:12:00",
    "velocidad": 10.0,
    "tiempo": 5.0,
    "distancia": 50.0
  }
]
```

!!! info "Serialización"
    La capa de storage convierte instancias de modelos en objetos JSON y, al cargar, reconstruye los modelos según el campo tipo.

## Reglas de consistencia

- Los IDs deben ser únicos.
- Los datos físicos deben cumplir validaciones del dominio.
- Tipos de experimento desconocidos generan excepción.

## Recomendaciones

- Ejecuta listar para comprobar que los ensayos se guardaron correctamente.
- Si quieres historial de cambios, puedes versionar el archivo JSON.
- Para escenarios de mayor escala, puedes extender la capa storage con SQL o API.

