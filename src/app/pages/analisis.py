import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


API_BASE = "http://localhost:8000/experiments"


@st.cache_data(ttl=20)
def cargar_experimentos() -> list[dict]:
    response = requests.get(API_BASE, timeout=20)
    response.raise_for_status()
    return response.json()


def cargar_detalle(exp_id: int) -> dict:
    response = requests.get(f"{API_BASE}/{exp_id}", timeout=20)
    response.raise_for_status()
    return response.json()


def construir_dataframe(detalle: dict) -> pd.DataFrame:
    tipo = detalle.get("tipo")
    physics = detalle.get("detalle", {})

    if tipo == "MRUA":
        tiempo = float(physics.get("tiempo") or 1)
        t = np.linspace(0, max(tiempo, 1.0), 100)
        x0 = float(physics.get("posicion_inicial") or 0)
        v0 = float(physics.get("velocidad_inicial") or 0)
        a = float(physics.get("aceleracion") or 0)
        x = x0 + v0 * t + 0.5 * a * t**2
        v = v0 + a * t
        acc = np.full_like(t, a)
    else:
        tiempo = float(physics.get("tiempo") or 1)
        t = np.linspace(0, max(tiempo, 1.0), 100)
        v0 = float(physics.get("velocidad") or 0)
        x = v0 * t
        v = np.full_like(t, v0)
        acc = np.zeros_like(t)

    return pd.DataFrame({
        "Tiempo (s)": t,
        "Posición (m)": x,
        "Velocidad (m/s)": v,
        "Aceleración (m/s²)": acc,
    })


def crear_figura(df: pd.DataFrame, variable: str, titulo: str) -> go.Figure:
    fig = px.line(df, x="Tiempo (s)", y=variable, title=titulo)
    fig.update_traces(line_width=3)
    fig.update_layout(hovermode="x unified", template="plotly_white")
    return fig


st.set_page_config(page_title="Análisis - PhysiLab", page_icon="📊", layout="wide")

st.title("📊 Análisis de ensayos")
st.caption("Selecciona un experimento guardado para revisar sus métricas y gráficas.")

try:
    experimentos = cargar_experimentos()
except requests.RequestException as exc:
    st.error(f"No se pudo cargar el historial: {exc}")
    st.stop()

if not experimentos:
    st.warning("Todavía no hay ensayos guardados.")
    st.stop()

opciones = {f"{item['nombre']} ({item['tipo']}) - {item['fecha_creacion']}": item["id"] for item in experimentos}
seleccion = st.sidebar.selectbox("Selecciona un ensayo", list(opciones.keys()))
detalle = cargar_detalle(opciones[seleccion])
physics = detalle.get("detalle", {})

st.header(detalle.get("nombre", "Ensayo"))
st.caption(f"Tipo: {detalle.get('tipo', '')} | Fecha: {detalle.get('fecha_creacion', '')}")

if detalle.get("tipo") == "MRUA":
    distancia = float(physics.get("posicion_final", 0)) - float(physics.get("posicion_inicial", 0))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocidad inicial", f"{float(physics.get('velocidad_inicial', 0)):.2f} m/s")
    col2.metric("Velocidad final", f"{float(physics.get('velocidad_final', 0)):.2f} m/s")
    col3.metric("Aceleración", f"{float(physics.get('aceleracion', 0)):.2f} m/s²")
    col4.metric("Tiempo", f"{float(physics.get('tiempo', 0)):.2f} s")

    col5, col6 = st.columns(2)
    col5.metric("Posición inicial", f"{float(physics.get('posicion_inicial', 0)):.2f} m")
    col6.metric("Posición final", f"{float(physics.get('posicion_final', 0)):.2f} m")

    df = construir_dataframe(detalle)
    st.subheader("Gráficas")
    tab_pos, tab_vel, tab_acc = st.tabs(["Posición", "Velocidad", "Aceleración"])

    with tab_pos:
        st.plotly_chart(crear_figura(df, "Posición (m)", "Posición vs Tiempo"), use_container_width=True)

    with tab_vel:
        st.plotly_chart(crear_figura(df, "Velocidad (m/s)", "Velocidad vs Tiempo"), use_container_width=True)

    with tab_acc:
        st.plotly_chart(crear_figura(df, "Aceleración (m/s²)", "Aceleración vs Tiempo"), use_container_width=True)

    st.subheader("Resumen del movimiento")
    st.write(f"Distancia recorrida: {distancia:.2f} m")
    st.write(
        f"Velocidad promedio: {((float(physics.get('velocidad_inicial', 0)) + float(physics.get('velocidad_final', 0))) / 2):.2f} m/s"
    )

else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocidad", f"{float(physics.get('velocidad', 0)):.2f} m/s")
    col2.metric("Distancia", f"{float(physics.get('distancia', 0)):.2f} m")
    col3.metric("Tiempo", f"{float(physics.get('tiempo', 0)):.2f} s")
    col4.metric("Aceleración", "0.00 m/s²")

    df = construir_dataframe(detalle)
    st.subheader("Gráficas")
    tab_pos, tab_vel, tab_acc = st.tabs(["Posición", "Velocidad", "Aceleración"])

    with tab_pos:
        st.plotly_chart(crear_figura(df, "Posición (m)", "Posición vs Tiempo"), use_container_width=True)

    with tab_vel:
        st.plotly_chart(crear_figura(df, "Velocidad (m/s)", "Velocidad vs Tiempo"), use_container_width=True)

    with tab_acc:
        st.plotly_chart(crear_figura(df, "Aceleración (m/s²)", "Aceleración vs Tiempo"), use_container_width=True)