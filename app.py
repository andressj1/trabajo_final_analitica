# Cargar datos
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64

# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")

# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #951F0F;'>Analisis de mortalidad en U.S.A💀; suicidio,sobredosis, y covid.  </h1>", unsafe_allow_html=True)
#----------------------------------------
df0 = pd.read_csv('covid.csv', sep=";")
df1 = pd.read_csv('drogas.csv', sep=";") 
df1 = df1.drop(['PANEL','PANEL_NUM'], axis=1)
df2 = pd.read_csv('suicidio.csv' , sep=";") 
df = pd.concat([df1,df2])

# Función para descargar base de datos
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

# Función para descargar base de datos
def get_table_download_link(df0):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

#----------------------------------------

#Depuracion
lista = df[df['AGE'] == 'All ages'].index 
df3 = df.drop(lista) # Aplicar filtro
df3['AGE'] = df3['AGE'].replace(['15-24 years','Under 15 years','10-14 years','15-19 years','20-24 years'], '0-24')
df3['AGE'] = df3['AGE'].replace(['25-34 years','35-44 years','25-44 years'], '25-44')
df3['AGE'] = df3['AGE'].replace(['45-64 years','45-54 years','55-64 years'], '45-64')
df3['AGE'] = df3['AGE'].replace(['65 years and over','65-74 years','75-84 years'], '65-84')

lista1 = df0[df0['Age Group'] == 'All Ages'].index 
dfa = df0.drop(lista1) # Aplicar filtro

lista2 = dfa[dfa['Age Group'] == 'Not stated'].index 
dff = dfa.drop(lista2) # Aplicar filtro

dff['Age Group'] = dff['Age Group'].replace(['25-34','35-44'], '25-44')
dff['Age Group'] = dff['Age Group'].replace(['45-54','55-64'], '45-64')
dff['Age Group'] = dff['Age Group'].replace(['65-74','75-84'], '65-84')




#-------------------------

c1, c2 ,c3  = st.columns((1,1,1))
                                
#--------------- Top edad

c1.markdown("<h3 style='text-align: left; color: while;'> Top Edad </h3>", unsafe_allow_html=True)

#st.write(df3['AGE'].value_counts())
top_perp_name = (df3['AGE'].value_counts().index[1])
top_perp_num = (round(df3['AGE'].value_counts()/df3['AGE'].value_counts().sum(),2)*100)[1]
top_cov_name = (dff['Age Group'].value_counts().index[1])
top_cov_num = (round(dff['Age Group'].value_counts()/dff['Age Group'].value_counts().sum(),2)*100)[1]

c1.text('Intervalo de edad: '+str(top_perp_name)+', '+str(top_perp_num)+'%')
c1.text('Intervalo de edad;covid: '+str(top_cov_name)+', '+str(top_cov_num)+'%')


################ Top tasa
                            
c2.markdown("<h3 style='text-align: left; color: while;'> Top mayor indice </h3>", unsafe_allow_html=True)


#st.write(df3['ESTIMATE'].value_counts())
top_perp_name = (df3['ESTIMATE'].max())
top_cov_name = (dff['COVID-19 Deaths'].max())

#st.write(dff['COVID-19 Deaths'].max())

c2.text('Tasa: '+str(top_perp_name))
c2.text('Muertes;covid: '+str(top_cov_name))

#--------------- Top edad

c3.markdown("<h3 style='text-align: left; color: while;'> Top Año </h3>", unsafe_allow_html=True)

top_perp_name = 2018
top_perp_num  = 253
top_cov_name  = 2021
top_cov_num  = 7008764 

c3.text('Año: '+str(top_perp_name)+', '+str(top_perp_num))
c3.text('Año;covid: '+str(top_cov_name)+', '+str(top_cov_num))


                  
# Título de la siguiente sección

