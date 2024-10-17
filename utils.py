import folium
import pandas as pd
import numpy as np
from haversine import haversine
from datetime import datetime
import plotly.express as px
from streamlit_folium import st_folium
import plotly.graph_objects as go
import streamlit as st

def filter_date():
    #==================================
    #filtro para datas
    #==================================  
    slider_date = st.slider(
        'Selecione a data:',        
        min_value=datetime(2022,2,12),
        max_value=datetime(2022,4,6),
        value= datetime(2022,4,5),
        format = 'DD-MM-YYYY')
    
    st.markdown(slider_date)
    st.markdown("""___""")
    return slider_date

def filter_traffic():
    #==================================
    #filtros para desidade de trafego
    #==================================
    slider_traffic = st.multiselect(
        'Selcione o tipo de trafego:',
        options= ['Low','Medium','High','Jam'],
        default= ['Low','Medium','High','Jam']
    )
    return slider_traffic

def clean_df(df1: pd.DataFrame):
    df1.replace('NaN ', np.nan, inplace= True)
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Delivery_person_Age'] = df1.loc[:, 'Delivery_person_Age'].astype(float)
    df1.loc[:, 'Delivery_person_Ratings'] = df1.loc[:, 'Delivery_person_Ratings'].astype(float)
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.replace('(min) ','')).astype(int)
    df1['distance'] = (df1.loc[:, ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude','Delivery_location_longitude']]
                        .apply(lambda x: haversine((x['Restaurant_latitude'], x['Restaurant_longitude']),
                                                    (x['Delivery_location_latitude'],x['Delivery_location_longitude'])),
                                                    axis=1))
    df1.dropna(axis=1)
    return df1

def count_value_unique(df1: pd.DataFrame, col: str):
    return df1[col].nunique()


def avg_time_festival(df1: pd.DataFrame, festival: bool = None ) -> str:
    if festival:
       return f'{df1.loc[df1['Festival']=='Yes', ['Time_taken(min)']].mean().reset_index().iloc[0,1]:.2f}'
    return f'{df1.loc[df1['Festival']=='No', ['Time_taken(min)']].mean().reset_index().iloc[0,1]:.2f}'

def std_time_festival(df1: pd.DataFrame, festival: bool = None) -> str:
    if festival:
        return f'{df1.loc[df1['Festival']=='Yes', ['Time_taken(min)']].std().reset_index().iloc[0,1]:.2f}'
    return f'{df1.loc[df1['Festival']=='No', ['Time_taken(min)']].std().reset_index().iloc[0,1]:.2f}'

def avg_distance(df1: pd.DataFrame):
    aux =df1.loc[:,['distance', 'City']].groupby('City').mean().reset_index()
    return aux


def draw_graph_distribution_time_city(df1):
        aux = df1.loc[:,['Time_taken(min)','City']].groupby('City').agg(['mean','std'])
        aux.columns = ['avg_time', 'std_time']
        aux= aux.reset_index()
        fig = go.Figure()
        fig.add_trace(
            go.Bar(name= 'Control', x= aux['City'], y= aux['avg_time'], error_y= dict(type = 'data', array= aux['std_time']))
        )
        fig.update_layout(barmode='group')
        return fig

def draw_graph_distribution_city_traffic(df1):
    aux1 = df1.loc[:,['City','Road_traffic_density','Time_taken(min)']].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)':['mean','std']})
    aux1.columns = ['avg_time', 'std_time']
    aux1 = aux1.reset_index()

    sun = px.sunburst(
        aux1,
        path=['City', 'Road_traffic_density'],
        values='avg_time',
        color='std_time',
        color_continuous_scale='RdBu',
        color_continuous_midpoint=np.average(aux1['std_time'])
    )
    return sun

def draw_chart_delivery_week(df1):
            #Filtrnado as colunas semana do ano e ID, e agrupando por semana
        aux = df1.loc[:, ['week_of_year', 'ID']].groupby('week_of_year').count().reset_index()
        #Filtrando as colunas semanas do ano e idendificação do entregador, e agrupando por semana
        aux1 = df1.loc[:,['week_of_year', 'Delivery_person_ID']].groupby('week_of_year').nunique().reset_index()
        #Juntando os 2 dataframes em apenas um
        df2 = pd.merge(aux, aux1, how='inner')
        #Criando a coluna 'ordem por entregador' realizando a conta da quantidade de entregas(ID) dividido pela quantidade de entregadores cadastrados
        df2['order_by_delivery'] = df2['ID']/df2['Delivery_person_ID']
        return df2

def draw_chart_location(df1):
        #Filtrando e agrupando o Dataframe por Cidade, tipo de tráfego e localização de entrega
        mapa = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index()
        #Inicializando o mapa com o construtor vazio, folium.Map()
        mapa1 = folium.Map()
        #Percorrendo cada linha das colunas de longitude / latitude e adicionando um marcador no mapa utilizando a função lambda       
        mapa.apply( lambda marker: folium.Marker(location= [marker['Delivery_location_latitude'], marker['Delivery_location_longitude']]).add_to(mapa1), axis =1)
        return mapa1
