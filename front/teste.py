import streamlit as st
import pandas as pd
from bd import iniciar_conexao, fechar_conexao, listar_equipamentos
from datetime import datetime

st.title("Reserva de Equipamentos")

# Iniciar a conexão com o banco de dados
conexao = iniciar_conexao()

# Carregar equipamentos do banco de dados
try:
    equipamentos = listar_equipamentos(conexao)
    categorias = set(eqp['categoria'] for eqp in equipamentos)
    equipamentos_por_categoria = {categoria: [eqp['nome'] for eqp in equipamentos if eqp['categoria'] == categoria] for categoria in categorias}
except Exception as e:
    st.error(f"Erro ao carregar os equipamentos: {e}")

# Inicializa a lista de equipamentos selecionados no estado de sessão, se não estiver inicializada
if "equipamentos_selecionados" not in st.session_state:
    st.session_state.equipamentos_selecionados = []

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

# Verificar as datas e horários
verificar_datas_horarios(date_inicio, time_inicio, date_fim, time_fim)


# Fechar a conexão ao final
fechar_conexao(conexao)
