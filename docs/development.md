# Guía de desarrollo

Esta sección está dirigida a desarrolladores que deseen contribuir o extender PhysiLab.

---

## 🏗️ Entender la arquitectura

Antes de escribir código, familiarízate con las capas en [Arquitectura](architecture.md):

1. **Presentation** (Streamlit): Interfaz de usuario
2. **API** (FastAPI): Endpoints REST
3. **Business Logic** (PhysicsService): Cálculos físicos
4. **Persistence** (Repository): Acceso a datos
5. **Domain** (Schemas + Exceptions): Validación y contratos

Cada capa es independiente y se comunica mediante interfaces definidas.

---

## 🛠️ Setup de desarrollo

### 1. Clonar y sincronizar

```bash
git clone https://github.com/SamSof28/physilab-project.git
cd physilab-project
uv sync
```

### 2. Crear rama de feature

```bash
git checkout -b feature/mi-caracteristica
```

### 3. Activar entorno

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

---

## 📝 Agregar nuevo modelo físico

Ejemplo: Agregar **Movimiento de Proyectiles**.

### Paso 1: Crear schema en `src/schemas/projectile.py`

```python
from pydantic import BaseModel, Field

class ProjectileSchema(BaseModel):
    angulo_inicial: float = Field(..., ge=0, le=90)
    velocidad_inicial: float = Field(..., gt=0)
    altura_inicial: float = Field(default=0)
    tiempo_vuelo: float | None = None
    alcance_horizontal: float | None = None
    altura_maxima: float | None = None
```

### Paso 2: Extender `PhysicsService` en `src/services/physics_service.py`

```python
def resolver_y_guardar_projectile(self, nombre: str, datos: ProjectileSchema):
    import math
    
    # Cálculos de trayectoria
    g = 9.81
    if datos.tiempo_vuelo is None:
        # Formula: t = 2 * v0 * sin(θ) / g
        rad = math.radians(datos.angulo_inicial)
        datos.tiempo_vuelo = (2 * datos.velocidad_inicial * math.sin(rad)) / g
    
    if datos.alcance_horizontal is None:
        rad = math.radians(datos.angulo_inicial)
        datos.alcance_horizontal = (datos.velocidad_inicial ** 2 * math.sin(2 * rad)) / g
    
    if datos.altura_maxima is None:
        rad = math.radians(datos.angulo_inicial)
        datos.altura_maxima = (datos.velocidad_inicial ** 2 * math.sin(rad) ** 2) / (2 * g)
    
    # Guardar
    exp_maestro = ExperimentCreate(nombre=nombre, tipo="PROJECTILE")
    return self.repository.create_projectile_experiment(exp_maestro, datos.model_dump())
```

### Paso 3: Extender Repository en `src/storage/experiment_repository.py`

```python
def create_projectile_experiment(self, experiment: ExperimentCreate, physics_data: dict):
    # Insertar en experiments y experiments_projectile
    # (requiere crear tabla en Supabase)
    pass
```

### Paso 4: Agregar endpoint en `src/api/routers/experiments.py`

```python
@router.post("/calculate/projectile")
def calculate_projectile(
    nombre: str,
    datos: ProjectileSchema,
    service: PhysicsService = Depends(get_physics_service)
):
    """Calcula y guarda trayectoria de proyectil."""
    return service.resolver_y_guardar_projectile(nombre, datos)
```

### Paso 5: Crear página Streamlit en `src/app/pages/projectile.py`

```python
import streamlit as st
import requests

st.title("🎯 Movimiento de Proyectiles")

col1, col2 = st.columns(2)
with col1:
    angulo = st.number_input("Ángulo inicial (°)", min_value=0, max_value=90)
    velocidad = st.number_input("Velocidad inicial (m/s)", min_value=0.1)

with col2:
    altura = st.number_input("Altura inicial (m)", min_value=0.0)
    nombre = st.text_input("Nombre del ensayo")

if st.button("Calcular"):
    response = requests.post(
        "http://localhost:8000/experiments/calculate/projectile",
        params={"nombre": nombre},
        json={
            "angulo_inicial": angulo,
            "velocidad_inicial": velocidad,
            "altura_inicial": altura
        }
    )
    if response.status_code == 200:
        st.success("✅ Ensayo guardado")
        st.json(response.json())
    else:
        st.error(f"❌ Error: {response.text}")
```

