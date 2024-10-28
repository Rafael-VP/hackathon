import streamlit as st
import os
import configparser
import speech_recognition as sr
from openai import OpenAI
from pydub import AudioSegment
import pandas as pd
from bd import iniciar_conexao, fechar_conexao, listar_equipamentos, inserir_ordem, inserir_ordem_equipamento, listar_tecnicos
import plotly.express as px
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read("config.ini")

r = sr.Recognizer()

client = OpenAI(api_key=config['Main']['gpt_key'])
prepend = "Resuma o seguinte texto em uma lista de tarefas:\n "

st.title("Ordem de serviço:")
uploaded_files = st.file_uploader("Arquivos de áudio:", type=['ogg', 'wav'], accept_multiple_files=True)

for uploaded_file in uploaded_files:
        # Salvando arquivo ogg
        path = os.path.join("userdata", uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
        print(path)

        # Convertendo arquivo para WAV
        audio = AudioSegment.from_ogg(path)
        path = path.replace("ogg", "wav")
        audio.export(path, format="wav")

        # Convertendo áudio para texto
        file_audio = sr.AudioFile(path)

        with file_audio as source:
            audio_text = r.record(source)

        #st.write(type(audio_text))
        st.write("Ouvindo áudio...")
        orders = r.recognize_google(audio_text, language="pt-BR")
        prompt = prepend + orders

        st.write("Interpretando ordem de serviço...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content":prompt}
            ]
        )

        st.write(response.choices[0].message.content)

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

# Função para verificar se a data e o horário de início são menores que os de fim
def verificar_datas_horarios(data_inicio, hora_inicio, data_fim, hora_fim):
    # Combina data e hora em objetos datetime
    inicio = datetime.combine(data_inicio, hora_inicio)
    fim = datetime.combine(data_fim, hora_fim)
    
    # Verifica se a data de início é maior ou igual à data de fim
    if inicio >= fim:
        st.error("Data e horário de início não podem ser maiores ou iguais ao de fim.")
    else:
        st.success("Data e horário válidos para a reserva.")
        st.session_state.inicio = inicio
        st.session_state.fim = fim

# Verificar as datas e horários
verificar_datas_horarios(date_inicio, time_inicio, date_fim, time_fim)

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

        
# Supondo que a sessão de estado já tenha os valores de 'inicio', 'fim', e 'tecnico_responsavel'
# Verifica se esses valores estão definidos antes de construir o gráfico
if st.session_state.inicio and st.session_state.fim and "equipamentos_selecionados" in st.session_state and st.session_state.equipamentos_selecionados:
    
    # Construção do DataFrame com os dados da ordem de serviço e do técnico
    data = {
        'Equipamento': st.session_state.equipamentos_selecionados,
        'Início': [st.session_state.inicio] * len(st.session_state.equipamentos_selecionados),
        'Fim': [st.session_state.fim] * len(st.session_state.equipamentos_selecionados),
        'Técnico': [tecnico_responsavel] * len(st.session_state.equipamentos_selecionados)
    }

    df = pd.DataFrame(data)

    # Criar o gráfico de Gantt usando Plotly
    fig = px.timeline(df, x_start="Início", x_end="Fim", y="Equipamento", color="Técnico", title="Gráfico de Gantt de Projetos")

    # Ajustar o layout do gráfico para mostrar o eixo x de hora em hora
    fig.update_layout(
        xaxis_title="Hora",
        yaxis_title="Equipamento",
        title="Calendário de Tarefas e Responsáveis",
        height=500,
        xaxis=dict(
            tickformat="%H:%M",  # Formato para mostrar apenas horas e minutos
            dtick=3600000  # Define o intervalo das marcações de eixo x para 1 hora (em milissegundos)
        )
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
else:
    st.warning("Por favor, preencha todos os dados de reserva para gerar o gráfico.")

# Botão para confirmar a reserva
datas_validas = True # TODO
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
