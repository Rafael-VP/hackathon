import sqlite3

def iniciar_conexao():
    return sqlite3.connect('manutencao.db')

def fechar_conexao(conexao):
    conexao.close()

def create_data_base(conexao):
    cursor = conexao.cursor()

    # Dropping tables if they exist
    cursor.execute('DROP TABLE IF EXISTS equipamento')
    cursor.execute('DROP TABLE IF EXISTS tecnico')
    cursor.execute('DROP TABLE IF EXISTS maquina')
    cursor.execute('DROP TABLE IF EXISTS ordem')
    cursor.execute('DROP TABLE IF EXISTS ordem_equipamento')
    
    # Criação das tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS equipamento (
        cod_sap TEXT PRIMARY KEY,
        nome TEXT,
        categoria TEXT,
        busca TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tecnico (
        id_tecnico INTEGER PRIMARY KEY,
        nome TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maquina (
        id_maquina INTEGER PRIMARY KEY,
        nome TEXT
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordem (
        id_ordem INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        hora_inicio TEXT,
        hora_fim TEXT,
        id_tecnico INTEGER,
        FOREIGN KEY (id_tecnico) REFERENCES tecnico(id_tecnico)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordem_equipamento (
        cod_sap TEXT,
        id_ordem INTEGER,
        FOREIGN KEY (id_ordem) REFERENCES ordem(id_ordem),
        FOREIGN KEY (cod_sap) REFERENCES equipamento(cod_sap)
    )''')
    
    conexao.commit()

def insert_template_data(conexao):
    inserir_equipamento(conexao, 'MAT001', 'Serra Circular', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT002', 'Disco de Corte', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT003', 'Serra de Fita', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT004', 'Disco de Desbaste', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT005', 'Broca de Aço Rápido 10mm', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT006', 'Conjunto de Fresas para Usinagem', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT007', 'Lâmina de Serra Sabre', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'EQP001', 'Lixadeira Angular', 'Ferramentas de Corte')
    inserir_equipamento(conexao, 'MAT101', 'Paquímetro Digital', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT102', 'Micrômetro', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT103', 'Relógio Comparador', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT104', 'Trena de Aço 5m', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT105', 'Nível de Bolha', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT106', 'Goniômetro Digital', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT107', 'Manômetro para Pressão', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'MAT108', 'Calibrador de Roscas', 'Ferramentas de Medição')
    inserir_equipamento(conexao, 'EQP201', 'Máquina de Solda MIG', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT201', 'Eletrodo de Solda Inox', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT202', 'Máscara de Solda Automática', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'EQP202', 'Maçarico de Corte Oxiacetilênico', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT203', 'Tocha de Solda TIG', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT204', 'Fio de Solda MIG ER70S-6', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT205', 'Regulador de Pressão para Gás', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT206', 'Tubo de Gás Acetileno', 'Equipamentos de Solda')
    inserir_equipamento(conexao, 'MAT301', 'Graxa Industrial', 'Lubrificação e Manutenção')
    inserir_equipamento(conexao, 'MAT302', 'Óleo Lubrificante 10W30', 'Lubrificação e Manutenção')
    inserir_equipamento(conexao, 'EQP301', 'Bomba de Graxa Pneumática', 'Lubrificação e Manutenção')
    inserir_equipamento(conexao, 'MAT303', 'Limpa Contatos Elétricos', 'Lubrificação e Manutenção')
    inserir_equipamento(conexao, 'MAT304', 'Spray Desengripante', 'Lubrificação e Manutenção')
    inserir_equipamento(conexao, 'MAT305', 'Veda Rosca em Fita', 'Lubrificação e Manutenção')
    inserir_equipamento(conexao, 'MAT401', 'Capacete de Segurança com Aba', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT402', 'Luvas Térmicas de Alta Resistência', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT403', 'Óculos de Proteção Antirrespingos', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT404', 'Protetor Auricular Tipo Plug', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT405', 'Máscara Respiratória com Filtro P3', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT406', 'Cinto de Segurança para Trabalho em Altura', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT407', 'Sapato de Segurança com Biqueira de Aço', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'MAT408', 'Protetor Facial de Policarbonato', 'Equipamentos de Segurança')
    inserir_equipamento(conexao, 'EQP501', 'Talha Elétrica de Corrente', 'Equipamentos de Elevação')
    inserir_equipamento(conexao, 'MAT501', 'Corrente de Elevação de 10m', 'Equipamentos de Elevação')
    inserir_equipamento(conexao, 'MAT502', 'Gancho Giratório com Trava de Segurança', 'Equipamentos de Elevação')
    inserir_equipamento(conexao, 'MAT503', 'Cinta de Elevação com Olhal', 'Equipamentos de Elevação')
    inserir_equipamento(conexao, 'EQP502', 'Carrinho de Transporte de Bobinas', 'Equipamentos de Elevação')
    inserir_equipamento(conexao, 'EQP503', 'Macaco Hidráulico 10 Toneladas', 'Equipamentos de Elevação')
    inserir_equipamento(conexao, 'MAT601', 'Rolamento Esférico de Precisão', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT602', 'Parafuso de Alta Resistência M12', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT603', 'Correia de Transmissão Industrial', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT604', 'Junta de Vedação em Borracha', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT605', 'Engrenagem Cilíndrica de Aço', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT606', 'Bucha de Bronze Autolubrificante', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT607', 'Eixo de Transmissão', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'MAT608', 'Polia de Alumínio', 'Componentes Mecânicos')
    inserir_equipamento(conexao, 'EQP601', 'Válvula Solenoide Hidráulica', 'Equipamentos Hidráulicos')
    inserir_equipamento(conexao, 'EQP602', 'Bomba Hidráulica de Pistão', 'Equipamentos Hidráulicos')
    inserir_equipamento(conexao, 'MAT701', 'Mangueira Hidráulica de Alta Pressão', 'Equipamentos Hidráulicos')
    inserir_equipamento(conexao, 'MAT702', 'Conector Hidráulico Rápido', 'Equipamentos Hidráulicos')
    inserir_equipamento(conexao, 'EQP701', 'Motor Elétrico Trifásico 5HP', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'MAT801', 'Cabo Elétrico 10mm²', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'MAT802', 'Disjuntor de 100A', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'EQP702', 'Quadro de Comando Elétrico com Inversor de Frequência', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'MAT803', 'Chave Seccionadora', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'MAT804', 'Fusível NH 100A', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'MAT805', 'Tomada Industrial 380V', 'Equipamentos Elétricos')
    inserir_equipamento(conexao, 'MAT901', 'Chave de Fenda Phillips 6mm', 'Ferramentas Manuais')
    inserir_equipamento(conexao, 'MAT902', 'Alicate de Corte', 'Ferramentas Manuais')
    inserir_equipamento(conexao, 'MAT903', 'Martelo de Borracha', 'Ferramentas Manuais')
    inserir_equipamento(conexao, 'MAT904', 'Torquímetro 40-200Nm', 'Ferramentas Manuais')
    inserir_equipamento(conexao, 'MAT905', 'Conjunto de Chaves Allen', 'Ferramentas Manuais')
    inserir_equipamento(conexao, 'MAT906', 'Chave Estrela 12mm', 'Ferramentas Manuais')
    inserir_equipamento(conexao, 'MAT907', 'Serra Manual', 'Ferramentas Manuais')

    inserir_tecnico(conexao, 1, "José")

    conexao.commit()

def inserir_equipamento(conexao, cod_sap, nome, categoria, busca = ''):
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO equipamento (cod_sap, nome, categoria, busca) VALUES (?, ?, ?, ?)''', (cod_sap, nome, categoria, busca))
    conexao.commit()

def atualizar_equipamento(conexao, cod_sap, nome, categoria, busca):
    cursor = conexao.cursor()
    cursor.execute('''UPDATE equipamento SET nome = ?, categoria = ?, busca = ? WHERE cod_sap = ?''', (nome, categoria, busca, cod_sap))
    conexao.commit()

def inserir_tecnico(conexao, id_tecnico, nome):
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO tecnico (id_tecnico, nome) VALUES (?, ?)''', (id_tecnico, nome))
    conexao.commit()

def atualizar_tecnico(conexao, id_tecnico, nome):
    cursor = conexao.cursor()
    cursor.execute('''UPDATE tecnico SET nome = ? WHERE id_tecnico = ?''', (nome, id_tecnico))
    conexao.commit()

def inserir_maquina(conexao, id_maquina, nome):
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO maquina (id_maquina, nome) VALUES (?, ?)''', (id_maquina, nome))
    conexao.commit()

def atualizar_maquina(conexao, id_maquina, nome):
    cursor = conexao.cursor()
    cursor.execute('''UPDATE maquina SET nome = ? WHERE id_maquina = ?''', (nome, id_maquina))
    conexao.commit()

# def inserir_ordem(conexao, id_ordem, descricao, hora_inicio, hora_fim, id_tecnico):
#     cursor = conexao.cursor()
#     cursor.execute('''INSERT INTO ordem (id_ordem, descricao, hora_inicio, hora_fim, id_tecnico) VALUES (?, ?, ?, ?, ?)''', (id_ordem, descricao, hora_inicio, hora_fim, id_tecnico))
#     conexao.commit()

def inserir_ordem(conexao, descricao, hora_inicio, hora_fim, id_tecnico):
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO ordem (descricao, hora_inicio, hora_fim, id_tecnico) VALUES (?, ?, ?, ?)''', (descricao, hora_inicio, hora_fim, id_tecnico))
    conexao.commit()
    return cursor.lastrowid

def atualizar_ordem(conexao, id_ordem, descricao, hora_inicio, hora_fim, id_tecnico):
    cursor = conexao.cursor()
    cursor.execute('''UPDATE ordem SET descricao = ?, hora_inicio = ?, hora_fim = ?, id_tecnico = ? WHERE id_ordem = ?''', (descricao, hora_inicio, hora_fim, id_tecnico, id_ordem))
    conexao.commit()

def inserir_ordem_equipamento(conexao, cod_sap, id_ordem):
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO ordem_equipamento (cod_sap, id_ordem) VALUES (?, ?)''', (cod_sap, id_ordem))
    conexao.commit()

