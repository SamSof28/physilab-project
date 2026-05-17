import pandas as pd
import plotly.express as px
import requests
import streamlit as st


API_BASE = "http://localhost:8000/experiments"


def cargar_experimentos() -> list[dict]:
    response = requests.get(API_BASE, timeout=20)
    response.raise_for_status()
    return response.json()


def construir_resumen(experimentos: list[dict]) -> pd.DataFrame:
    if not experimentos:
        return pd.DataFrame(columns=["tipo", "cantidad"])
    return pd.DataFrame(experimentos).groupby("tipo", as_index=False).size().rename(columns={"size": "cantidad"})


def guardar_mru(nombre: str, variable_faltante: str, valores: dict[str, float]) -> None:
    if variable_faltante == "Distancia":
        payload = {"velocidad": valores["velocidad"], "tiempo": valores["tiempo"], "distancia": None}
    elif variable_faltante == "Velocidad":
        payload = {"distancia": valores["distancia"], "tiempo": valores["tiempo"], "velocidad": None}
    else:
        payload = {"distancia": valores["distancia"], "velocidad": valores["velocidad"], "tiempo": None}

    response = requests.post(f"{API_BASE}/calculate/mru", params={"nombre": nombre}, json=payload, timeout=20)
    response.raise_for_status()
    st.success(f"Ensayo MRU guardado con ID {response.json().get('id')}.")
    st.json(response.json())


def guardar_mrua(nombre: str, variable_faltante: str, valores: dict[str, float]) -> None:
    payload: dict[str, float | None] = {
        "posicion_inicial": valores["posicion_inicial"],
        "velocidad_inicial": valores["velocidad_inicial"],
        "posicion_final": None,
        "velocidad_final": None,
        "aceleracion": None,
        "tiempo": None,
    }

    if variable_faltante == "Aceleración":
        payload.update({
            "velocidad_final": valores["velocidad_final"],
            "tiempo": valores["tiempo"],
        })
    elif variable_faltante == "Posición final":
        payload.update({
            "aceleracion": valores["aceleracion"],
            "tiempo": valores["tiempo"],
        })
    elif variable_faltante == "Velocidad final":
        payload.update({
            "aceleracion": valores["aceleracion"],
            "tiempo": valores["tiempo"],
        })
    else:
        payload.update({
            "aceleracion": valores["aceleracion"],
            "posicion_final": valores["posicion_final"],
        })

    response = requests.post(f"{API_BASE}/calculate/mrua", params={"nombre": nombre}, json=payload, timeout=20)
    response.raise_for_status()
    st.success(f"Ensayo MRUA guardado con ID {response.json().get('id')}.")
    st.json(response.json())


st.set_page_config(page_title="Ensayos - PhysiLab", page_icon="🧪", layout="wide")

st.title("🧪 Ensayos")
st.caption("Registra experimentos y revisa un resumen rápido del historial.")

try:
    experimentos = cargar_experimentos()
except requests.RequestException as exc:
    st.warning(f"No se pudo cargar el historial: {exc}")
    experimentos = []

if experimentos:
    resumen = construir_resumen(experimentos)
    st.subheader("Resumen del historial")
    st.plotly_chart(
        px.bar(resumen, x="tipo", y="cantidad", color="tipo", title="Cantidad de ensayos por tipo"),
        use_container_width=True,
    )

    st.subheader("Últimos registros")
    st.dataframe(pd.DataFrame(experimentos).sort_values("fecha_creacion", ascending=False), use_container_width=True)

st.divider()

tab_mru, tab_mrua = st.tabs(["MRU", "MRUA"])

with tab_mru:
    st.subheader("Registrar ensayo MRU")
    with st.form("ensayo_mru_form"):
        nombre = st.text_input("Nombre del ensayo", placeholder="Ej: MRU de carrito")
        variable_faltante = st.radio("Variable a calcular", ["Distancia", "Velocidad", "Tiempo"], horizontal=True)
        col1, col2 = st.columns(2)

        valores: dict[str, float] = {}
        if variable_faltante == "Distancia":
            valores["velocidad"] = col1.number_input("Velocidad (m/s)", min_value=0.0, step=0.1, format="%.2f")
            valores["tiempo"] = col2.number_input("Tiempo (s)", min_value=0.0, step=0.1, format="%.2f")
        elif variable_faltante == "Velocidad":
            valores["distancia"] = col1.number_input("Distancia (m)", min_value=0.0, step=0.1, format="%.2f")
            valores["tiempo"] = col2.number_input("Tiempo (s)", min_value=0.0, step=0.1, format="%.2f")
        else:
            valores["distancia"] = col1.number_input("Distancia (m)", min_value=0.0, step=0.1, format="%.2f")
            valores["velocidad"] = col2.number_input("Velocidad (m/s)", min_value=0.0, step=0.1, format="%.2f")

        submit_mru = st.form_submit_button("Calcular y guardar MRU")

    if submit_mru:
        if not nombre.strip():
            st.error("Debes escribir un nombre para el ensayo.")
        else:
            try:
                guardar_mru(nombre.strip(), variable_faltante, valores)
            except requests.RequestException as exc:
                st.error(f"No se pudo guardar el MRU: {exc}")

with tab_mrua:
    st.subheader("Registrar ensayo MRUA")
    with st.form("ensayo_mrua_form"):
        nombre = st.text_input("Nombre del ensayo", placeholder="Ej: MRUA en rampa")
        variable_faltante = st.radio(
            "Variable a calcular",
            ["Aceleración", "Posición final", "Velocidad final", "Tiempo"],
            horizontal=True,
        )

        col1, col2 = st.columns(2)
        valores = {
            "posicion_inicial": col1.number_input("Posición inicial (m)", min_value=0.0, step=0.1, format="%.2f"),
            "velocidad_inicial": col2.number_input("Velocidad inicial (m/s)", min_value=0.0, step=0.1, format="%.2f"),
        }

        if variable_faltante == "Aceleración":
            col3, col4 = st.columns(2)
            valores["velocidad_final"] = col3.number_input("Velocidad final (m/s)", min_value=0.0, step=0.1, format="%.2f")
            valores["tiempo"] = col4.number_input("Tiempo (s)", min_value=0.0, step=0.1, format="%.2f")
        elif variable_faltante in {"Posición final", "Velocidad final"}:
            col3, col4 = st.columns(2)
            valores["aceleracion"] = col3.number_input("Aceleración (m/s²)", min_value=0.0, step=0.1, format="%.2f")
            valores["tiempo"] = col4.number_input("Tiempo (s)", min_value=0.0, step=0.1, format="%.2f")
        else:
            col3, col4 = st.columns(2)
            valores["aceleracion"] = col3.number_input("Aceleración (m/s²)", min_value=0.0, step=0.1, format="%.2f")
            valores["posicion_final"] = col4.number_input("Posición final (m)", min_value=0.0, step=0.1, format="%.2f")

        submit_mrua = st.form_submit_button("Calcular y guardar MRUA")

    if submit_mrua:
        if not nombre.strip():
            st.error("Debes escribir un nombre para el ensayo.")
        else:
            try:
                guardar_mrua(nombre.strip(), variable_faltante, valores)
            except requests.RequestException as exc:
                st.error(f"No se pudo guardar el MRUA: {exc}")