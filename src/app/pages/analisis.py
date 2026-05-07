import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Agregar ruta del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from mi_app.storage import JsonStorage
from mi_app.models import (
    MovimientoRectilineoUniformementeAcelerado,
    MovimientoRectilineoUniforme,
)

# Configuración de página
st.set_page_config(
    page_title="Análisis de Ensayos - PhysiLab",
    page_icon="📊",
    layout="wide",
)


# ===== Funciones de utilidad =====
def cargar_ensayos():
    """Carga todos los ensayos desde storage."""
    ruta_db = Path(__file__).parent.parent.parent.parent / "data" / "database.json"
    storage = JsonStorage(ruta_db)
    return storage.cargar()


def obtener_nombre_completo_ensayo(ensayo):
    """Genera un nombre completo para mostrar en selectores."""
    return f"{ensayo.nombre} ({ensayo.tipo}) - {ensayo.fecha}"


def generar_grafica_mrua(ensayo: MovimientoRectilineoUniformementeAcelerado):
    """Genera gráficas para un ensayo MRUA."""
    # Vector de tiempo
    t = np.linspace(0, ensayo.tiempo, 100)
    
    # Calcular posiciones: x = x0 + v0*t + 0.5*a*t^2
    x = (
        ensayo.posicion_inicial
        + ensayo.velocidad_inicial * t
        + 0.5 * ensayo.aceleracion * t**2
    )
    
    # Calcular velocidades: v = v0 + a*t
    v = ensayo.velocidad_inicial + ensayo.aceleracion * t
    
    # Aceleración constante
    a = np.full_like(t, ensayo.aceleracion)
    
    # DataFrame para Plotly
    df_plot = pd.DataFrame({
        "Tiempo (s)": t,
        "Posición (m)": x,
        "Velocidad (m/s)": v,
        "Aceleración (m/s²)": a,
    })
    
    return df_plot


def generar_grafica_mru(ensayo: MovimientoRectilineoUniforme):
    """Genera gráficas para un ensayo MRU."""
    # Vector de tiempo
    t = np.linspace(0, ensayo.tiempo, 100)
    
    # Calcular posiciones: x = v*t
    x = ensayo.velocidad * t
    
    # Velocidad constante
    v = np.full_like(t, ensayo.velocidad)
    
    # Aceleración nula
    a = np.zeros_like(t)
    
    # DataFrame para Plotly
    df_plot = pd.DataFrame({
        "Tiempo (s)": t,
        "Posición (m)": x,
        "Velocidad (m/s)": v,
        "Aceleración (m/s²)": a,
    })
    
    return df_plot


def crear_figura_posicion(df_plot, nombre_ensayo):
    """Crea gráfica de posición vs tiempo."""
    fig = px.line(
        df_plot,
        x="Tiempo (s)",
        y="Posición (m)",
        title=f"Posición vs Tiempo - {nombre_ensayo}",
    )
    fig.update_traces(line_color="#00d1ff", line_width=3)
    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def crear_figura_velocidad(df_plot, nombre_ensayo):
    """Crea gráfica de velocidad vs tiempo."""
    fig = px.line(
        df_plot,
        x="Tiempo (s)",
        y="Velocidad (m/s)",
        title=f"Velocidad vs Tiempo - {nombre_ensayo}",
    )
    fig.update_traces(line_color="#ff006e", line_width=3)
    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def crear_figura_aceleracion(df_plot, nombre_ensayo):
    """Crea gráfica de aceleración vs tiempo."""
    fig = px.line(
        df_plot,
        x="Tiempo (s)",
        y="Aceleración (m/s²)",
        title=f"Aceleración vs Tiempo - {nombre_ensayo}",
    )
    fig.update_traces(line_color="#ffbe0b", line_width=3)
    fig.update_layout(
        hovermode="x unified",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    return fig


def crear_figura_comparativa(df1, df2, nombre1, nombre2, variable):
    """Crea una gráfica comparativa entre dos ensayos."""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df1["Tiempo (s)"],
        y=df1[variable],
        mode="lines",
        name=nombre1,
        line=dict(color="#00d1ff", width=3),
    ))
    
    fig.add_trace(go.Scatter(
        x=df2["Tiempo (s)"],
        y=df2[variable],
        mode="lines",
        name=nombre2,
        line=dict(color="#ff006e", width=3),
    ))
    
    fig.update_layout(
        title=f"Comparación: {variable}",
        xaxis_title="Tiempo (s)",
        yaxis_title=variable,
        hovermode="x unified",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0.1)",
    )
    
    return fig


