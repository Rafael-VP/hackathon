import streamlit as st
import os
import configparser
import speech_recognition as sr
from pydub import AudioSegment
from openai import OpenAI
from modules.pdf import create_pdf
import PyPDF2

########################

import streamlit as st
import pandas as pd
from bd import iniciar_conexao, fechar_conexao, listar_equipamentos, inserir_ordem, inserir_ordem_equipamento, listar_tecnicos
from datetime import datetime
import plotly.express as px  # Importação do Plotly Express

##########################


def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":prompt}
        ]
    )

    return response.choices[0].message.content


st.set_page_config(
    page_title="Tractian",
    page_icon="data/tractian.jpg",  # You can replace with a favicon path or emoji
    #initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        border: 5px inset #0468f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px; /* Added space between elements */
        display: flex; /* Use flexbox for layout */
        justify-content: center; /* Center items horizontally */
        align-items: center; /* Center items vertically */
    }
    .logo {
        margin-right: 20px; /* Space between logo and title */
    }
    .stFileUploader {
        background-color: #282434;
        border: 5px inset #0468f6;
        border-radius: 10px;
        padding: 10px;
        margin-top: 20px; /* Added space between elements */
    }
    .stFileUploader p {
        color: #0468f6;
    }
    .css-1d391kg {  /* The title class */
        text-align: center;
        color: #0468f6;
    }
    </style>
    <div class="main">
        <img class="logo" src="https://yt3.googleusercontent.com/RcyFXjXXaec7Bc_PS8pUtmlrJP28XxqeSBp0oGHLjEE9bHhYxiYr_FeDVQSOmg4G3L3uET0B6ao=s900-c-k-c0x00ffffff-no-rj" alt="Logo" style="width:100px;height:auto;">
        <div class="css-1d391kg">
            <h1>Hackathon Tractian 2024</h1>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>-> MAINTENANCE COMPANION <-</h1>", unsafe_allow_html=True)


config = configparser.ConfigParser()
config.read("config.ini")

r = sr.Recognizer()

client = OpenAI(api_key=config['Main']['gpt_key'])
prepend = "Resuma o seguinte texto em uma lista de tarefas:\n "

uploaded_files = st.file_uploader("Arquivos de áudio:", type=['ogg'], accept_multiple_files=True)


pressed = 0
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Salvando arquivo ogg
        path = os.path.join("userdata", uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())

        # Convertendo arquivo para WAV
        audio = AudioSegment.from_ogg(path)
        path = path.replace("ogg", "wav")
        audio.export(path, format="wav")

        # Convertendo áudio para texto
        file_audio = sr.AudioFile(path)

        with file_audio as source:
            audio_text = r.record(source)

        st.write("Ouvindo áudio...")
        orders = r.recognize_google(audio_text, language="pt-BR")
        prompt = prepend + orders

        # Resumindo áudio com GPT
        st.write("Interpretando ordem de serviço...")
        response = ask_gpt(prompt)
        
        with st.expander("Transcrição completa da ordem de serviço:", expanded=False):
            st.write(orders)

        st.write("Resumo da ordem de serviço:")
        st.write(response)

        pressed = 1
        uploaded_files.clear()

if pressed:
    order_text = "**# RESUMO:**\n" + response
    uploaded_pdfs = []
    uploaded_pdfs = st.file_uploader("Insira manuais para conserto das peças acima:", type=['pdf'], accept_multiple_files=True)
    detected_text = ''

    if uploaded_pdfs:
        st.write("Lendo PDF...")
        for pdf in uploaded_pdfs:
            # Salvando os arquivos pdf
            path = os.path.join("userdata", pdf.name)
            with open(path, "wb") as f:
                f.write(pdf.getvalue())

            # Abrindo os arquivos pdf para leitura
            with open(path, 'rb') as pdf_file_obj:
                pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
                num_pages = len(pdf_reader.pages)

                # Transformando pdf em texto
                for page_num in range(num_pages):
                    page_obj = pdf_reader.pages[page_num]
                    detected_text += page_obj.extract_text() + '\n\n'

        # Preparando o prompt
        st.write("Interpretando texto...")
        prepend2 = "Procure nesse manual como consertar as máquinas descritas na lista com o máximo de informação possível"
        prompt = prepend2 + detected_text + response

        # Resposta do chatgpt
        response = ask_gpt(prompt)

        # Mostrando a Resposta
        st.write("Explicações de Conserto das Peças anteriorimente pedidas:")
        st.write(response)

        order_text += "\n\n# INSTRUÇÕES COMPLETAS:\n" + response

        # Gerando ordem de serviço para download
        pdf_path="userdata/service_order.pdf"
        create_pdf(pdf_path, order_text)

        #f.write(orders)
        with open(pdf_path, "rb") as f:
            st.download_button("Baixar ordem de serviço", f, file_name="service_order.pdf")
        
        uploaded_pdfs = []



##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################


st.title("Reserva de Equipamentos")

# Iniciar a conexão com o banco de dados
conexao = iniciar_conexao()

