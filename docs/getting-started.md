# Primeros pasos

En esta guía instalarás PhysiLab, configurarás Supabase y ejecutarás tu primer experimento desde cero.

---

## 📋 Requisitos

- **Python**: 3.14 o superior.
- **uv**: Gestor de dependencias moderno (instala desde [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)).
- **Supabase**: Proyecto activo con credenciales (URL y API Key).
- **Terminal**: Bash, PowerShell o equivalente.
- **Git**: Para clonar el repositorio.

---

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/SamSof28/physilab-project.git
cd physilab-project
```

---

## 2️⃣ Instalar dependencias con uv

```bash
uv sync
```

Este comando:
- Crea o actualiza el entorno virtual.
- Instala todas las dependencias del `pyproject.toml`.
- Configura el proyecto para desarrollo inmediato.

---

## 3️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
touch .env
```

Edítalo e ingresa tus credenciales de Supabase:

```env
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# FastAPI (opcional)
API_BASE_URL=http://localhost:8000
DEBUG=true
```

!!! warning "Seguridad"
    Nunca versiones `.env` en Git. Asegúrate de que `.gitignore` lo excluya.

---

## 4️⃣ Verificar la instalación

=== "Linux / macOS"
    ```bash
    source .venv/bin/activate
    uv run python -c "import src; print('✅ Proyecto importable')"
    ```

=== "Windows"
    ```powershell
    .venv\Scripts\activate
    uv run python -c "import src; print('✅ Proyecto importable')"
    ```

Si ves `✅ Proyecto importable`, estás listo.

---

## 5️⃣ Ejecutar el backend (FastAPI)

En una terminal:

```bash
uv run fastapi dev src/api/main.py
```

Verás:
```
Uvicorn running on http://127.0.0.1:8000
```

Abre tu navegador en [http://localhost:8000/docs](http://localhost:8000/docs) para ver la documentación interactiva de la API (Swagger UI).

---

## 6️⃣ Ejecutar el frontend (Streamlit)

En otra terminal:

```bash
uv run streamlit run src/app/main.py
```

Se abrirá automáticamente en [http://localhost:8501](http://localhost:8501).

---

## 7️⃣ Crear tu primer ensayo MRU desde la API

Con FastAPI ejecutándose, abre [http://localhost:8000/docs](http://localhost:8000/docs) y:

1. Localiza **POST /experiments/calculate/mru**
2. Haz clic en **"Try it out"**
3. Completa los parámetros (ejemplo):
   ```json
   {
     "nombre": "Primer MRU",
     "datos": {
       "velocidad": 10,
       "tiempo": 5
     }
   }
   ```
4. Haz clic en **"Execute"**

Resultado esperado:
```json
{
  "id": 1,
  "nombre": "Primer MRU",
  "tipo": "MRU",
  "fecha_creacion": "2026-05-17T10:30:00",
  "distancia": 50.0
}
```

---

## 8️⃣ Crear ensayo desde Streamlit

1. Navega a la sección de **Registro de ensayos** en Streamlit.
2. Selecciona el tipo: **MRU**.
3. Ingresa nombre y datos conocidos.
4. Haz clic en **"Calcular y guardar"**.

Verás el resultado con la variable calculada.

---

## Solución de problemas

| Problema | Solución |
| --- | --- |
| `ModuleNotFoundError: src` | Ejecuta `uv sync` nuevamente |
| `ERROR: No SUPABASE_URL encontrada` | Revisa `.env` con credenciales correctas |
| Puerto 8000 ocupado | Ejecuta `uv run fastapi dev src/api/main.py --port 8001` |
| Puerto 8501 ocupado | Ejecuta `uv run streamlit run src/app/main.py --server.port 8502` |
| Conexión rechazada a Supabase | Verifica URL y API Key, y asegúrate que la tabla `experiments` existe |

---

## Próximos pasos

✅ **Frontend**: Explora las páginas de registro y análisis en Streamlit.  
✅ **API**: Consulta la [Guía de Usuario](user-guide/commands.md) para endpoints disponibles.  
✅ **Arquitectura**: Entiende el diseño completo en [Arquitectura](architecture.md).