def mostrar_ecuaciones_mrua(ensayo: MovimientoRectilineoUniformementeAcelerado):
    """Muestra las ecuaciones específicas del MRUA."""
    st.subheader("📐 Ecuaciones de Movimiento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Posición en función del tiempo:**")
        st.latex(
            f"x(t) = {ensayo.posicion_inicial} + {ensayo.velocidad_inicial}t + "
            f"\\frac{{1}}{{2}}({ensayo.aceleracion})t^2"
        )
    
    with col2:
        st.markdown("**Velocidad en función del tiempo:**")
        st.latex(f"v(t) = {ensayo.velocidad_inicial} + ({ensayo.aceleracion})t")
    
    # Posición y velocidad finales
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**Posición Final:**")
        st.latex(
            f"x_f = {ensayo.posicion_inicial} + {ensayo.velocidad_inicial}"
            f"({ensayo.tiempo}) + \\frac{{1}}{{2}}({ensayo.aceleracion})"
            f"({ensayo.tiempo})^2 = {ensayo.posicion_final:.2f} \\text{{ m}}"
        )
    
    with col4:
        st.markdown("**Velocidad Final:**")
        st.latex(
            f"v_f = {ensayo.velocidad_inicial} + {ensayo.aceleracion}"
            f"({ensayo.tiempo}) = {ensayo.velocidad_final:.2f} \\text{{ m/s}}"
        )


def mostrar_ecuaciones_mru(ensayo: MovimientoRectilineoUniforme):
    """Muestra las ecuaciones específicas del MRU."""
    st.subheader("📐 Ecuaciones de Movimiento")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Posición en función del tiempo:**")
        st.latex(f"x(t) = {ensayo.velocidad}t")
    
    with col2:
        st.markdown("**Velocidad (constante):**")
        st.latex(f"v = {ensayo.velocidad} \\text{{ m/s}}")
    
    with col3:
        st.markdown("**Aceleración:**")
        st.latex(f"a = 0 \\text{{ m/s}}^2")
    
    # Distancia recorrida
    st.markdown("**Distancia recorrida:**")
    st.latex(
        f"d = v \\times t = {ensayo.velocidad} \\times {ensayo.tiempo} = "
        f"{ensayo.distancia:.2f} \\text{{ m}}"
    )


def mostrar_metricas_mrua(ensayo: MovimientoRectilineoUniformementeAcelerado):
    """Muestra métricas estadísticas para MRUA."""
    st.subheader("📊 Resumen Estadístico")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Velocidad Inicial", f"{ensayo.velocidad_inicial:.2f} m/s")
    col2.metric("Velocidad Final", f"{ensayo.velocidad_final:.2f} m/s")
    col3.metric("Aceleración", f"{ensayo.aceleracion:.2f} m/s²")
    col4.metric("Tiempo Total", f"{ensayo.tiempo:.2f} s")
    
    col5, col6, col7, col8 = st.columns(4)
    
    col5.metric("Posición Inicial", f"{ensayo.posicion_inicial:.2f} m")
    col6.metric("Posición Final", f"{ensayo.posicion_final:.2f} m")
    distancia = ensayo.posicion_final - ensayo.posicion_inicial
    col7.metric("Distancia Recorrida", f"{distancia:.2f} m")
    velocidad_promedio = (ensayo.velocidad_inicial + ensayo.velocidad_final) / 2
    col8.metric("Velocidad Promedio", f"{velocidad_promedio:.2f} m/s")


