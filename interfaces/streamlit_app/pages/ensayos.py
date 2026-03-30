import streamlit as st

from pathlib import Path
from src.mi_app.services import LaboratoryService
from src.mi_app.storage import JsonStorage
from src.mi_app.models.mru import MovimientoRectilineoUniforme

path_data = Path("data/database.json")
storage = JsonStorage(path_data)
service = LaboratoryService(storage=storage)

st.title("🧪 Nuevo Ensayo de Cinemática")
st.write("Configura y registra un nuevo experimento en el laboratorio.")

tab_mru, tab_mrua = st.tabs(["MRU (Velocidad Constante)", "MRUA (Acelerado)"])

with tab_mru:
    st.subheader("Configuración de MRU")
    
    with st.container(border=True):
        id_ensayo = st.number_input("ID único del Ensayo", min_value=1, step=1, value=1)
        nombre_ensayo = st.text_input("Nombre descriptivo", value="MRU_01")
        
        col1, col2, col3 = st.columns(3)
        # st.number_input permite poner LaTeX en el label
        distancia = col1.number_input("Distancia $$ (m) $$", value=None)
        velocidad = col2.number_input("Velocidad $$ (m/s) $$", value=None)
        tiempo = col3.number_input("Tiempo $$ (s) $$", value=None)

        # 3. Llamar al backend al hacer click
        if st.button("Calcular y Guardar MRU"):
            try:
                # Instanciamos el modelo con los datos del frontend
                ensayo = MovimientoRectilineoUniforme(
                    id=id_ensayo, 
                    nombre=nombre_ensayo, 
                    tipo="Movimiento Rectilineo Uniforme",
                    distancia=distancia if distancia != 0 else None,
                    velocidad=velocidad if velocidad != 0 else None,
                    tiempo=tiempo if tiempo != 0 else None
                )
                
                resultado = service.calcular_mru(ensayo)
                
                # 4. Notificar
                st.success(f"✅ Ensayo '{resultado.nombre}' guardado con éxito. Distancia calculada: {resultado.distancia} m.")
            except Exception as e:
                st.error(f"❌ Error al guardar el ensayo: {e}")