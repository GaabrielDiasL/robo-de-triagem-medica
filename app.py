import streamlit as st
from agent import DoctorAgent
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(page_title='Robo de Triagem Médica', layout='wide')

# Inicializa a chave da API
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.warning("Chave da API OpenAI não definida. Por favor, insira a chave abaixo.")
    openai_api_key = st.text_input("Chave da API OpenAI", type="password")
    if st.button("Salvar Chave"):
        with open('.env', 'a') as f:
            f.write(f"\nOPENAI_API_KEY={openai_api_key}")
        st.success("Chave da API salva! Por favor, recarregue a página.")
else:
    # Inicializa o agente
    agent = DoctorAgent(open_ai_api_key=openai_api_key)

    # Cabeçalho
    st.title('🩺 Robo de Triagem Médica')
    st.write("""
        Este projeto ajuda a população a identificar possíveis doenças com base em sintomas informados. 
        Preencha os sintomas que você está sentindo para obter uma triagem preliminar.
    """)

    # Layout com coluna para entrada de dados e coluna para resultados
    col1, col2 = st.columns([2, 3])

    with col1:
        st.header('Informações de Sintomas')
        request = st.text_area('Digite os sintomas que você está sentindo:', height=200, placeholder="Ex: dor de cabeça, febre, tosse...")
        button = st.button('Enviar', key='submit_button')

    with col2:
        st.header('Resumo da Triagem')
        if button:
            if request:
                with st.spinner('Processando...'):
                    triagem = agent.get_triagem(request)
                    try:
                        st.markdown(triagem['agent_suggestion'])
                    except KeyError:
                        st.warning('Não foi possível identificar a doença com base nos sintomas informados.')
            else:
                st.error('Por favor, insira os sintomas antes de enviar.')

    # Adicione uma seção de FAQ ou ajuda na barra lateral
    with st.sidebar:
        st.header('Ajuda e Informações')
        st.markdown("""
            ### Como usar
            - Insira os sintomas na caixa de texto à esquerda.
            - Clique em "Enviar" para obter uma triagem.
            - Os resultados serão exibidos na seção à direita.

            ### Sobre
            Este é um projeto de triagem médica em desenvolvimento. Não substitui o diagnóstico de um profissional de saúde.
        """)