def mostrar_metricas_mru(ensayo: MovimientoRectilineoUniforme):
    """Muestra métricas estadísticas para MRU."""
    st.subheader("📊 Resumen Estadístico")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Velocidad", f"{ensayo.velocidad:.2f} m/s")
    col2.metric("Distancia", f"{ensayo.distancia:.2f} m")
    col3.metric("Tiempo Total", f"{ensayo.tiempo:.2f} s")
    col4.metric("Aceleración", "0 m/s²")


# ===== INTERFAZ PRINCIPAL =====
st.title("📊 Análisis de Ensayos - PhysiLab")

# Cargar ensayos
ensayos = cargar_ensayos()

if not ensayos:
    st.warning("⚠️ No hay ensayos disponibles. Crea algunos ensayos primero desde la página de Ensayos.")
    st.stop()

# ===== SIDEBAR: Controles =====
st.sidebar.header("🎛️ Controles")

# Selector de ensayo único
st.sidebar.subheader("Análisis Individual")
opciones_ensayos = [obtener_nombre_completo_ensayo(e) for e in ensayos]
indice_seleccionado = st.sidebar.selectbox(
    "Selecciona un ensayo:",
    range(len(ensayos)),
    format_func=lambda i: opciones_ensayos[i],
)

ensayo_seleccionado = ensayos[indice_seleccionado]

# ===== CONTENIDO PRINCIPAL =====
st.header(f"Ensayo: {ensayo_seleccionado.nombre}")
st.caption(f"Tipo: {ensayo_seleccionado.tipo} | Fecha: {ensayo_seleccionado.fecha}")

# Generar datos para gráficas
if isinstance(ensayo_seleccionado, MovimientoRectilineoUniformementeAcelerado):
    df_plot = generar_grafica_mrua(ensayo_seleccionado)
    mostrar_metricas_mrua(ensayo_seleccionado)
    
    # Gráficas individuales
    st.subheader("📈 Gráficas de Movimiento")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pos = crear_figura_posicion(df_plot, ensayo_seleccionado.nombre)
        st.plotly_chart(fig_pos, use_container_width=True)
    
    with col2:
        fig_vel = crear_figura_velocidad(df_plot, ensayo_seleccionado.nombre)
        st.plotly_chart(fig_vel, use_container_width=True)
    
    st.plotly_chart(
        crear_figura_aceleracion(df_plot, ensayo_seleccionado.nombre),
        use_container_width=True,
    )
    
    # Ecuaciones
    mostrar_ecuaciones_mrua(ensayo_seleccionado)

else:  # MRU
    df_plot = generar_grafica_mru(ensayo_seleccionado)
    mostrar_metricas_mru(ensayo_seleccionado)
    
    # Gráficas individuales
    st.subheader("📈 Gráficas de Movimiento")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pos = crear_figura_posicion(df_plot, ensayo_seleccionado.nombre)
        st.plotly_chart(fig_pos, use_container_width=True)
    
    with col2:
        fig_vel = crear_figura_velocidad(df_plot, ensayo_seleccionado.nombre)
        st.plotly_chart(fig_vel, use_container_width=True)
    
    # Ecuaciones
    mostrar_ecuaciones_mru(ensayo_seleccionado)


# ===== COMPARACIÓN ENTRE ENSAYOS =====
st.divider()
st.header("🔄 Comparación de Ensayos")

col1, col2 = st.columns(2)

with col1:
    indice_ensayo1 = st.selectbox(
        "Primer ensayo:",
        range(len(ensayos)),
        format_func=lambda i: opciones_ensayos[i],
        key="ensayo_comp_1"
    )

with col2:
    indice_ensayo2 = st.selectbox(
        "Segundo ensayo:",
        range(len(ensayos)),
        format_func=lambda i: opciones_ensayos[i],
        key="ensayo_comp_2",
        index=1 if len(ensayos) > 1 else 0,
    )

