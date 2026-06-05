"""Página MRUA de PhysiLab."""
# ruff: noqa: E402

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests
import plotly.express as px
import streamlit as st

from src.app.ui import apply_theme, get_experiments_url, render_hero, render_topbar

st.set_page_config(page_title="PhysiLab - MRUA", page_icon="🚀", layout="wide")
BACKEND_URL = get_experiments_url()

apply_theme()
render_topbar("MRUA")
render_hero(
    "Simulación de Movimiento Rectilíneo Uniformemente Acelerado",
    "Completa el formulario y deja que la API resuelva la incógnita con un gráfico dinámico de Plotly.",
    tag="Cinemática acelerada",
)

st.info(
    "Define la incógnita física y completa los datos conocidos para resolver el ensayo."
)

with st.form("form_mrua"):
    nombre = st.text_input("Identificador del Ensayo", value="Ensayo Acelerado Beta")
    c1, c2 = st.columns(2)
    with c1:
        x0 = st.number_input("Posición Inicial (m)", min_value=0.0, value=0.0)
        v0 = st.number_input("Velocidad Inicial (m/s)", min_value=0.0, value=4.0)
        aceleracion = st.number_input("Aceleración (m/s²)", min_value=0.0, value=2.0)
    with c2:
        xf = st.number_input(
            "Posición Final (m) [Dejar 0 si falta]", min_value=0.0, value=0.0
        )
        t = st.number_input("Tiempo (s) [Dejar 0 si falta]", min_value=0.0, value=0.0)

    enviar = st.form_submit_button("Ejecutar Análisis Cuadrático")

if enviar:
    payload = {
        "posicion_inicial": x0,
        "velocidad_inicial": v0,
        "aceleracion": aceleracion if aceleracion > 0 else None,
        "posicion_final": xf if xf > 0 else None,
        "tiempo": t if t > 0 else None,
    }

    try:
        res = requests.post(
            f"{BACKEND_URL}/calculate/mrua",
            params={"nombre": nombre},
            json=payload,
            timeout=20,
        )
        res.raise_for_status()
        if res.status_code == 201:
            data = res.json()
            st.success(f"Ensayo MRUA guardado con el ID {data['id']}.")

            det = data["detalle"]
            t_limite = float(det["tiempo"])
            posicion_final = float(det.get("posicion_final", 0))
            velocidad_final = float(det.get("velocidad_final", 0))
            aceleracion = float(det.get("aceleracion", 0))

            met1, met2, met3, met4 = st.columns(4)
            met1.metric("Posición final", f"{posicion_final:.2f} m")
            met2.metric("Velocidad final", f"{velocidad_final:.2f} m/s")
            met3.metric("Aceleración", f"{aceleracion:.2f} m/s²")
            met4.metric("Tiempo", f"{t_limite:.2f} s")

            pasos_tiempo = [i * (t_limite / 20) for i in range(21)]
            posiciones = [
                det["posicion_inicial"]
                + (det["velocidad_inicial"] * t)
                + (0.5 * det["aceleracion"] * (t**2))
                for t in pasos_tiempo
            ]

            fig = px.area(
                x=pasos_tiempo,
                y=posiciones,
                labels={"x": "Tiempo (s)", "y": "Desplazamiento Total (m)"},
                title="Curva de Comportamiento Dinámico (Ecuación de Segundo Grado)",
            )
            fig.update_traces(line_color="crimson")
            st.plotly_chart(fig, use_container_width=True)

            st.json(det)
        else:
            st.error(f"Fallo matemático: {res.json().get('detail')}")
    except Exception as e:
        st.error(f"Error en la llamada de red: {e}")
