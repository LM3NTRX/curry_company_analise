import pandas as pd 
import plotly.express as px
import streamlit as st
from streamlit_folium import st_folium
import utils as ut

#==================================
#page config
#==================================
st.set_page_config(page_title='Visão Negócios', layout= 'wide')
#==================================
#Carregando e limpando o FataFrame
#==================================
df = pd.read_csv(r'train.csv')
df1 = df.copy()
ut.clean_df(df1)
#==================================
#Side bar
#==================================
with st.sidebar:
    #==================================
    #Inserindo lgotipo
    #==================================
    st.image(r'3.png')
    st.markdown("""___""")
    #==================================
    #colocando filtros para os dashboards
    #==================================
    selec_lines = df1['Order_Date'] < pd.to_datetime(ut.filter_date())
    df1=df1.loc[selec_lines,:]
    df1=df1.loc[df1['Road_traffic_density'].isin(ut.filter_traffic()),:]
#==================================
#Layout page
#==================================
#st.image(r'C:\Users\Felipe\Documents\repos\img\3.png', use_column_width= True)

with st.container():
    tab, tab1, tab2 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geografica'])
    with tab:

        st.markdown('## Quantidade de pedidos por dia:')
        entregas_dia = px.bar(df1.loc[:,['ID','Order_Date']].groupby('Order_Date').count().reset_index(), x='Order_Date', y='ID')
        st.plotly_chart(entregas_dia, use_container_width= True)
        st.markdown("""___""")

        col, col1 = st.columns(2, gap='small', vertical_alignment='top')
        with col:
            st.markdown('### Distribuição de pedidos por tipo de tráfego')
            #configurando as linhas para criação do gráfico de pizza
            df_aux = df1.loc[:,['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
            df_aux['percentual'] = df_aux['ID'] / df_aux['ID'].sum()
            #Desenhando o gráfico de linha
            st.plotly_chart(px.pie(df_aux, values= 'percentual', names= 'Road_traffic_density'), use_container_width= True)
    
        st.markdown("""___""")

        with col1:
            st.markdown('### Comparação do volume de pedidos por cidade e tipo de tráfego')
            df_aux1=df1.loc[:,['ID', 'Road_traffic_density', 'City']].groupby(['City', 'Road_traffic_density']).count()
            st.plotly_chart(px.scatter(df_aux1.reset_index(), x='City', y='Road_traffic_density', size= 'ID'))  


    with tab1:
        st.markdown('## Quantidade de pedidos por entregador por semana')
        #plotando o gráfico de linhas
        st.plotly_chart(px.line(ut.draw_chart_delivery_week(df1), y= 'order_by_delivery', x='week_of_year'))
        st.markdown("""___""")

        st.markdown('## Quantidade de pedidos por semana')
        st.plotly_chart(px.line(df1.loc[:,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index(), x='week_of_year', y='ID'))


    with tab2:
        st.markdown('## Localização central de cada cidade por tráfego')
        #colocando o gráfico na tela
        st_folium(ut.draw_chart_location(df1), use_container_width=True)