if indice_ensayo1 != indice_ensayo2:
    ensayo1 = ensayos[indice_ensayo1]
    ensayo2 = ensayos[indice_ensayo2]
    
    # Generar datos
    if isinstance(ensayo1, MovimientoRectilineoUniformementeAcelerado):
        df1 = generar_grafica_mrua(ensayo1)
    else:
        df1 = generar_grafica_mru(ensayo1)
    
    if isinstance(ensayo2, MovimientoRectilineoUniformementeAcelerado):
        df2 = generar_grafica_mrua(ensayo2)
    else:
        df2 = generar_grafica_mru(ensayo2)
    
    # Mostrar gráficas comparativas
    col1, col2 = st.columns(2)
    
    with col1:
        fig_comp_pos = crear_figura_comparativa(df1, df2, ensayo1.nombre, ensayo2.nombre, "Posición (m)")
        st.plotly_chart(fig_comp_pos, use_container_width=True)
    
    with col2:
        fig_comp_vel = crear_figura_comparativa(df1, df2, ensayo1.nombre, ensayo2.nombre, "Velocidad (m/s)")
        st.plotly_chart(fig_comp_vel, use_container_width=True)
    
    # Análisis comparativo
    st.subheader("📋 Análisis Comparativo")
    
    col1, col2, col3 = st.columns(3)
    
    # Ensayo 1
    with col1:
        st.markdown(f"**{ensayo1.nombre}**")
        if isinstance(ensayo1, MovimientoRectilineoUniformementeAcelerado):
            st.write(f"Velocidad inicial: {ensayo1.velocidad_inicial:.2f} m/s")
            st.write(f"Velocidad final: {ensayo1.velocidad_final:.2f} m/s")
            st.write(f"Aceleración: {ensayo1.aceleracion:.2f} m/s²")
            st.write(f"Distancia: {ensayo1.posicion_final - ensayo1.posicion_inicial:.2f} m")
        else:
            st.write(f"Velocidad: {ensayo1.velocidad:.2f} m/s")
            st.write(f"Distancia: {ensayo1.distancia:.2f} m")
            st.write(f"Tiempo: {ensayo1.tiempo:.2f} s")
    
    with col2:
        st.markdown("**Comparación**")
        
        # Tiempos
        if hasattr(ensayo1, 'tiempo') and hasattr(ensayo2, 'tiempo'):
            diferencia_tiempo = ensayo2.tiempo - ensayo1.tiempo
            st.write(f"Diferencia de tiempo: {diferencia_tiempo:.2f} s")
        
        # Distancias
        if isinstance(ensayo1, MovimientoRectilineoUniformementeAcelerado):
            dist1 = ensayo1.posicion_final - ensayo1.posicion_inicial
        else:
            dist1 = ensayo1.distancia
        
        if isinstance(ensayo2, MovimientoRectilineoUniformementeAcelerado):
            dist2 = ensayo2.posicion_final - ensayo2.posicion_inicial
        else:
            dist2 = ensayo2.distancia
        
        diferencia_distancia = dist2 - dist1
        st.write(f"Diferencia de distancia: {diferencia_distancia:.2f} m")
    
    # Ensayo 2
    with col3:
        st.markdown(f"**{ensayo2.nombre}**")
        if isinstance(ensayo2, MovimientoRectilineoUniformementeAcelerado):
            st.write(f"Velocidad inicial: {ensayo2.velocidad_inicial:.2f} m/s")
            st.write(f"Velocidad final: {ensayo2.velocidad_final:.2f} m/s")
            st.write(f"Aceleración: {ensayo2.aceleracion:.2f} m/s²")
            st.write(f"Distancia: {ensayo2.posicion_final - ensayo2.posicion_inicial:.2f} m")
        else:
            st.write(f"Velocidad: {ensayo2.velocidad:.2f} m/s")
            st.write(f"Distancia: {ensayo2.distancia:.2f} m")
            st.write(f"Tiempo: {ensayo2.tiempo:.2f} s")

else:
    st.info("ℹ️ Selecciona dos ensayos diferentes para hacer una comparación.")