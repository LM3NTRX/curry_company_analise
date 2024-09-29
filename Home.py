import streamlit as st

st.set_page_config(
    page_title='Home',
    page_icon='Home'
)

with st.sidebar:
    #==================================
    #Inserindo lgotipo
    #==================================
    st.image(r'3.png')

st.markdown('# Growth')
st.markdown(
    """
    Growth Dashboard foi construido para acompanhar as métricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar esse DashBorad?
        - Visão Empresa:
            - Visão gerencial: Métricas  gerais de comportamento.
            - Visão tática: Indicadores semanais de crescimento.
            - Visão geográfica: Insigth de geolocalização.
        - Visão Entregador:
            - Acompanhamento dos indicadores semanais de crescimento.
        - Visão Restaurantes:
            - Indicadores semanais de crescimento dos restaurantes
    """
    )