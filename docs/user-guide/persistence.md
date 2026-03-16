# Persistencia de Datos 💾

PhysiLab utiliza un sistema de almacenamiento ligero basado en archivos planos.

## Estructura JSON
Los datos se guardan en `data/experiments.json`. Los modelos se serializan automáticamente:

```json
{
  "id": 1,
  "tipo": "MRU",
  "datos": {
    "velocidad": 10.0,
    "tiempo": 5.0,
    "distancia": 50.0
  }
}

!!! info "Serialización"
Utilizamos la capacidad de las dataclasses para convertir objetos de Python a diccionarios compatibles con JSON antes de guardar.

