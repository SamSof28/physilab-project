import numpy as np
import plotly.graph_objects as go
import requests
import streamlit as st


API_URL = "http://localhost:8000/experiments/calculate/mru"


def construir_figura_mru(detalle: dict) -> go.Figure:
    tiempo = float(detalle.get("tiempo") or 0)
    velocidad = float(detalle.get("velocidad") or 0)
    t = np.linspace(0, max(tiempo, 1.0), 100)
    posicion = velocidad * t
    velocidad_constante = np.full_like(t, velocidad)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=posicion, mode="lines", name="Posición", line=dict(color="#00d1ff", width=3)))
    fig.add_trace(go.Scatter(x=t, y=velocidad_constante, mode="lines", name="Velocidad", line=dict(color="#ff006e", width=3)))
    fig.update_layout(
        title=f"Comportamiento MRU - {detalle.get('nombre', 'Ensayo')}",
        xaxis_title="Tiempo (s)",
        yaxis_title="Valor",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


st.set_page_config(page_title="MRU - PhysiLab", page_icon="🧪", layout="wide")

st.title("🧪 Laboratorio de MRU")
st.caption("Registra un movimiento rectilíneo uniforme y calcula la variable faltante.")

with st.form("mru_form"):
    nombre = st.text_input("Nombre del ensayo", placeholder="Ej: Carrito de madera 01")
    variable_faltante = st.radio(
        "Variable a calcular",
        ["Distancia", "Velocidad", "Tiempo"],
        horizontal=True,
    )

    col1, col2 = st.columns(2)

    if variable_faltante == "Distancia":
        velocidad = col1.number_input("Velocidad (m/s)", min_value=0.0, step=0.1, format="%.2f")
        tiempo = col2.number_input("Tiempo (s)", min_value=0.0, step=0.1, format="%.2f")
        payload = {"velocidad": velocidad, "tiempo": tiempo, "distancia": None}
    elif variable_faltante == "Velocidad":
        distancia = col1.number_input("Distancia (m)", min_value=0.0, step=0.1, format="%.2f")
        tiempo = col2.number_input("Tiempo (s)", min_value=0.0, step=0.1, format="%.2f")
        payload = {"distancia": distancia, "tiempo": tiempo, "velocidad": None}
    else:
        distancia = col1.number_input("Distancia (m)", min_value=0.0, step=0.1, format="%.2f")
        velocidad = col2.number_input("Velocidad (m/s)", min_value=0.0, step=0.1, format="%.2f")
        payload = {"distancia": distancia, "velocidad": velocidad, "tiempo": None}

    enviar = st.form_submit_button("Calcular y guardar")

if enviar:
    if not nombre.strip():
        st.error("Debes escribir un nombre para el ensayo.")
        st.stop()

    try:
        response = requests.post(API_URL, params={"nombre": nombre.strip()}, json=payload, timeout=20)
        response.raise_for_status()
        resultado = response.json()
        detalle = resultado.get("detalle", {})

        st.success(f"Ensayo guardado con ID {resultado.get('id')}.")
        st.json(resultado)

        if detalle:
            st.subheader("Gráfica del movimiento")
            st.plotly_chart(construir_figura_mru({**detalle, "nombre": nombre.strip()}), use_container_width=True)

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Velocidad", f"{float(detalle.get('velocidad', 0)):.2f} m/s")
            col_b.metric("Tiempo", f"{float(detalle.get('tiempo', 0)):.2f} s")
            col_c.metric("Distancia", f"{float(detalle.get('distancia', 0)):.2f} m")
    except requests.RequestException as exc:
        st.error(f"No se pudo conectar con la API: {exc}")
    except Exception as exc:
        st.error(f"Error al guardar el ensayo: {exc}")