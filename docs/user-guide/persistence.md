# Persistencia de datos

PhysiLab guarda automáticamente los experimentos en **Supabase PostgreSQL** para garantizar persistencia, sincronización en tiempo real y acceso multiusuario.

---

## 🏗️ Estructura de base de datos

### Tabla: `experiments` (Maestra)

Contiene información general de todos los experimentos.

```sql
experiments (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  tipo VARCHAR(20) NOT NULL,           -- 'MRU' o 'MRUA'
  fecha_creacion TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)
```

### Tabla: `experiments_mru` (Especializada)

Almacena datos específicos para experimentos MRU.

```sql
experiments_mru (
  id INT PRIMARY KEY REFERENCES experiments(id) ON DELETE CASCADE,
  velocidad FLOAT NOT NULL,
  tiempo FLOAT NOT NULL,
  distancia FLOAT NOT NULL
)
```

### Tabla: `experiments_mrua` (Especializada)

Almacena datos específicos para experimentos MRUA.

```sql
experiments_mrua (
  id INT PRIMARY KEY REFERENCES experiments(id) ON DELETE CASCADE,
  aceleracion FLOAT NOT NULL,
  velocidad_inicial FLOAT NOT NULL,
  velocidad_final FLOAT NOT NULL,
  posicion_inicial FLOAT NOT NULL,
  posicion_final FLOAT NOT NULL,
  tiempo FLOAT NOT NULL
)
```

!!! info "Diseño normalizado"
    Esta estructura evita redundancia y facilita las consultas específicas de cada tipo de experimento.

---

## 🔄 Flujo de persistencia

```mermaid
sequenceDiagram
    participant User as Usuario
    participant Streamlit as Streamlit<br/>Frontend
    participant API as FastAPI<br/>API
    participant Service as PhysicsService
    participant Repo as Repository
    participant Supabase as Supabase<br/>PostgreSQL

    User->>Streamlit: Ingresa datos MRU
    Streamlit->>API: POST /calculate/mru
    API->>Service: resolver_y_guardar_mru()
    Service->>Service: Calcula variable faltante
    Service->>Repo: create_mru_experiment()
    Repo->>Supabase: INSERT INTO experiments<br/>INSERT INTO experiments_mru
    Supabase-->>Repo: {id, fecha_creacion}
    Repo-->>Service: Confirmación
    Service-->>API: ExperimentResponse
    API-->>Streamlit: JSON con resultado
    Streamlit-->>User: ✅ "Experimento guardado"
```

---

## 📤 Crear experimento (INSERT)

### Desde la API

**Request:**
```bash
curl -X POST "http://localhost:8000/experiments/calculate/mru" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Caída libre",
    "datos": {
      "velocidad": 10,
      "tiempo": 5
    }
  }'
```

**En base de datos:**

Tabla `experiments`:
```
| id | nombre      | tipo | fecha_creacion        |
|----|-------------|------|----------------------|
| 1  | Caída libre | MRU  | 2026-05-17 10:30:00  |
```

Tabla `experiments_mru`:
```
| id | velocidad | tiempo | distancia |
|----|-----------|--------|-----------|
| 1  | 10.0      | 5.0    | 50.0      |
```

---

## 📖 Leer experimentos (SELECT)

### Listar todos

**Request:**
```bash
curl -X GET "http://localhost:8000/experiments"
```

**Consulta SQL interna:**
```sql
SELECT e.*, 
       CASE 
         WHEN e.tipo = 'MRU' THEN row_to_json(m.*)
         WHEN e.tipo = 'MRUA' THEN row_to_json(a.*)
       END as physics_data
FROM experiments e
LEFT JOIN experiments_mru m ON e.id = m.id
LEFT JOIN experiments_mrua a ON e.id = a.id
ORDER BY e.fecha_creacion DESC;
```

### Obtener uno específico

**Request:**
```bash
curl -X GET "http://localhost:8000/experiments/1"
```

**Consulta SQL:**
```sql
SELECT e.*, m.*
FROM experiments e
LEFT JOIN experiments_mru m ON e.id = m.id
WHERE e.id = 1;
```

**Response:**
```json
{
  "id": 1,
  "nombre": "Caída libre",
  "tipo": "MRU",
  "fecha_creacion": "2026-05-17T10:30:00",
  "velocidad": 10.0,
  "tiempo": 5.0,
  "distancia": 50.0
}
```

---

