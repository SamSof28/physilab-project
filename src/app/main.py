import streamlit as st

st.set_page_config(page_title="PhysiLab Digital", page_icon="🔬", layout="wide")

st.title("🔬 PhysiLab Digital")
st.caption("Cuaderno de laboratorio de física para registrar, analizar y consultar ensayos experimentales.")

st.divider()

st.header("Bienvenida")
st.write(
    "PhysiLab es una plataforma orientada a estudiantes y docentes para organizar prácticas "
    "de cinemática con estructura clara, resultados reproducibles y seguimiento de ensayos."
)
st.write(
    "Desde esta interfaz puedes acceder a módulos de registro y análisis, mientras mantienes "
    "la compatibilidad con el flujo de trabajo por línea de comandos del proyecto."
)

st.divider()

st.header("Resumen del Proyecto")
metric_1, metric_2, metric_3 = st.columns(3)

with metric_1:
    st.metric(label="Modelos cinemáticos", value="2", help="MRU y MRUA")

with metric_2:
    st.metric(label="Persistencia", value="JSON", help="Registro histórico de ensayos")

with metric_3:
    st.metric(label="Interfaz", value="CLI + Web", help="Flujo híbrido para aprendizaje y práctica")

st.divider()

st.header("Qué puedes hacer en PhysiLab")
col_1, col_2 = st.columns(2)

with col_1:
    st.subheader("Registro de ensayos")
    st.write("Crea y guarda experimentos con datos consistentes para mantener trazabilidad.")
    st.write("Incluye variables físicas relevantes para análisis posterior.")

    st.subheader("Gestión de historial")
    st.write("Consulta ensayos previos y organiza tu trabajo de laboratorio por sesiones.")
    st.write("Facilita el seguimiento de avances académicos y comparaciones entre pruebas.")

with col_2:
    st.subheader("Análisis de resultados")
    st.write("Interpreta comportamientos de movimiento con apoyo de una vista más visual.")
    st.write("Revisa rápidamente resultados clave para discusión en clase o informe.")

    st.subheader("Aprendizaje aplicado")
    st.write("Conecta teoría de física con práctica experimental en un entorno digital.")
    st.write("Ideal para cursos introductorios y actividades de laboratorio guiadas.")

st.divider()

st.header("Navegación")
st.info("Usa el menú lateral para abrir las páginas de Ensayos y Análisis.")

st.header("Comando recomendado")
st.code("PYTHONPATH=. streamlit run interfaces/streamlit_app/app.py", language="bash")

st.success("PhysiLab listo para comenzar una nueva sesión experimental.")