import pandas as pd 
import plotly.express as px
import streamlit as st
import utils as ut

st.set_page_config(layout= 'wide', page_title='Visão Restaurantes')
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
    #colocando filtros para os dashboards
    selec_lines = df1['Order_Date'] < pd.to_datetime(ut.filter_date())
    df1=df1.loc[selec_lines,:]
    df1=df1.loc[df1['Road_traffic_density'].isin(ut.filter_traffic()),:]

#==================================
#Layout page
#==================================
st.title('Visão Restaurante')

#Criando o conteiner para alocar as informações
with st.container():
    #inicializando as colunas
    c,c1,c2,c3,c4,c5 = st.columns(6)

    with c:
        st.markdown('##### Entregadores únicos')
        st.text(f'{ut.count_value_unique(df1, 'Delivery_person_ID')}')

    with c1:
        st.markdown('##### Distância média')
        x=df1.loc[:,'distance'].mean()
        st.text(f'{x:.2f}km')

    with c2:
        st.markdown('##### Tempo médio de entrega c/ festival')
        st.text(f'{ut.avg_time_festival(df1, True)} min')

    with c3:
        st.markdown('##### Tempo médio de entrega s/ festival')
        st.text(f'{ut.avg_time_festival(df1)} min')

    with c4:
        st.markdown('##### Desvio padrão médio de entrega c/ festival')
        st.text(f'{ut.std_time_festival(df1, True)}')

    with c5:
        st.markdown('##### Desvio padrão médio de entrega s/ festival')
        st.text(f'{ut.std_time_festival(df1)}')
    st.markdown("""___""")

#Criando o conteiner para alocar as informações gráficas e datafremes
with st.container():
    st.markdown('#### Distribuição de distância média por cidade')
    st.plotly_chart(px.pie(ut.avg_distance(df1), values='distance', names= 'City'))
    st.markdown("""___""")

#Criando o conteiner para alocar as informações
with st.container():

    c6,c7 = st.columns(2)

    with c6:
        st.markdown('#### Distribuaição do tempo por cidade')
        st.plotly_chart(ut.draw_graph_distribution_time_city(df1))

    with c7:
        st.markdown('#### Tempo médio por tipo de entrega')
        st.dataframe(df1.loc[:,['Time_taken(min)','Type_of_order','City']].groupby(['City','Type_of_order']).mean().reset_index())
    st.markdown("""___""")

with st.container():
    st.markdown('#### Tempo médio por cidade e tipo de tráfego')
    st.plotly_chart(ut.draw_graph_distribution_city_traffic(df1))