def atualizar_ordem_equipamento(conexao, cod_sap, id_ordem, novo_cod_sap, novo_id_ordem):
    cursor = conexao.cursor()
    cursor.execute('''UPDATE ordem_equipamento SET cod_sap = ?, id_ordem = ? WHERE cod_sap = ? AND id_ordem = ?''', (novo_cod_sap, novo_id_ordem, cod_sap, id_ordem))
    conexao.commit()

def listar_equipamentos(conexao):
    conexao.row_factory = sqlite3.Row  # Allows indexing by column name
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM equipamento''')
    equipamentos = [dict(row) for row in cursor.fetchall()]  # Convert rows to dictionaries
    return equipamentos

def listar_tecnicos(conexao):
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM tecnico''')
    tecnicos = [dict(row) for row in cursor.fetchall()]
    return tecnicos

def listar_maquinas(conexao):
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM maquina''')
    maquinas = [dict(row) for row in cursor.fetchall()]
    return maquinas

def listar_ordens(conexao):
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM ordem''')
    ordens = [dict(row) for row in cursor.fetchall()]
    return ordens

def listar_ordem_equipamento(conexao):
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM ordem_equipamento''')
    ordem_equipamentos = [dict(row) for row in cursor.fetchall()]
    return ordem_equipamentos
