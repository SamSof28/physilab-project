"""Página MRU de PhysiLab."""
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

st.set_page_config(page_title="PhysiLab - MRU", page_icon="📊", layout="wide")
BACKEND_URL = get_experiments_url()

apply_theme()
render_topbar("MRU")
render_hero(
    "Simulación de Movimiento Rectilíneo Uniforme",
    "Completa dos variables, calcula la faltante y visualiza el resultado en una curva limpia de Plotly.",
    tag="Cinemática básica",
)

st.info(
    "Deja en blanco o en 0.0 la magnitud específica que deseas calcular analíticamente."
)

with st.form("form_mru"):
    nombre = st.text_input("Identificador del Ensayo", value="Ensayo MRU General")
    c1, c2, c3 = st.columns(3)
    with c1:
        distancia = st.number_input("Distancia (m)", min_value=0.0, step=1.0, value=0.0)
    with c2:
        velocidad = st.number_input(
            "Velocidad (m/s)", min_value=0.0, step=1.0, value=5.0
        )
    with c3:
        tiempo = st.number_input("Tiempo (s)", min_value=0.0, step=1.0, value=2.0)

    # SOLUCIÓN AL CRASH: Cambiado a st.form_submit_button estándar
    enviar = st.form_submit_button("Calcular y Guardar en Laboratorio")

if enviar:
    payload = {
        "distancia": distancia if distancia > 0 else None,
        "velocidad": velocidad if velocidad > 0 else None,
        "tiempo": tiempo if tiempo > 0 else None,
    }

    try:
        res = requests.post(
            f"{BACKEND_URL}/calculate/mru",
            params={"nombre": nombre},
            json=payload,
            timeout=20,
        )
        res.raise_for_status()
        if res.status_code == 201:
            data = res.json()
            st.success(f"Ensayo MRU guardado con el ID {data['id']}.")

            detalle = data["detalle"]
            distancia = float(detalle.get("distancia", 0))
            velocidad = float(detalle.get("velocidad", 0))
            tiempo = float(detalle.get("tiempo", 0))

            met1, met2, met3 = st.columns(3)
            met1.metric("Distancia", f"{distancia:.2f} m")
            met2.metric("Velocidad", f"{velocidad:.2f} m/s")
            met3.metric("Tiempo", f"{tiempo:.2f} s")

            tiempos = [t * (tiempo / 10) for t in range(11)]
            posiciones = [velocidad * t for t in tiempos]

            fig = px.line(
                x=tiempos,
                y=posiciones,
                labels={"x": "Tiempo (segundos)", "y": "Posición (metros)"},
                title=f"Evolución Cinemática Temporal: {nombre}",
                markers=True,
            )
            fig.update_traces(line_color="teal", width=3)
            st.plotly_chart(fig, use_container_width=True)

            st.json(detalle)
        else:
            st.error(f"Error de validación física: {res.json().get('detail')}")
    except Exception:
        st.error("Fallo crítico: No se puede establecer comunicación con la API REST.")
