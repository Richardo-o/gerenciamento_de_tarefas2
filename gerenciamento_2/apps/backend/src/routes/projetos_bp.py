from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from src.schemas.projeto_schema import ProjetoSchema
from src.models import Projeto
from src.database import db

projetos_bp = Blueprint('projetos', __name__)

@projetos_bp.route('/', methods=['GET'])
def get_projetos():
    """
    Lista todos os projetos
    ---
    tags:
      - Projetos
    responses:
      200:
        description: Lista de projetos
        schema:
          type: array
          items:
            $ref: '#/definitions/ProjetoSchema'
    """
    projetos = Projeto.query.all()
    result = [ProjetoSchema(**projeto.to_dict()).model_dump() for projeto in projetos]
    return jsonify(result)

@projetos_bp.route('/<int:projeto_id>', methods=['GET'])
def get_projeto_by_id(projeto_id):
    """
    Obtém um projeto por ID
    ---
    tags:
      - Projetos
    parameters:
      - name: projeto_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Projeto encontrado
        schema:
          $ref: '#/definitions/ProjetoSchema'
      404:
        description: Projeto não encontrado
    """
    projeto = Projeto.query.get(projeto_id)
    if projeto:
        result = ProjetoSchema(**projeto.to_dict()).model_dump()
        return jsonify(result)
    return jsonify({"error": "Projeto não encontrado"}), 404

@projetos_bp.route('/', methods=['POST'])
def create_projeto():
    """
    Cria um novo projeto
    ---
    tags:
      - Projetos
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            descricao:
              type: string
    responses:
      201:
        description: Projeto criado
        schema:
          $ref: '#/definitions/ProjetoSchema'
      400:
        description: Dados inválidos
    """
    data = request.json
    if not data or not data.get('nome'):
        return jsonify({"error": "Nome é obrigatório"}), 400
    novo_projeto = Projeto(
        nome=data['nome'],
        descricao=data.get('descricao'),
        criado_em=datetime.now(timezone.utc)
    )
    db.session.add(novo_projeto)
    db.session.commit()
    result = ProjetoSchema(**novo_projeto.to_dict()).model_dump()
    return jsonify(result), 201

@projetos_bp.route('/<int:projeto_id>', methods=['PUT'])
def update_projeto(projeto_id):
    """
    Atualiza um projeto existente
    ---
    tags:
      - Projetos
    parameters:
      - name: projeto_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            descricao:
              type: string
    responses:
      200:
        description: Projeto atualizado
        schema:
          $ref: '#/definitions/ProjetoSchema'
      404:
        description: Projeto não encontrado
    """
    projeto = Projeto.query.get(projeto_id)
    if not projeto:
        return jsonify({"error": "Projeto não encontrado"}), 404
    data = request.json
    if 'nome' in data:
        projeto.nome = data['nome']
    if 'descricao' in data:
        projeto.descricao = data['descricao']
    db.session.commit()
    result = ProjetoSchema(**projeto.to_dict()).model_dump()
    return jsonify(result)

@projetos_bp.route('/<int:projeto_id>', methods=['DELETE'])
def delete_projeto(projeto_id):
    """
    Remove um projeto
    ---
    tags:
      - Projetos
    parameters:
      - name: projeto_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Projeto removido
      404:
        description: Projeto não encontrado
    """
    projeto = Projeto.query.get(projeto_id)
    if not projeto:
        return jsonify({"error": "Projeto não encontrado"}), 404
    db.session.delete(projeto)
    db.session.commit()
    return jsonify({"message": "Projeto removido com sucesso"})