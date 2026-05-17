# Referencia técnica

Esta sección documenta los módulos principales, esquemas y servicios de PhysiLab. Consulta las firmas, clases, métodos y contratos internos del proyecto.

---

## 🎨 Frontend (Streamlit)

Módulo principal de presentación web.

**Ubicación**: `src/app/main.py`

### Funcionalidades
- Página de inicio con métricas del proyecto.
- Formularios para registro de MRU y MRUA.
- Listado y búsqueda de experimentos.
- Visualizaciones gráficas de resultados.

---

## ⚡ API REST (FastAPI)

Exposición de endpoints CRUD para experimentos.

**Ubicación**: `src/api/main.py`

### Endpoints principales
```
POST   /experiments/calculate/mru      → Crear y guardar MRU
POST   /experiments/calculate/mrua     → Crear y guardar MRUA
GET    /experiments                    → Listar todos
GET    /experiments/{id}               → Obtener detalles
DELETE /experiments/{id}               → Eliminar
```

### Documentación interactiva
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔬 Lógica de Física (Services)

**Clase**: `PhysicsService`  
**Ubicación**: `src/services/physics_service.py`

### Métodos principales

#### `resolver_y_guardar_mru(nombre: str, datos: MRUSchema)`
Resuelve MRU y persiste resultado.
- Requiere exactamente 2 de 3 variables: velocidad, tiempo, distancia
- Calcula la variable faltante
- Retorna `ExperimentResponse` con resultado

#### `resolver_y_guardar_mrua(nombre: str, datos: MRUASchema)`
Resuelve MRUA usando ecuaciones cinemáticas.
- Requiere velocidad inicial y posición inicial
- Calcula aceleración, tiempo, posición final y velocidad final según sea necesario
- Retorna `ExperimentResponse` con resultado

#### `list_all()`
Retorna lista de todos los experimentos.

#### `get_one(exp_id: int)`
Retorna un experimento específico con todos sus datos.

#### `remove_one(exp_id: int) -> bool`
Elimina un experimento y retorna confirmación.

---

## 📋 Esquemas de Validación (Pydantic)

**Ubicación**: `src/schemas/`

### ExperimentCreate
```python
class ExperimentCreate(BaseModel):
	nombre: str          # Min 3, Max 100 caracteres
	tipo: str            # 'MRU' o 'MRUA'
```

### MRUSchema
```python
class MRUSchema(BaseModel):
	velocidad: float | None      # m/s
	tiempo: float | None         # s
	distancia: float | None      # m
```

!!! info "Regla MRU"
	Proporciona exactamente 2 de 3 variables.

### MRUASchema
```python
class MRUASchema(BaseModel):
	aceleracion: float | None             # m/s²
	velocidad_inicial: float              # m/s (obligatorio)
	velocidad_final: float | None         # m/s
	posicion_inicial: float               # m (obligatorio)
	posicion_final: float | None          # m
	tiempo: float | None                  # s
```

---

## 💾 Persistencia (Storage)

**Clase**: `ExperimentRepository`  
**Ubicación**: `src/storage/experiment_repository.py`  
**Backend**: Supabase PostgreSQL

### Métodos principales

#### `create_mru_experiment(experiment: ExperimentCreate, physics_data: dict)`
Inserta MRU en tablas `experiments` y `experiments_mru`.

#### `create_mrua_experiment(experiment: ExperimentCreate, physics_data: dict)`
Inserta MRUA en tablas `experiments` y `experiments_mrua`.

#### `get_all() -> List[ExperimentResponse]`
Consulta todos los experimentos con JOIN a tablas especializadas.

#### `get_by_id(exp_id: int) -> ExperimentResponse`
Obtiene un experimento con todos sus datos físicos.

#### `delete(exp_id: int) -> bool`
Elimina experimento (con cascada automática).

---

## 🛡️ Excepciones personalizadas

**Ubicación**: `src/core/exceptions.py`

### Jerarquía
```
AppError (base)
├── NotFoundError        → HTTP 404
├── DuplicateError       → HTTP 409
├── ValidationError      → HTTP 422
├── StorageError         → HTTP 502
└── [Excepciones físicas]
	├── ErrorDivisionPorCeroFisica
	└── ErrorDiscriminanteNegativo
```

### Ejemplo: Capturar ErrorDivisionPorCeroFisica
```python
try:
	service.resolver_y_guardar_mru("test", datos)
except ErrorDivisionPorCeroFisica as e:
	return {"error": f"División por cero en {e.magnitud}"}
```

---

## ⚙️ Configuración

**Ubicación**: `src/core/config.py`

### Settings (Variables de entorno)
```python
SUPABASE_URL: str           # URL del proyecto Supabase
SUPABASE_KEY: str           # API Key pública
API_BASE_URL: str = "http://localhost:8000"
API_TITLE: str = "PhysiLab API - Laboratorio de Física"
API_VERSION: str = "1.0.0"
DEBUG: bool = True
```

---

## 📊 Dependencias e inyección

**Ubicación**: `src/api/dependencies.py`

### Función: `get_physics_service()`
Inyecta una instancia de `PhysicsService` en los endpoints.

**Ejemplo en un endpoint:**
```python
@router.post("/calculate/mru")
def calculate_mru(
	nombre: str,
	datos: MRUSchema,
	service: PhysicsService = Depends(get_physics_service)
):
	return service.resolver_y_guardar_mru(nombre, datos)
```

---

## 🔄 Estructura de base de datos

### Tabla: experiments
```sql
id (SERIAL PRIMARY KEY)
nombre (VARCHAR 100)
tipo (VARCHAR 20) -- 'MRU' o 'MRUA'
fecha_creacion (TIMESTAMP)
```

### Tabla: experiments_mru
```sql
id (INT PRIMARY KEY, FK experiments)
velocidad (FLOAT)
tiempo (FLOAT)
distancia (FLOAT)
```

### Tabla: experiments_mrua
```sql
id (INT PRIMARY KEY, FK experiments)
aceleracion (FLOAT)
velocidad_inicial (FLOAT)
velocidad_final (FLOAT)
posicion_inicial (FLOAT)
posicion_final (FLOAT)
tiempo (FLOAT)
```

---

## 📚 Librerías principales

| Librería | Propósito |
| --- | --- |
| **Pydantic V2** | Validación y serialización de esquemas |
| **FastAPI** | Framework web asincrónico |
| **Streamlit** | Frontend interactivo |
| **Supabase** | Cliente PostgreSQL |
| **NumPy** | Cálculos matemáticos |
| **Plotly** | Visualizaciones |

---

## 🚀 Próximas características

- WebSockets para sincronización en tiempo real
- Historial de cambios (auditoría)
- Nuevos modelos físicos (fuerzas, energías)
- Autenticación de usuarios
- Exportación de reportes (PDF, Excel)
