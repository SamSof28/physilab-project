# Guía de API REST

En esta página tienes una referencia práctica de los endpoints disponibles en la API REST de PhysiLab.

---

## 🎯 Base URL

```
http://localhost:8000
```

Todos los endpoints están prefijados con `/experiments`.

---

## 📚 Resumen de endpoints

| Método | Endpoint | Propósito |
| --- | --- | --- |
| **POST** | `/calculate/mru` | Registra y resuelve un MRU |
| **POST** | `/calculate/mrua` | Registra y resuelve un MRUA |
| **GET** | `` (raíz) | Lista todos los experimentos |
| **GET** | `/{id}` | Obtiene detalles de un experimento |
| **DELETE** | `/{id}` | Elimina un experimento |

---

## 📝 Crear un experimento MRU

Calcula automáticamente la variable faltante en un Movimiento Rectilíneo Uniforme.

### Endpoint

```http
POST /experiments/calculate/mru
```

### Parámetros (Body - JSON)

```json
{
  "nombre": "string (obligatorio)",
  "datos": {
    "velocidad": "float (opcional)",
    "tiempo": "float (opcional)",
    "distancia": "float (opcional)"
  }
}
```

!!! info "Regla de cálculo"
    Proporciona **exactamente dos de tres** variables. PhysiLab calcula la tercera.

### Ejemplo: Calcular distancia

**Solicitud:**
```bash
curl -X POST "http://localhost:8000/experiments/calculate/mru" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "MRU base",
    "datos": {
      "velocidad": 10,
      "tiempo": 5
    }
  }'
```

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "MRU base",
  "tipo": "MRU",
  "fecha_creacion": "2026-05-17T10:30:00",
  "distancia": 50.0
}
```

### Ejemplo: Calcular velocidad

**Solicitud:**
```bash
curl -X POST "http://localhost:8000/experiments/calculate/mru" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Velocidad desconocida",
    "datos": {
      "distancia": 120,
      "tiempo": 12
    }
  }'
```

**Respuesta (200 OK):**
```json
{
  "id": 2,
  "nombre": "Velocidad desconocida",
  "tipo": "MRU",
  "fecha_creacion": "2026-05-17T10:31:00",
  "velocidad": 10.0
}
```

### Errores comunes

| Código | Escenario |
| --- | --- |
| **400** | Faltan o sobran variables (no son exactamente 2) |
| **400** | Divisiones por cero (tiempo o velocidad = 0) |
| **422** | Datos inválidos (non-numeric, tipos incorrectos) |

---

## 📝 Crear un experimento MRUA

Calcula automáticamente variables en un Movimiento Rectilíneo Uniformemente Acelerado.

### Endpoint

```http
POST /experiments/calculate/mrua
```

### Parámetros (Body - JSON)

```json
{
  "nombre": "string (obligatorio)",
  "datos": {
    "aceleracion": "float (opcional)",
    "velocidad_inicial": "float (obligatorio)",
    "velocidad_final": "float (opcional)",
    "posicion_inicial": "float (obligatorio)",
    "posicion_final": "float (opcional)",
    "tiempo": "float (opcional)"
  }
}
```

!!! info "Configuración MRUA"
    Se requieren velocidad inicial y posición inicial. El sistema calcula lo faltante usando ecuaciones cinemáticas.

### Ejemplo: Calcular aceleración

**Solicitud:**
```bash
curl -X POST "http://localhost:8000/experiments/calculate/mrua" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Aceleración en plano inclinado",
    "datos": {
      "velocidad_inicial": 0,
      "velocidad_final": 20,
      "tiempo": 4,
      "posicion_inicial": 0
    }
  }'
```

**Respuesta (200 OK):**
```json
{
  "id": 3,
  "nombre": "Aceleración en plano inclinado",
  "tipo": "MRUA",
  "fecha_creacion": "2026-05-17T10:32:00",
  "aceleracion": 5.0,
  "posicion_final": 40.0
}
```

---

## 📋 Listar todos los experimentos

Obtiene el historial completo de experimentos guardados.

### Endpoint

```http
GET /experiments
```

### Respuesta (200 OK)

```json
[
  {
    "id": 1,
    "nombre": "MRU base",
    "tipo": "MRU",
    "fecha_creacion": "2026-05-17T10:30:00"
  },
  {
    "id": 2,
    "nombre": "Velocidad desconocida",
    "tipo": "MRU",
    "fecha_creacion": "2026-05-17T10:31:00"
  },
  {
    "id": 3,
    "nombre": "Aceleración en plano inclinado",
    "tipo": "MRUA",
    "fecha_creacion": "2026-05-17T10:32:00"
  }
]
```

### Ejemplo con curl

```bash
curl -X GET "http://localhost:8000/experiments"
```

---

## 🔍 Obtener detalles de un experimento

Recupera toda la información de un experimento específico, incluyendo datos físicos calculados.

### Endpoint

```http
GET /experiments/{id}
```

### Parámetros

| Parámetro | Tipo | Ubicación | Descripción |
| --- | --- | --- | --- |
| `id` | int | Path | ID único del experimento |

### Respuesta (200 OK)

```json
{
  "id": 1,
  "nombre": "MRU base",
  "tipo": "MRU",
  "fecha_creacion": "2026-05-17T10:30:00",
  "velocidad": 10.0,
  "tiempo": 5.0,
  "distancia": 50.0
}
```

### Ejemplo con curl

```bash
curl -X GET "http://localhost:8000/experiments/1"
```

### Error 404

Si el ID no existe:
```json
{
  "detail": "El experimento con ID 999 no existe."
}
```

---

## 🗑️ Eliminar un experimento

Elimina un experimento de la base de datos.

### Endpoint

```http
DELETE /experiments/{id}
```

### Parámetros

| Parámetro | Tipo | Ubicación |
| --- | --- | --- |
| `id` | int | Path |

### Respuesta (200 OK)

```json
{
  "message": "Experimento 1 eliminado exitosamente."
}
```

### Ejemplo con curl

```bash
curl -X DELETE "http://localhost:8000/experiments/1"
```

### Error 404

Si el ID no existe:
```json
{
  "detail": "No se encontró el experimento 1 para eliminar."
}
```

---

## 🛠️ Explorar la API interactivamente

FastAPI genera documentación automática. Abre tu navegador en:

**Swagger UI (Recomendado):**
```
http://localhost:8000/docs
```

**ReDoc (Alternativa):**
```
http://localhost:8000/redoc
```

En Swagger UI puedes:
- Ver todos los endpoints.
- Leer descripciones y parámetros.
- Ejecutar requests directamente.
- Ver respuestas y códigos de error.

---

## 📊 Códigos de estado HTTP

| Código | Significado |
| --- | --- |
| **200** | OK - Operación exitosa |
| **201** | Created - Recurso creado |
| **400** | Bad Request - Datos inválidos o lógica rechazada |
| **404** | Not Found - Experimento no existe |
| **422** | Unprocessable Entity - Validación de esquema fallida |
| **502** | Bad Gateway - Error de conexión a Supabase |

---

## 💡 Buenas prácticas

1. **Valida antes de enviar**: Verifica que proporciones exactamente 2 variables en MRU.
2. **Captura errores**: Implementa reintentos para errores 502 (DB).
3. **Caching**: Almacena resultados del GET `/experiments` para reducir latencia.
4. **Logging**: Registra IDs de experimentos para auditoría.

!!! tip "Testing"
    Usa Postman, Insomnia o curl para probar endpoints durante desarrollo.