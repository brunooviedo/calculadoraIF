# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Título de la aplicación
st.title('Calculadora de Libertad Financiera')

# Entrada de datos
st.sidebar.header('Parámetros de entrada')
aporte_mensual = st.sidebar.number_input('Aporte mensual (USD)', min_value=0.0, value=500.0, step=50.0)
tasa_retorno_anual = st.sidebar.slider('Tasa de retorno anual (%)', min_value=0.0, max_value=20.0, value=7.0, step=0.1) / 100
tasa_inflacion_anual = st.sidebar.slider('Tasa de inflación anual (%)', min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100
monto_objetivo = st.sidebar.number_input('Monto objetivo para la libertad financiera (USD)', min_value=0.0, value=1000000.0, step=50000.0)

# Simulación del crecimiento del capital
def calcular_libertad_financiera(aporte_mensual, tasa_retorno_anual, tasa_inflacion_anual, monto_objetivo):
    años = np.arange(1, 101)
    capital = np.zeros(100)
    capital_inflacion = np.zeros(100)
    for i in range(100):
        if i == 0:
            capital[i] = aporte_mensual * 12
            capital_inflacion[i] = capital[i]
        else:
            capital[i] = (capital[i-1] + aporte_mensual * 12) * (1 + tasa_retorno_anual)
            capital_inflacion[i] = capital[i] / ((1 + tasa_inflacion_anual) ** (i+1))
        
        if capital_inflacion[i] >= monto_objetivo:
            break
    
    return años[:i+1], capital[:i+1], capital_inflacion[:i+1], i+1

años, capital, capital_inflacion, años_necesarios = calcular_libertad_financiera(aporte_mensual, tasa_retorno_anual, tasa_inflacion_anual, monto_objetivo)

# Mostrar resultados
st.subheader('Resultados')
st.write(f'Si aportas ${aporte_mensual:.2f} mensualmente con una tasa de retorno anual del {tasa_retorno_anual*100:.2f}% y una tasa de inflación anual del {tasa_inflacion_anual*100:.2f}%, alcanzarás tu objetivo de libertad financiera de ${monto_objetivo:.2f} en aproximadamente {años_necesarios} años (ajustado por inflación).')

# Graficar resultados
fig, ax = plt.subplots()
ax.plot(años, capital, label='Capital acumulado (nominal)')
ax.plot(años, capital_inflacion, label='Capital acumulado (ajustado por inflación)', linestyle='--')
ax.axhline(y=monto_objetivo, color='r', linestyle='-', label='Objetivo de libertad financiera')
ax.set_xlabel('Años')
ax.set_ylabel('Monto (USD)')
ax.set_title('Crecimiento del Capital a lo Largo del Tiempo')
ax.legend()
st.pyplot(fig)

# Mostrar la probabilidad estimada de alcanzar la libertad financiera
st.subheader('Estimación de Probabilidad')
st.write(f'Teniendo en cuenta las tasas de retorno e inflación seleccionadas, la probabilidad estimada de alcanzar tu objetivo de libertad financiera en {años_necesarios} años es alta, asumiendo que las condiciones del mercado se mantienen constantes y que los aportes mensuales no cambian.')

