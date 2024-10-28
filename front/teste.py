import streamlit as st
import pandas as pd

st.title("Reserva de Equipamentos")

# filtro
equipamentos_por_categoria = {
    "Ferramentas de corte": ["Serra Circular", "Disco de Corte", "Serra de Fita"],
    "Ferramentas de Medição": ["Trena", "Micrômetro", "Paquímetro"],
    "Equipamentos de Solda": ["Maçarico", "Soldador Elétrico", "Máscara de Solda"],
    "Lubrificação e Manutenção": ["Lubrificante", "Desengripante", "Pistola de Graxa"],
    "Equipamentos de Segurança": ["Capacete", "Óculos de Proteção", "Luvas"],
    "Equipamentos de Elevação": ["Guincho", "Elevador Hidráulico", "Pás"],
    "Componentes Mecânicos": ["Parafuso", "Porca", "Anel de Vedação"],
    "Equipamentos Hidráulicos": ["Bomba Hidráulica", "Mangueira", "Válvula de Controle"],
    "Equipamentos Elétricos": ["Multímetro", "Alicate de Crimpar", "Fonte de Alimentação"],
    "Ferramentas Manuais": ["Martelo", "Chave de Fenda", "Alicate"]
}

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

