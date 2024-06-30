# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Función para formatear números en formato CLP
def formatear_clp(numero):
    return f'${int(numero):,}'.replace(',', '.')

# Título de la aplicación
st.title('Calculadora de Libertad Financiera')

# Entrada de datos
st.sidebar.header('Parámetros de entrada')
currency = 'CLP'  # Establecer CLP como moneda por defecto

# Entrada del monto inicial
monto_inicial = st.sidebar.number_input(f'Monto inicial ({currency})', min_value=0.0, value=0.0, step=5000.0, format='%f')

# Entrada del aporte mensual
aporte_mensual = st.sidebar.number_input(f'Aporte mensual ({currency})', min_value=0.0, value=500.0, step=50.0, format='%f')

# Entrada de tasas de retorno e inflación
tasa_retorno_anual = st.sidebar.slider('Tasa de retorno anual (%)', min_value=0.0, max_value=20.0, value=7.0, step=0.1) / 100
tasa_inflacion_anual = st.sidebar.slider('Tasa de inflación anual (%)', min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100

# Entrada del monto objetivo
monto_objetivo = st.sidebar.number_input(f'Monto objetivo para la libertad financiera ({currency})', min_value=0.0, value=1000000.0, step=50000.0, format='%f')

# Simulación del crecimiento del capital
def calcular_libertad_financiera(monto_inicial, aporte_mensual, tasa_retorno_anual, tasa_inflacion_anual, monto_objetivo):
    # ... (código anterior)

# Mostrar resultados
st.subheader('Resultados')
st.write(f'Si aportas {formatear_clp(aporte_mensual)} {currency} mensualmente, comienzas con un monto inicial de {formatear_clp(monto_inicial)} {currency}, con una tasa de retorno anual del {tasa_retorno_anual*100:.2f}% y una tasa de inflación anual del {tasa_inflacion_anual*100:.2f}%, alcanzarás tu objetivo de libertad financiera de {formatear_clp(monto_objetivo)} {currency} en aproximadamente {años_necesarios} años (ajustado por inflación). 🎉')

# Graficar resultados
fig = go.Figure()
# ... (código anterior)

# Ajustar la visibilidad de las leyendas según el tamaño de la pantalla
if st.get_option('client.showWarnings'):
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
else:
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

# Usar use_container_width=True para hacer el gráfico responsive
st.plotly_chart(fig, use_container_width=True)

# Mostrar la probabilidad estimada de alcanzar la libertad financiera
st.subheader('Estimación de Probabilidad')
st.write(f'Teniendo en cuenta las tasas de retorno e inflación seleccionadas, la probabilidad estimada de alcanzar tu objetivo de libertad financiera en {años_necesarios} años es alta, asumiendo que las condiciones del mercado se mantienen constantes y que los aportes mensuales no cambian. 🎉')
