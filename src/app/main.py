import streamlit as st


st.set_page_config(page_title="PhysiLab Digital", page_icon="🔬", layout="wide")

st.title("🔬 PhysiLab Digital")
st.caption("Plataforma web para registrar, analizar y consultar ensayos de cinemática.")

st.divider()

st.header("Resumen del proyecto")
col_1, col_2, col_3 = st.columns(3)

with col_1:
    st.metric("Modelos físicos", "2", help="MRU y MRUA")

with col_2:
    st.metric("Backend", "FastAPI", help="Endpoints REST para cálculo y consulta")

with col_3:
    st.metric("Persistencia", "Supabase", help="Base de datos PostgreSQL administrada")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Qué puedes hacer")
    st.write("Registrar ensayos desde formularios simples con cálculos automáticos.")
    st.write("Consultar el historial y abrir detalles con gráficos interactivos.")
    st.write("Explorar resultados con Plotly para comparar posición, velocidad y aceleración.")

with right:
    st.subheader("Ruta de trabajo")
    st.write("1. Abre la página de Ensayos para crear registros.")
    st.write("2. Usa MRU si necesitas un acceso rápido al cálculo uniforme.")
    st.write("3. Revisa Análisis para ver gráficas y métricas del experimento guardado.")

st.divider()

st.subheader("Acceso rápido")
st.info("Usa el menú lateral para abrir Ensayos, MRU y Análisis.")
st.code("uv run fastapi dev src/api/main.py", language="bash")
st.code("uv run streamlit run src/app/main.py", language="bash")

st.success("PhysiLab está listo para una nueva sesión experimental.")