## 🔄 Actualizar experimento (UPDATE)

Actualmente, PhysiLab **no permite actualizaciones**. Para corregir un experimento:

1. **Elimina** el experimento incorrecto: `DELETE /experiments/{id}`
2. **Crea uno nuevo** con los datos correctos: `POST /calculate/mru`

!!! note "Auditoría"
    Esta política preserva la trazabilidad de cambios. En futuras versiones, se agregará historial de modificaciones.

---

## 🗑️ Eliminar experimento (DELETE)

### Endpoint

```bash
curl -X DELETE "http://localhost:8000/experiments/1"
```

### Consulta SQL (con cascada automática)

```sql
DELETE FROM experiments WHERE id = 1;
-- Elimina automáticamente de experiments_mru y experiments_mrua
-- gracias a ON DELETE CASCADE
```

### Response

```json
{
  "message": "Experimento 1 eliminado exitosamente."
}
```

!!! warning "Irreversible"
    El borrado es permanente. No hay papelera de reciclaje.

---

## 🔐 Configuración de Supabase

### Variables de entorno

En `.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

### Obtener credenciales

1. Crea un proyecto en [supabase.com](https://supabase.com)
2. Ve a **Settings → API**
3. Copia:
   - `URL` → `SUPABASE_URL`
   - `anon public` key → `SUPABASE_KEY`

!!! warning "Seguridad"
    Usa un `.env` local, nunca versiones credenciales en Git.

### Políticas de Row Level Security (RLS)

Por defecto, Supabase requiere políticas RLS. Para desarrollo:

```sql
-- Permitir todos los SELECT
CREATE POLICY "Allow read all" ON experiments
  FOR SELECT USING (true);

-- Permitir INSERT solo con autenticación
CREATE POLICY "Allow insert authenticated" ON experiments
  FOR INSERT WITH CHECK (true);

-- Permitir DELETE solo con autenticación
CREATE POLICY "Allow delete authenticated" ON experiments
  FOR DELETE USING (true);
```

---

## 💡 Buenas prácticas

### 1. Backups regulares

Supabase mantiene backups automáticos. Para exportar:
```bash
# Usando pg_dump (requiere acceso directo)
pg_dump "postgresql://user:password@host/db" > backup.sql
```

### 2. Monitoreo de eventos

Suscríbete a cambios en Streamlit:
```python
import streamlit as st

@st.cache_resource
def get_realtime_listener():
    # Futura integración de WebSockets para sync en tiempo real
    pass
```

### 3. Validación en origen

Siempre valida datos antes de enviar a la API:
```python
if velocidad <= 0 or tiempo <= 0:
    st.error("Velocidad y tiempo deben ser > 0")
```

### 4. Logging de operaciones

El logger interno registra:
- Experimentos creados (ID, tipo, fecha)
- Errores de validación
- Fallos de conexión a Supabase

---

## 📊 Estadísticas de uso

Para consultar estadísticas:

```sql
-- Total de experimentos
SELECT COUNT(*) as total_experiments FROM experiments;

-- Por tipo
SELECT tipo, COUNT(*) as cantidad
FROM experiments
GROUP BY tipo;

-- Más recientes
SELECT nombre, tipo, fecha_creacion
FROM experiments
ORDER BY fecha_creacion DESC
LIMIT 10;
```

---

## 🚀 Escalabilidad

### Índices (en producción)

```sql
CREATE INDEX idx_experiments_tipo ON experiments(tipo);
CREATE INDEX idx_experiments_fecha ON experiments(fecha_creacion DESC);
```

### Particionamiento (para 1M+ registros)

```sql
-- Particionar por año
CREATE TABLE experiments_2026 PARTITION OF experiments
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

### Replicación

Supabase replica automáticamente a múltiples regiones para alta disponibilidad.

---

## 🔧 Troubleshooting

| Problema | Solución |
| --- | --- |
| `Connection refused` | Verifica `SUPABASE_URL` y que el proyecto está activo |
| `Unauthorized` | Comprueba que `SUPABASE_KEY` es la clave "anon public" |
| `Table not found` | Ejecuta SQL en Supabase para crear `experiments` tabla |
| `Constraint violation` | El ID ya existe (violación de PRIMARY KEY) |
| `Timeout` | La red está lenta; intenta nuevamente o aumenta timeout |

!!! tip "Debug"
    Activa logs en `src/core/config.py` con `DEBUG=true` para ver queries SQL.

