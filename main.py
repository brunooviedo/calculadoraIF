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

# Entrada de la edad actual
edad_actual = st.sidebar.number_input('Edad actual', min_value=0, max_value=100, value=30, step=1)

# Entrada del sexo (para considerar la esperanza de vida)
sexo = st.sidebar.radio('Sexo', ['Hombre', 'Mujer'])

# Definir la esperanza de vida según el sexo
if sexo == 'Hombre':
    esperanza_vida = 80
else:
    esperanza_vida = 85

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
def calcular_libertad_financiera(monto_inicial, aporte_mensual, tasa_retorno_anual, tasa_inflacion_anual, monto_objetivo, esperanza_vida, edad_actual):
    años = np.arange(0, min(100, esperanza_vida - edad_actual + 1))  # Limitar hasta 100 años o la esperanza de vida desde la edad actual
    capital = np.zeros(len(años))
    capital_inflacion = np.zeros(len(años))
    
    for i in range(len(años)):
        if i == 0:
            capital[i] = monto_inicial + aporte_mensual * 12
            capital_inflacion[i] = capital[i]
        else:
            capital[i] = (capital[i-1] + aporte_mensual * 12) * (1 + tasa_retorno_anual)
            capital_inflacion[i] = capital[i] / ((1 + tasa_inflacion_anual) ** (i+1))
        
        if capital_inflacion[i] >= monto_objetivo:
            # Ajustar los arrays para detener el crecimiento una vez alcanzado el objetivo
            años = años[:i+1]
            capital = capital[:i+1]
            capital_inflacion = capital_inflacion[:i+1]
            break
    
    años_necesarios = i + 1
    
    # Calcular edad alcanzada
    edad_alcanzada = edad_actual + años[-1]
    
    # Definir el mensaje de acuerdo a los años restantes
    años_restantes_vida = esperanza_vida - edad_alcanzada
    if años_restantes_vida > 0:
        mensaje_vida = f"Tendrías aproximadamente <b>{años_restantes_vida:.1f} años</b> de vida esperados restantes una vez alcanzada la Libertad Financiera 🎉💰💸"
    else:
        mensaje_vida = f"Probablemente no alcances a disfrutar la libertad financiera, ya que estarías muerto 💀⚰️, debido a la esperanza de vida de {esperanza_vida} años en los {sexo.lower()}."
    
    return años, capital, capital_inflacion, años_necesarios, edad_alcanzada, mensaje_vida

# Llamar a la función para obtener los datos de simulación
años, capital, capital_inflacion, años_necesarios, edad_alcanzada, mensaje_vida = calcular_libertad_financiera(monto_inicial, aporte_mensual, tasa_retorno_anual, tasa_inflacion_anual, monto_objetivo, esperanza_vida, edad_actual)

# Mostrar resultados
st.subheader('Resultados')
st.markdown(f"""
    <p>Si aportas <b>{formatear_clp(aporte_mensual)} {currency}</b> mensualmente,
    y comienzas con un monto inicial de <b>{formatear_clp(monto_inicial)} {currency}</b>,
    con una tasa de retorno anual del <b>{tasa_retorno_anual*100:.2f}%</b> y una tasa de inflación anual del <b>{tasa_inflacion_anual*100:.2f}%</b>,
    alcanzarás tu objetivo de libertad financiera de <b>{formatear_clp(monto_objetivo)} {currency}</b> en aproximadamente <b>{años_necesarios} años</b> (ajustado por inflación).
    Para ese momento, tendrás <b>{edad_alcanzada} años</b>.
    {mensaje_vida}</p>
""", unsafe_allow_html=True)

# Graficar resultados
fig = go.Figure()
fig.add_trace(go.Scatter(x=años + edad_actual, y=capital, mode='lines', name='Capital acumulado (nominal)'))
fig.add_trace(go.Scatter(x=años + edad_actual, y=capital_inflacion, mode='lines', name='Capital acumulado (ajustado por inflación)'))
fig.add_hline(y=monto_objetivo, line_color='red', line_dash='dash', name='Objetivo de libertad financiera')

# Añadir anotación con icono de fiesta cuando se alcanza la libertad financiera
fig.add_annotation(x=edad_actual + años[-1], y=capital_inflacion[años_necesarios-1],
                   text="🎉💰", showarrow=True, arrowhead=2, ax=-30, ay=-30)

# Ajustar el layout del gráfico incluyendo padding y margin para la leyenda y el título
fig.update_layout(
    title='Crecimiento del Capital',
    title_x=0.5,
    title_y=0.9,
    title_xanchor='center',
    title_yanchor='top',
    title_font=dict(size=15, family='Arial'),
    xaxis_title='Edad',
    yaxis_title=f'Monto ({currency})',
    margin=dict(l=80, r=50, t=100, b=100),  # Ajustar los márgenes
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,  # Ajustar esta posición para centrar verticalmente la leyenda
        xanchor="center",
        x=0.5,  # Ajustar esta posición para centrar horizontalmente la leyenda
        font=dict(size=10),  # Disminuir el tamaño de la fuente
        bgcolor='rgba(255, 255, 255, 0.5)',
        bordercolor='Black',
        borderwidth=1
    ),
    xaxis=dict(
        range=[0, 100]  # Limitar el eje x desde 0 hasta 100 años
    )
)

# Usar use_container_width=True para hacer el gráfico responsive
st.plotly_chart(fig, use_container_width=True)

# Calcular la probabilidad estimada de alcanzar la libertad financiera
edad_alcanzada = edad_actual + años_necesarios
años_restantes_vida = esperanza_vida - edad_alcanzada

if años_restantes_vida > 0:
    probabilidad_alcanzar = 100
    mensaje_probabilidad = f"Tienes una alta probabilidad de alcanzar tu objetivo de libertad financiera. Tendrías aproximadamente {años_restantes_vida:.1f} años de vida esperados restantes una vez alcanzada la Libertad Financiera 🎉💰💸"
else:
    probabilidad_alcanzar = 0
    mensaje_probabilidad = f"Probablemente no alcances a disfrutar la libertad financiera, ya que estarías muerto 💀⚰️, debido a la esperanza de vida de {esperanza_vida} años en los {sexo.lower()}."

# Mostrar la probabilidad estimada de alcanzar la libertad financiera
st.subheader('Estimación de Probabilidad')
st.markdown(f"""
    <p>Teniendo en cuenta las tasas de retorno e inflación seleccionadas,
    la probabilidad estimada de alcanzar tu objetivo de libertad financiera en <b>{años_necesarios} años</b> es del <b>{probabilidad_alcanzar:.1f}%</b>.
    {mensaje_probabilidad}</p>
""", unsafe_allow_html=True)


# Incluir CSS y JavaScript para ajustar la leyenda en dispositivos móviles
st.markdown("""
<style>
@media only screen and (max-width: 600px) {
    .plotly-graph-div .legend {
        transform: translateY(20px) !important;
        position: relative !important;
        padding: 10px !important;
        margin: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Sección para retroalimentación de usuarios
st.sidebar.header('Retroalimentación')
feedback = st.sidebar.text_area('¿Qué te gustaría mejorar en la aplicación?')

if st.sidebar.button('Enviar Retroalimentación'):
    # Aquí puedes agregar código para procesar el feedback, como enviarlo por correo electrónico o guardarlo en una base de datos
    st.sidebar.success('¡Gracias por tu retroalimentación!')
