from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from src.schemas.tarefa_schema import TarefaSchema
from src.models import Tarefa, Projeto, Categoria
from src.database import db

tarefas_bp = Blueprint('tarefas', __name__)

@tarefas_bp.route('/', methods=['GET'])
def get_tarefas():
    """
    Lista todas as tarefas
    ---
    tags:
      - Tarefas
    responses:
      200:
        description: Lista de tarefas
        schema:
          type: array
          items:
            $ref: '#/definitions/Tarefa'
    """
    tarefas = Tarefa.query.all()
    result = [TarefaSchema(**t.to_dict()).model_dump() for t in tarefas]
    return jsonify(result)

@tarefas_bp.route('/<int:tarefa_id>', methods=['GET'])
def get_tarefa_by_id(tarefa_id):
    """
    Obtém uma tarefa pelo ID
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tarefa encontrada
        schema:
          $ref: '#/definitions/Tarefa'
      404:
        description: Tarefa não encontrada
    """
    tarefa = Tarefa.query.get(tarefa_id)
    if tarefa:
        result = TarefaSchema(**tarefa.to_dict()).model_dump()
        return jsonify(result)
    return jsonify({"error": "Tarefa não encontrada"}), 404

@tarefas_bp.route('/', methods=['POST'])
def create_tarefa():
    """
    Cria uma nova tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
            descricao:
              type: string
            concluida:
              type: boolean
            prioridade:
              type: string
              enum: ['baixa', 'media', 'alta']
            projeto_id:
              type: integer
            categoria_id:
              type: integer
    responses:
      201:
        description: Tarefa criada
        schema:
          $ref: '#/definitions/Tarefa'
      400:
        description: Dados inválidos
      404:
        description: Projeto ou categoria não encontrado
    """
    data = request.json
    
    prioridades_validas = ['baixa', 'media', 'alta']
    if data.get('prioridade') and data['prioridade'] not in prioridades_validas:
        return jsonify({"error": f"Prioridade deve ser uma de: {prioridades_validas}"}), 400
    
    if data.get('projeto_id'):
        projeto = Projeto.query.get(data['projeto_id'])
        if not projeto:
            return jsonify({"error": "Projeto não encontrado"}), 404
    
    if data.get('categoria_id'):
        categoria = Categoria.query.get(data['categoria_id'])
        if not categoria:
            return jsonify({"error": "Categoria não encontrada"}), 404
    
    nova_tarefa = Tarefa(
        titulo=data.get('titulo'),
        descricao=data.get('descricao'),
        concluida=data.get('concluida', False),
        prioridade=data.get('prioridade', 'media'),
        criado_em=datetime.now(timezone.utc),
        projeto_id=data.get('projeto_id'),
        categoria_id=data.get('categoria_id')
    )
    db.session.add(nova_tarefa)
    db.session.commit()
    result = TarefaSchema(**nova_tarefa.to_dict()).model_dump()
    return jsonify(result), 201

@tarefas_bp.route('/<int:tarefa_id>', methods=['PUT'])
def update_tarefa(tarefa_id):
    """
    Atualiza uma tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
            descricao:
              type: string
            concluida:
              type: boolean
            prioridade:
              type: string
            projeto_id:
              type: integer
            categoria_id:
              type: integer
    responses:
      200:
        description: Tarefa atualizada
        schema:
          $ref: '#/definitions/Tarefa'
      404:
        description: Tarefa não encontrada
    """
    tarefa = Tarefa.query.get(tarefa_id)
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    
    data = request.json
    if 'prioridade' in data:
        prioridades_validas = ['baixa', 'media', 'alta']
        if data['prioridade'] not in prioridades_validas:
            return jsonify({"error": f"Prioridade deve ser uma de: {prioridades_validas}"}), 400
    if 'titulo' in data:
        tarefa.titulo = data['titulo']
    if 'descricao' in data:
        tarefa.descricao = data['descricao']
    if 'concluida' in data:
        tarefa.concluida = data['concluida']
    if 'prioridade' in data:
        tarefa.prioridade = data['prioridade']
    if 'projeto_id' in data:
        tarefa.projeto_id = data['projeto_id']
    if 'categoria_id' in data:
        tarefa.categoria_id = data['categoria_id']
    
    db.session.commit()
    result = TarefaSchema(**tarefa.to_dict()).model_dump()
    return jsonify(result)

@tarefas_bp.route('/<int:tarefa_id>', methods=['DELETE'])
def delete_tarefa(tarefa_id):
    """
    Remove uma tarefa
    ---
    tags:
      - Tarefas
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Tarefa removida
      404:
        description: Tarefa não encontrada
    """
    tarefa = Tarefa.query.get(tarefa_id)
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({"message": "Tarefa removida com sucesso"})