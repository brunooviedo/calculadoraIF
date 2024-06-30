# Graficar resultados
fig = go.Figure()
fig.add_trace(go.Scatter(x=años, y=capital, mode='lines', name='Capital acumulado (nominal)'))
fig.add_trace(go.Scatter(x=años, y=capital_inflacion, mode='lines', name='Capital acumulado (ajustado por inflación)'))
fig.add_hline(y=monto_objetivo, line_color='red', line_dash='dash', name='Objetivo de libertad financiera')

# Añadir anotación con icono de fiesta cuando se alcanza la libertad financiera
fig.add_annotation(x=años[años_necesarios-1], y=capital_inflacion[años_necesarios-1],
                   text="🎉", showarrow=True, arrowhead=2, ax=-30, ay=-30)

fig.update_layout(
    title={
        'text': 'Crecimiento del Capital',
        'y': 0.95,  # Ajustar la posición del título
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'pad': {'b': 20}  # Agregar padding inferior al título
    },
    xaxis_title='Años',
    yaxis_title=f'Monto ({currency})',
    margin=dict(l=50, r=50, t=100, b=50),  # Ajustar los márgenes
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor='rgba(255, 255, 255, 0.5)',  # Agregar fondo a la leyenda
        bordercolor='rgba(0, 0, 0, 0.2)',  # Agregar borde a la leyenda
        borderwidth=1,
        pad={'b': 10, 'l': 10, 'r': 10, 't': 10}  # Agregar padding a la leyenda
    )
)

# Usar use_container_width=True para hacer el gráfico responsive
st.plotly_chart(fig, use_container_width=True)
