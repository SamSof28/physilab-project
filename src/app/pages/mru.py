import streamlit as st
import requests  # Esta librería es la que "habla" con FastAPI

st.title("🧪 Laboratorio de MRU")

with st.form("mru_form"):
    nombre = st.text_input("Nombre del ensayo", placeholder="Ej: Carrito de madera 01")
    
    col1, col2, col3 = st.columns(3)
    distancia = col1.number_input("Distancia (m)", min_value=0.0, value=None)
    velocidad = col2.number_input("Velocidad (m/s)", min_value=0.0, value=None)
    tiempo = col3.number_input("Tiempo (s)", min_value=0.0, value=None)
    
    enviar = st.form_submit_button("Calcular y Guardar")

if enviar:
    # 1. Empaquetamos los datos (JSON)
    payload = {
        "distancia": distancia,
        "velocidad": velocidad,
        "tiempo": tiempo
    }
    
    # 2. Llamamos a nuestra API (FastAPI)
    # Importante: El parámetro 'nombre' va en la URL porque así lo definimos en el Router
    api_url = f"http://localhost:8000/experiments/calculate/mru?nombre={nombre}"
    
    try:
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            resultado = response.json()
            st.success(f"✅ ¡Guardado! Experimento ID: {resultado['id']}")
            st.json(resultado["detalle"]) # Mostramos los cálculos finales
        else:
            st.error(f"❌ Error de la API: {response.json()['detail']}")
            
    except Exception as e:
        st.error(f"No se pudo conectar con el servidor: {e}")