# Carregar técnicos do banco de dados
try:
    tecnicos = listar_tecnicos(conexao)  # Função que retorna os técnicos
    tecnicos_nomes = [tec['nome'] for tec in tecnicos]
except Exception as e:
    st.error(f"Erro ao carregar os técnicos: {e}")
    tecnicos_nomes = []

# Carregar equipamentos do banco de dados
try:
    equipamentos = listar_equipamentos(conexao)
    categorias = set(eqp['categoria'] for eqp in equipamentos)
    equipamentos_por_categoria = {categoria: [f"{eqp['cod_sap']}: {eqp['nome']}" for eqp in equipamentos if eqp['categoria'] == categoria] for categoria in categorias}
except Exception as e:
    st.error(f"Erro ao carregar os equipamentos: {e}")

# Inicializa a lista de equipamentos selecionados no estado de sessão, se não estiver inicializada
if "equipamentos_selecionados" not in st.session_state:
    st.session_state.equipamentos_selecionados = []

if "inicio" not in st.session_state: st.session_state.inicio = None
if "fim" not in st.session_state: st.session_state.fim = None

# Seleção do técnico responsável
st.header("Escolha do Técnico")
tecnico_responsavel = st.selectbox("Selecione o Técnico Responsável", tecnicos_nomes)

st.header("Equipamentos a serem usados")

# Seleção de categoria de equipamento
tipo_equip = st.selectbox(
    "Qual é a categoria de equipamento?",
    list(equipamentos_por_categoria.keys())
)

# Filtra as opções de equipamentos com base na categoria escolhida
equipamentos_disponiveis = equipamentos_por_categoria[tipo_equip]

# Seleção de equipamentos específicos com base na categoria
options = st.multiselect(
    "Equipamentos",
    equipamentos_disponiveis
)

# Adicionar as novas seleções à lista persistente
if st.button("Adicionar Equipamentos"):
    st.session_state.equipamentos_selecionados.extend([item for item in options if item not in st.session_state.equipamentos_selecionados])
    st.success("Equipamentos adicionados!")

# Exibir todos os equipamentos selecionados até agora
st.write("Equipamentos selecionados:", st.session_state.equipamentos_selecionados)

st.header("Horário de uso")
col1, col2 = st.columns(2)

with col1:
    date_inicio = st.date_input("Dia de início")
    time_inicio = st.time_input("Horário de início")
with col2:
    date_fim = st.date_input("Dia de fim")
    time_fim = st.time_input("Horário de fim")

# Combina data e hora em objetos datetime
inicio = datetime.combine(date_inicio, time_inicio)
fim = datetime.combine(date_fim, time_fim)

# Função para verificar se a data e o horário de início são menores que os de fim
def verificar_datas_horarios(inicio, fim):
    # Verifica se a data de início é maior ou igual à data de fim
    if inicio >= fim:
        st.error("Data e horário de início não podem ser maiores ou iguais ao de fim.")
        return False
    else:
        st.success("Data e horário válidos para a reserva.")
        st.session_state.inicio = inicio
        st.session_state.fim = fim
        return True

# Verificar as datas e horários
datas_validas = verificar_datas_horarios(inicio, fim)

# Adiciona o gráfico de linha do tempo
if datas_validas:
    # Cria um DataFrame com o evento
    df_event = pd.DataFrame([{
        'Equipamento': 'Reserva Selecionada',
        'Início': inicio,
        'Fim': fim
    }])

    # Cria o gráfico de linha do tempo usando Plotly Express
    fig = px.timeline(df_event, x_start='Início', x_end='Fim', y='Equipamento')
    fig.update_yaxes(autorange="reversed")  # Inverte a ordem do eixo Y (opcional)
    fig.update_layout(title='Linha do Tempo da Reserva')

    st.plotly_chart(fig, use_container_width=True)

# Função para inserir a ordem de serviço no banco de dados
def reservar_ordem_servico(hora_inicio, hora_fim, id_tecnico, descricao, equipamentos_list):
    try:
        id_ordem = inserir_ordem(conexao, descricao, hora_inicio, hora_fim, id_tecnico)
        for equipamento in equipamentos_list:
            cod_sap = equipamento[0:6]
            inserir_ordem_equipamento(conexao, cod_sap, id_ordem)
        st.success("Ordem de serviço criada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao criar a ordem de serviço: {e}")

# Botão para confirmar a reserva
if st.button("Confirmar Reserva") and datas_validas:
    if st.session_state.equipamentos_selecionados:

        inicio = st.session_state.inicio
        fim = st.session_state.fim
        equipamentos_selecionados = st.session_state.equipamentos_selecionados

        reservar_ordem_servico(inicio, fim, 1, "", equipamentos_selecionados)

        st.session_state.equipamentos_selecionados.clear()  # Limpa a lista após reserva
    else:
        st.warning("Selecione pelo menos um equipamento para reservar.")

# Fechar a conexão ao final
fechar_conexao(conexao)
