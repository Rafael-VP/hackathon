from flask import Flask, jsonify, request, g
from bd import iniciar_conexao, fechar_conexao, create_data_base, insert_template_data
from bd import inserir_equipamento, atualizar_equipamento, inserir_tecnico, atualizar_tecnico, inserir_maquina, atualizar_maquina, inserir_ordem, atualizar_ordem, inserir_ordem_equipamento, atualizar_ordem_equipamento
from bd import listar_equipamentos, listar_tecnicos, listar_maquinas, listar_ordens, listar_ordem_equipamento


app = Flask(__name__)

# Configuração de conexão por requisição
@app.before_request
def before_request():
    g.conexao = iniciar_conexao()

@app.teardown_request
def teardown_request(exception=None):
    fechar_conexao(g.conexao)

# Rota de teste - home
@app.route('/')
def home():
    # Listar todas as entidades
    equipamentos = listar_equipamentos(g.conexao)
    tecnicos = listar_tecnicos(g.conexao)
    maquinas = listar_maquinas(g.conexao)
    ordens = listar_ordens(g.conexao)
    ordem_equipamentos = listar_ordem_equipamento(g.conexao)

    return jsonify({
        "equipamentos": equipamentos,
        "tecnicos": tecnicos,
        "maquinas": maquinas,
        "ordens": ordens,
        "ordem_equipamentos": ordem_equipamentos
    })

# Reiniciar banco
@app.route('/reset', methods=['GET'])
def reset_database():
    create_data_base(g.conexao)
    insert_template_data(g.conexao)

    return home()


conexao = None
if __name__ == '__main__':
    conexao = iniciar_conexao()
    app.run(debug=True)