import streamlit as st
import requests

# Configuración de página con estética profesional
st.set_page_config(
    page_title="PhysiLab - Laboratorio Virtual",
    page_icon="🧪",
    layout="wide"
)

BACKEND_URL = "http://localhost:8000/experiments"

st.title("🧪 PhysiLab: Plataforma de Simulación Cinemática")
st.markdown("---")

# Estructuración por pestañas para cumplir con "Navegación Clara"
tab1, tab2, tab3 = st.tabs(["📊 Simulación MRU", "🚀 Simulación MRUA", "🗄️ Historial de Ensayos"])

# ==============================================================================
# VISTA 1: MOVIMIENTO RECTILÍNEO UNIFORME (MRU)
# ==============================================================================
with tab1:
    st.header("Movimiento Rectilíneo Uniforme")
    st.info("💡 Deja en blanco (o en 0.0) exactamente la variable que deseas calcular.")
    
    with st.form("form_mru"):
        nombre_mru = st.text_input("Nombre del Ensayo", value="Ensayo MRU Alpha")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            distancia = st.number_input("Distancia (m)", min_value=0.0, step=1.0, value=0.0)
        with col2:
            velocidad = st.number_input("Velocidad (m/s)", min_value=0.0, step=1.0, value=5.0)
        with col3:
            tiempo = st.number_input("Tiempo (s)", min_value=0.0, step=1.0, value=2.0)
            
        btn_mru = st.form_submit_button("Calcular MRU")
        
    if btn_mru:
        # Preparación de contrato de datos para enviar a la API
        payload = {
            "distancia": distancia if distancia > 0 else None,
            "velocidad": velocidad if velocidad > 0 else None,
            "tiempo": tiempo if tiempo > 0 else None
        }
        
        with st.spinner("Procesando ecuaciones físicas..."):
            try:
                res = requests.post(f"{BACKEND_URL}/calculate/mru", params={"nombre": nombre_mru}, json=payload)
                if res.status_code == 201:
                    data = res.json()
                    st.success(f"🎉 ¡Cálculo Exitoso! Guardado con ID: {data['id']}")
                    st.json(data["detalle"])
                else:
                    st.error(f"Error en la simulación: {res.json().get('detail')}")
            except Exception:
                st.error("No se pudo conectar con el servidor de la API Backend.")

# ==============================================================================
# VISTA 2: MOVIMIENTO RECTILÍNEO UNIFORMEMENTE ACELERADO (MRUA)
# ==============================================================================
with tab2:
    st.header("Movimiento Rectilíneo Uniformemente Acelerado")
    
    with st.form("form_mrua"):
        nombre_mrua = st.text_input("Nombre del Ensayo", value="Ensayo MRUA Beta")
        
        col1, col2 = st.columns(2)
        with col1:
            x0 = st.number_input("Posición Inicial (m)", min_value=0.0, value=0.0)
            v0 = st.number_input("Velocidad Inicial (m/s)", min_value=0.0, value=10.0)
            aceleracion = st.number_input("Aceleración (m/s²)", min_value=0.0, value=2.0)
        with col2:
            xf = st.number_input("Posición Final (m) [Opcional]", min_value=0.0, value=0.0)
            vf = st.number_input("Velocidad Final (m/s) [Opcional]", min_value=0.0, value=0.0)
            t = st.number_input("Tiempo (s) [Opcional]", min_value=0.0, value=0.0)
            
        btn_mrua = st.form_submit_button("Calcular MRUA")
        
    if btn_mrua:
        payload_mrua = {
            "posicion_inicial": x0,
            "velocidad_inicial": v0,
            "aceleracion": aceleracion if aceleracion > 0 else None,
            "posicion_final": xf if xf > 0 else None,
            "velocidad_final": vf if vf > 0 else None,
            "tiempo": t if t > 0 else None
        }
        with st.spinner("Calculando matrices de movimiento..."):
            try:
                res = requests.post(f"{BACKEND_URL}/calculate/mrua", params={"nombre": nombre_mrua}, json=payload_mrua)
                if res.status_code == 201:
                    data = res.json()
                    st.success(f"🎉 ¡Cálculo Exitoso! Guardado con ID: {data['id']}")
                    st.json(data["detalle"])
                else:
                    st.error(f"Error físico: {res.json().get('detail')}")
            except Exception:
                st.error("Error al establecer comunicación con el Backend.")

# ==============================================================================
# VISTA 3: HISTORIAL, ACTUALIZACIÓN Y BORRADO (CRUD COMPLETO)
# ==============================================================================
with tab3:
    st.header("Historial de Ensayos Registrados")
    
    try:
        response = requests.get(BACKEND_URL)
        if response.status_code == 200:
            lista_experimentos = response.json()
            
            if not lista_experimentos:
                st.info("No hay experimentos en la base de datos de Supabase.")
            else:
                for exp in lista_experimentos:
                    # Crear una tarjeta estética para cada elemento
                    with st.container(border=True):
                        c1, c2, c3, c4 = st.columns([1, 4, 3, 2])
                        with c1:
                            st.markdown(f"**ID: {exp['id']}**")
                        with c2:
                            st.markdown(f"🔬 **{exp['nombre']}** *(Tipo: {exp['tipo']})*")
                        with c3:
                            # Formulario integrado para actualización de nombre
                            nuevo_nombre = st.text_input("Editar nombre", value=exp['nombre'], key=f"edit_{exp['id']}")
                            if nuevo_nombre != exp['nombre']:
                                if st.button("💾 Guardar", key=f"btn_edit_{exp['id']}"):
                                    res_up = requests.put(f"{BACKEND_URL}/{exp['id']}", params={"nuevo_nombre": nuevo_nombre})
                                    if res_up.status_code == 200:
                                        st.rerun()
                        with c4:
                            # Botón de eliminación definitiva
                            if st.button("🗑️ Eliminar", key=f"del_{exp['id']}", type="primary"):
                                res_del = requests.delete(f"{BACKEND_URL}/{exp['id']}")
                                if res_del.status_code == 200:
                                    st.success("Eliminado")
                                    st.rerun()
        else:
            st.error("Error al obtener el listado del servidor.")
    except Exception:
        st.error("Conexión con el backend no disponible.")