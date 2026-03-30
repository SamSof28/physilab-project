import streamlit as st
import numpy as np
import plotly.express as px

x = np.linspace(0, 10, 400)
y = np.sin(x)


fig = px.line(x=x, 
              y =y, 
              labels={
                  'x': "x",
                  'y': "y"
              })

fig.update_traces(line_color='#00d1ff', line_width=3)

st.title("Función Sen(x)")
st.markdown(
    """
    # **$$\sin{x}$$**
    """
)
st.plotly_chart(fig)