### Paso 6: Crear tabla en Supabase

```sql
CREATE TABLE experiments_projectile (
  id INT PRIMARY KEY REFERENCES experiments(id) ON DELETE CASCADE,
  angulo_inicial FLOAT NOT NULL,
  velocidad_inicial FLOAT NOT NULL,
  altura_inicial FLOAT NOT NULL,
  tiempo_vuelo FLOAT NOT NULL,
  alcance_horizontal FLOAT NOT NULL,
  altura_maxima FLOAT NOT NULL
);
```

✅ **¡Listo!** Ya puedes calcular proyectiles desde la API y Streamlit.

---

## 🧪 Escribir tests

Ejemplo: Test para MRU en `tests/test_services.py`

```python
import pytest
from src.services.physics_service import PhysicsService
from src.schemas.mru import MRUSchema

@pytest.fixture
def service():
    return PhysicsService()

def test_mru_calcular_distancia(service):
    datos = MRUSchema(velocidad=10, tiempo=5, distancia=None)
    resultado = service.resolver_y_guardar_mru("Test MRU", datos)
    assert resultado["distancia"] == 50.0

def test_mru_validar_division_cero(service):
    from src.core.exceptions import ErrorDivisionPorCeroFisica
    datos = MRUSchema(velocidad=0, tiempo=5, distancia=None)
    with pytest.raises(ErrorDivisionPorCeroFisica):
        service.resolver_y_guardar_mru("Test MRU", datos)
```

Ejecutar tests:
```bash
uv run pytest -v
```

---

## 🐛 Debugging

### Activar logs detallados

En `src/core/config.py`:
```python
DEBUG: bool = True
```

### Ver queries SQL

```bash
uv run python -c "
from src.storage.base import BaseRepository
repo = BaseRepository()
# Los logs mostrarán todas las queries
"
```

### Usar debugger

```python
import pdb; pdb.set_trace()  # Breakpoint
```

---

## 📋 Checklist antes de PR

- [ ] Tests nuevos y todos pasan (`uv run pytest`)
- [ ] Documentación actualizada en `/docs`
- [ ] Código sin conflictos de merge
- [ ] Commits atómicos y descriptivos
- [ ] Sin `print()`, usar logs
- [ ] Sin `.env` versionado
- [ ] Seguir convenciones del proyecto

---

## 📚 Convenciones de código

### Nombres
- Módulos: `snake_case` (physics_service.py)
- Clases: `PascalCase` (PhysicsService)
- Funciones: `snake_case` (resolver_y_guardar_mru)
- Variables: `snake_case` (velocidad, tiempo)

### Docstrings
```python
def calcular_distancia(velocidad: float, tiempo: float) -> float:
    """
    Calcula distancia en MRU.
    
    Args:
        velocidad: en m/s
        tiempo: en segundos
    
    Returns:
        Distancia en metros.
    
    Raises:
        ErrorDivisionPorCeroFisica: Si velocidad o tiempo es 0.
    """
    return velocidad * tiempo
```

### Type hints
Siempre incluir tipos:
```python
def crear_experimento(nombre: str, tipo: str) -> ExperimentResponse:
    pass
```

---

## 🚀 Publicar cambios

### 1. Push a rama feature

```bash
git add .
git commit -m "feat: Agregar modelo de proyectiles"
git push origin feature/proyectiles
```

### 2. Crear Pull Request

En GitHub, describe:
- **Qué**: Breve descripción del cambio
- **Por qué**: Motivación o problema resuelto
- **Cómo**: Enfoque técnico
- **Tests**: Incluye ejemplos de ejecución

### 3. Code review

Espera feedback, ajusta si es necesario.

### 4. Merge

Usa "Squash and merge" para mantener historial limpio.

---

## 📖 Referencias útiles

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Pydantic V2](https://docs.pydantic.dev/latest/)
- [Supabase Docs](https://supabase.com/docs)
- [Python Type Hints](https://www.python.org/dev/peps/pep-0484/)

---

## 🤝 Preguntas o problemas

- **Issues**: Abre una discusión en GitHub
- **Discussions**: Debate sobre features
- **PRs**: Propón cambios directamente

¡Bienvenido al proyecto! 🎉
