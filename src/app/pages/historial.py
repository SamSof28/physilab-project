from pathlib import Path
import sys

# 1. Asegurar resolución de rutas en el Layout SRC
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from src.app.ui import render_topbar, render_hero, get_api_base_url

st.set_page_config(
    page_title="PhysiLab - Historial de Ensayos",
    page_icon="🗄️",
    layout="wide"
)

# Renderizar la barra lateral personalizada con el contexto correcto
render_topbar("Historial")

render_hero(
    "Historial de experimentos",
    "Explora cada registro, abre el análisis completo, edita el nombre o elimina un experimento desde la base de datos.",
    tag="Persistencia y control"
)

API_URL = f"{get_api_base_url()}/experiments"

if "analizar_id" not in st.session_state:
    st.session_state.analizar_id = None

# --- CAPA DE CONSUMO DEL API MAESTRO ---
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        experimentos = response.json()
    else:
        st.error(f"Error al obtener experimentos del backend: {response.status_code}")
        experimentos = []
except Exception as e:
    st.error(f"El servidor backend no responde: {e}")
    experimentos = []

# --- 1. SECCIÓN: GRÁFICO RESUMEN DE CONTROL ---
if experimentos:
    df_resumen = pd.DataFrame(experimentos)
    conteo_tipos = df_resumen["tipo"].value_counts().reset_index()
    conteo_tipos.columns = ["tipo", "cantidad"]
    
    fig_barra = px.bar(
        conteo_tipos, 
        x="tipo", 
        y="cantidad", 
        color="tipo",
        labels={"tipo": "Tipo de Experimento", "cantidad": "Cantidad"},
        color_discrete_map={"MRU": "#7ec4cf", "MRUA": "#4f6dd7"}
    )
    fig_barra.update_layout(height=280, showlegend=False)
    st.plotly_chart(fig_barra, use_container_width=True)
else:
    st.info("No hay experimentos registrados en la base de datos aún.")

st.markdown("---")

# --- 2. SECCIÓN: LISTADO MAESTRO ---
for exp in experimentos:
    exp_id = exp["id"]
    tipo = exp["tipo"]
    nombre_actual = exp["nombre"]

    with st.container(border=True):
        col_id, col_tipo, col_nombre, col_acciones = st.columns([1, 1, 4, 3])
        
        with col_id:
            st.markdown(f"**ID {exp_id}**")
        
        with col_tipo:
            st.caption(f"`{tipo}`")
        
        with col_nombre:
            nuevo_nombre = st.text_input(
                "Nombre", 
                value=nombre_actual, 
                key=f"name_{exp_id}", 
                label_visibility="collapsed"
            )
            
        with col_acciones:
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            with btn_col1:
                if st.button("Ver análisis", key=f"view_{exp_id}", type="primary"):
                    st.session_state.analizar_id = exp_id
            
            with btn_col2:
                if st.button("Guardar", key=f"save_{exp_id}"):
                    if nuevo_nombre != nombre_actual:
                        try:
                            put_res = requests.put(f"{API_URL}/{exp_id}?nuevo_nombre={nuevo_nombre}")
                            if put_res.status_code == 200:
                                st.toast(f"¡Experimento {exp_id} actualizado!", icon="✅")
                                st.rerun()
                        except Exception as err:
                            st.error(f"Error de red: {err}")
            
            with btn_col3:
                if st.button("🗑️", key=f"del_{exp_id}"):
                    try:
                        del_res = requests.delete(f"{API_URL}/{exp_id}")
                        if del_res.status_code == 200:
                            st.toast(f"Experimento {exp_id} eliminado.", icon="🗑️")
                            if st.session_state.analizar_id == exp_id:
                                st.session_state.analizar_id = None
                            st.rerun()
                    except Exception as err:
                        st.error(f"Error de red: {err}")

        # --- 3. SOLUCCIÓN AL ERROR: CONSULTAR EL DETALLE ON-DEMAND ---
        if st.session_state.analizar_id == exp_id:
            st.markdown("#### 📈 Desglose Cinemático del Experimento")
            
            # Hacemos la petición al endpoint de detalle individual que SÍ trae los datos físicos
            try:
                detail_response = requests.get(f"{API_URL}/{exp_id}")
                if detail_response.status_code == 200:
                    experimento_completo = detail_response.json()
                    detalle = experimento_completo.get("detalle", {})
                else:
                    detalle = {}
            except Exception as e:
                st.error(f"No se pudieron cargar los detalles desde el servidor: {e}")
                detalle = {}

            if not detalle:
                st.warning("No se encontraron variables numéricas para este ensayo en las tablas de física.")
            else:
                try:
                    # Extraer parámetros mapeando los nombres exactos de tus columnas de Supabase
                    posicion_inicial = float(detalle.get("posicion_inicial", detalle.get("posicion_origen", 0.0)))
                    tiempo_total = float(detalle.get("tiempo", detalle.get("tiempo_total", 5.0)))
                    velocidad_inicial = float(detalle.get("velocidad_inicial", detalle.get("velocidad", 0.0)))
                    aceleracion = float(detalle.get("aceleracion", 0.0)) if tipo == "MRUA" else 0.0
                    
                    # Generar los puntos para la gráfica con las leyes de la física
                    pasos_tiempo = [i * (tiempo_total / 20) for i in range(21)]
                    datos_grafico = []
                    
                    for t in pasos_tiempo:
                        if tipo == "MRU":
                            x = posicion_inicial + velocidad_inicial * t
                            v = velocidad_inicial
                        else:
                            x = posicion_inicial + velocidad_inicial * t + 0.5 * aceleracion * (t ** 2)
                            v = velocidad_inicial + aceleracion * t
                            
                        datos_grafico.append({"Tiempo (s)": t, "Posición (m)": x, "Velocidad (m/s)": v})
                    
                    df_dinamico = pd.DataFrame(datos_grafico)
                    
                    # Gráfica de Plotly
                    fig_analisis = px.line(
                        df_dinamico, 
                        x="Tiempo (s)", 
                        y="Posición (m)", 
                        title=f"Evolución de Posición vs Tiempo: {nombre_actual}",
                        markers=True
                    )
                    fig_analisis.update_traces(line_color="#4f6dd7" if tipo == "MRUA" else "#7ec4cf")
                    
                    # Mostrar Tarjetas de Métricas
                    met_col1, met_col2, met_col3 = st.columns(3)
                    with met_col1:
                        st.metric("Posición Inicial ($x_0$)", f"{posicion_inicial} m")
                    with met_col2:
                        st.metric("Velocidad Inicial ($v_0$)", f"{velocidad_inicial} m/s")
                    with met_col3:
                        if tipo == "MRUA":
                            st.metric("Aceleración ($a$)", f"{aceleracion} $m/s^2$")
                        else:
                            st.metric("Movimiento", "Velocidad Constante")
                            
                    st.plotly_chart(fig_analisis, use_container_width=True)
                    
                except Exception as eval_err:
                    st.error(f"Error al procesar las variables físicas del diccionario: {eval_err}")