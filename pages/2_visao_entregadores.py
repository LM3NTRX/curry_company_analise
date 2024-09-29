
import pandas as pd 
import streamlit as st
import utils as ut

st.set_page_config(layout= 'wide', page_title='Visão Entregadores')
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
    #==================================
    #filtro para datas
    #==================================  
    selec_lines = df1['Order_Date'] < pd.to_datetime(ut.filter_date())
    df1=df1.loc[selec_lines,:]
    df1=df1.loc[df1['Road_traffic_density'].isin(ut.filter_traffic()),:]
#==================================
#Layout page
#==================================

#Criando o conteiner para alocar as informações
with st.container():
    
    st.title('Visão Geral entregadores')    
    st.markdown("""___""")       

    #inicializando as colunas
    c, c1, c2, c3 = st.columns(4, gap='small') 
    with c:
        #filtrando o dataframe pela idade dos entregadores e pegando o menor valor
        yang=df1['Delivery_person_Age'].min()
        st.metric(label="##### Idade do entregador mais novo", value=f"{yang:.0f}")
    with c1:
        #filtrando o dataframe pela idade dos entregadores e pegando o maior valor
        older=df1['Delivery_person_Age'].max()
        st.metric('##### Idade do entregador mais velho',value=f'{older:.0f}')
    with c2:
        #filtrando o dataframe pela condição veicular dos entregadores e pegando o maior valor
        better_condicao_veiculo = df1.loc[:,'Vehicle_condition'].astype(int).max()
        st.metric('##### Melhor condição de veicular  ',value=f'{better_condicao_veiculo}')
    with c3:
        #filtrando o dataframe pela condição veicular dos entregadores e pegando o menor valor
        worst_vehicle_conditions = df1.loc[:,'Vehicle_condition'].astype(int).min()
        st.metric('##### Pior condição veicular',value=f'{worst_vehicle_conditions}')
    st.markdown("""___""")
    with st.container():
        
        c4,c5=st.columns(2)
        with c4:
            st.markdown('##### Avaliação média por entregador:')
            st.dataframe(df1.loc[:,['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index(), use_container_width=True)
        with c5:
            st.markdown('##### Avaliação média por tipo de tráfego:')
            st.dataframe(df1.loc[:,['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').mean().reset_index(), use_container_width=True)
            with st.container():
                st.markdown('##### Avaliação média por tipo de clima:')
                st.dataframe(df1.loc[:,['Weatherconditions','Delivery_person_Ratings']].groupby('Weatherconditions').mean().reset_index(), use_container_width=True)
    st.markdown("""___""")
    with st.container():
        c6, c7 = st.columns(2)
        with c6:
            st.markdown('##### Top 10 entregadores mais rapidos:')
            st.dataframe(df1.loc[:,['Time_taken(min)','Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index().sort_values(by= 'Time_taken(min)',ascending=True).head(9))
        with c7:
            st.markdown('##### Top 10 entregadores mais lentos:')
            st.dataframe(df1.loc[:,['Time_taken(min)','Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index().sort_values(by= 'Time_taken(min)',ascending=False).head(9))