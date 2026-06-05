import streamlit as st
import sys
from pathlib import Path
from src.app.ui import apply_theme, render_hero, render_topbar

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


st.set_page_config(
    page_title="PhysiLab - Laboratorio Virtual", page_icon="🧪", layout="wide"
)

# Invocar la barra de navegación personalizada pasándole el contexto actual
render_topbar("Inicio")
apply_theme()

render_hero(
    "Bienvenido a PhysiLab",
    "Plataforma de simulación y registro de ensayos de cinemática conectada a FastAPI, Plotly y Supabase.",
    tag="Laboratorio digital",
)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Lo que puedes hacer")
    st.write("- Crear experimentos MRU y MRUA desde formularios guiados.")
    st.write("- Ver gráficos interactivos vectoriales generados por Plotly.")
    st.write("- Controlar y auditar los registros en tiempo real en Supabase.")

with col2:
    st.subheader("Estado del sistema")
    st.write(
        "Backend FastAPI listo para recibir experimentos y frontend conectado al API."
    )
    st.metric(label="Flujo objetivo", value="100%", delta="Frontend + API + DB")

st.markdown("### Acciones rápidas")
quick1, quick2, quick3 = st.columns(3)
with quick1:
    st.page_link("pages/mru.py", label="📊 Abrir Laboratorio MRU")
with quick2:
    st.page_link("pages/mrua.py", label="🚀 Abrir Laboratorio MRUA")
with quick3:
    st.page_link("pages/historial.py", label="🗄️ Ver consola de Historial")