st.markdown("<h3 style='text-align: center; color: while;'> ¿Cómo ha sido la evolución de la mortalidad por edad? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
dfs = df3.groupby(['YEAR','AGE'])[['ESTIMATE']].count().reset_index().rename(columns = {'ESTIMATE':'ESTIMADO'})

# Generar gráfica
fig = px.line(dfs, x='YEAR', y='ESTIMADO', color = 'AGE', width=1350, height=450)

# Editar gráfica
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Año<b>",
        yaxis_title='<b>Estimado<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.7))

st.plotly_chart(fig)

#-------------------------------------------------

# Título de la siguiente sección
st.markdown("<h3 style='text-align: center; color: while;'> ¿Cómo ha sido la evolución de la mortalidad por edad; COVID-19? </h3>", unsafe_allow_html=True)

# Organizar DataFrame
dfq = dff.groupby(['Year','Age Group'])[['COVID-19 Deaths']].count().reset_index().rename(columns = {'COVID-19 Deaths':'muertes'})

# Generar gráfica
fig1 = px.line(dfq, x='Year', y='muertes', color = 'Age Group', width=1400, height=450)

# Editar gráfica
fig1.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Año<b>",
        yaxis_title='<b>muertes<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.7))

# Enviar gráfica a streamlit
st.plotly_chart(fig1)

#----------------------------------------------------

c1, c2 = st.columns((1,1))

# c1
c1.markdown("<h3 style='text-align: center; color: while;'> ¿Que intervalo de edad aumento mas la tasa de mortalidad? </h3>", unsafe_allow_html=True)


# Hacer gráfica
fig = px.pie(dfs, values = 'ESTIMADO', names="AGE",
             width=370, height=370)
fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gráfica a streamlit
c1.plotly_chart(fig)

# c2
c2.markdown("<h3 style='text-align: center; color: while;'> ¿Que intervalo de edad aumento mas la tasa de mortalidad; covid? </h3>", unsafe_allow_html=True)


# Hacer gráfica
fig = px.pie(dff, values = 'COVID-19 Deaths', names="Age Group",
             width=370, height=370)
fig.update_layout(template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  legend=dict(orientation="h",
                              yanchor="bottom",
                              y=-0.4,
                              xanchor="center",
                              x=0.5))

# Enviar gráfica a streamlit
c2.plotly_chart(fig)




#--------------------------------------------------
c3, c4= st.columns((1,1))

c3.markdown("<h3 style='text-align: center; color: while;'> ¿En que año aumento mas la mortalidad? </h3>", unsafe_allow_html=True)

dfp = dfs.groupby(['YEAR'])[['ESTIMADO']].sum().reset_index()

dfp= dfp.sort_values('YEAR',ascending = False)

# Hacer gráfica
fig = px.bar(dfp, x="ESTIMADO", y="YEAR", orientation='h', width=450,  height=650)
fig.update_layout(xaxis_title="<b>Muertes<b>",
                  yaxis_title="<b>Año<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gráfica a streamlit
c3.plotly_chart(fig)


#---------------------------------------------------

c4.markdown("<h3 style='text-align: center; color: while;'> ¿En que año aumento mas la mortalidad; covid-19? </h3>", unsafe_allow_html=True)

dfk = dff.groupby(['Year'])[['COVID-19 Deaths']].sum().reset_index()

dfk= dfk.sort_values('Year',ascending = False)

# Hacer gráfica
fig = px.bar(dfk, x="COVID-19 Deaths", y="Year", orientation='h', width=370,  height=370)
fig.update_layout(xaxis_title="<b>Muertes<b>",
                  yaxis_title="<b>Año<b>", template = 'simple_white',
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)')

# Enviar gráfica a streamlit
c4.plotly_chart(fig)

#------------------------------------------------------

st.markdown("<h3 style='text-align: center; color: while;'> Evolución de la mortalidad por el intervalo de edad que más la aumenta </h3>", unsafe_allow_html=True)

# Organizar DataFrame
dft = dfs[dfs['AGE'].isin(['45-64'])].groupby(['YEAR','AGE'])[['ESTIMADO']].sum().sort_values('ESTIMADO', ascending = False).reset_index() 
dft['AGE'] = dft['AGE'].astype('category')

### graficar
fig = px.bar(dft, x='YEAR', y='ESTIMADO', color ='AGE', barmode='group', width=1650, height=450)
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text = '<b>edad<b>',
        xaxis_title="<b>Año<b>",
        yaxis_title="<b>Muertes<b>")

# Enviar gráfica a streamlit
st.plotly_chart(fig)

#------------------------------------------------------

st.markdown("<h3 style='text-align: center; color: while;'> Evolución de la mortalidad por el intervalo de edad que más la aumenta; covid-19 </h3>", unsafe_allow_html=True)

# Organizar DataFrame
dfg = dff[dff['Age Group'].isin(['65-84'])].groupby(['Year','Age Group'])[['COVID-19 Deaths']].sum().sort_values('COVID-19 Deaths', ascending = False).reset_index() 
dfg['Age Group'] = dfg['Age Group'].astype('category')

### graficar
fig = px.bar(dfg, x='Year', y='COVID-19 Deaths', color ='Age Group', barmode='group', width=1200, height=450)
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        legend_title_text = '<b>edad<b>',
        xaxis_title="<b>Año<b>",
        yaxis_title="<b>Muertes<b>")

# Enviar gráfica a streamlit
st.plotly_chart(fig)

#---------------------------------------------------------

# Hacer un checkbox
if st.checkbox('Obtener datos por año y edad', False):
    
    # Código para generar el DataFrame
    dfi = df3.groupby(['YEAR','AGE'])[['ESTIMATE']].count().reset_index().rename(columns ={'YEAR':'AÑO','AGE':'EDAD','ESTIMATE':'CANTIDAD'})
    
    # Código para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(dfi.columns),
        fill_color='blue',
        line_color='darkslategray'),
        cells=dict(values=[dfi.AÑO, dfi.EDAD, dfi.CANTIDAD],fill_color='black',line_color='lightgrey'))
       ])
    fig.update_layout(width=500, height=450)

# Enviar tabla a streamlit
    st.write(fig)
    
# Generar link de descarga
    st.markdown(get_table_download_link(dfi), unsafe_allow_html=True)

# Hacer un checkbox
if st.checkbox('Obtener datos por año y edad;covid', False):
    
    # Código para generar el DataFrame
    dfb = dff.groupby(['Year','Age Group'])[['COVID-19 Deaths']].count().reset_index().rename(columns ={'Year':'AÑO','Age Group':'EDAD','COVID-19 Deaths':'CANTIDAD'})
    
    # Código para convertir el DataFrame en una tabla plotly resumen
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(dfi.columns),
        fill_color='blue',
        line_color='darkslategray'),
        cells=dict(values=[dfb.AÑO, dfb.EDAD, dfb.CANTIDAD],fill_color='black',line_color='lightgrey'))
       ])
    fig.update_layout(width=500, height=450)

# Enviar tabla a streamlit
    st.write(fig)
    
# Generar link de descarga
    st.markdown(get_table_download_link(dfb), unsafe_allow_html=True)

