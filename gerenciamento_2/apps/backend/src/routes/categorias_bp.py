from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from src.schemas.categoria_schema import CategoriaSchema
from src.models import Categoria
from src.database import db

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/', methods=['GET'])
def get_categorias():
    """
    Lista todas as categorias
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias
        schema:
          type: array
          items:
            $ref: '#/definitions/Categoria'
    """
    categorias = Categoria.query.all()
    result = [CategoriaSchema(**c.to_dict()).model_dump() for c in categorias]
    return jsonify(result)

@categorias_bp.route('/<int:categoria_id>', methods=['GET'])
def get_categoria_by_id(categoria_id):
    """
    Obtém uma categoria pelo ID
    ---
    tags:
      - Categorias
    parameters:
      - name: categoria_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Categoria encontrada
        schema:
          $ref: '#/definitions/Categoria'
      404:
        description: Categoria não encontrada
    """
    categoria = Categoria.query.get(categoria_id)
    if categoria:
        result = CategoriaSchema(**categoria.to_dict()).model_dump()
        return jsonify(result)
    return jsonify({"error": "Categoria não encontrada"}), 404

@categorias_bp.route('/', methods=['POST'])
def create_categoria():
    """
    Cria uma nova categoria
    ---
    tags:
      - Categorias
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            cor:
              type: string
    responses:
      201:
        description: Categoria criada
        schema:
          $ref: '#/definitions/Categoria'
      400:
        description: Dados inválidos
    """
    data = request.json
    nova_categoria = Categoria(
        nome=data.get('nome'),
        cor=data.get('cor')
    )
    db.session.add(nova_categoria)
    db.session.commit()
    result = CategoriaSchema(**nova_categoria.to_dict()).model_dump()
    return jsonify(result), 201

@categorias_bp.route('/<int:categoria_id>', methods=['PUT'])
def update_categoria(categoria_id):
    """
    Atualiza uma categoria
    ---
    tags:
      - Categorias
    parameters:
      - name: categoria_id
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
            cor:
              type: string
    responses:
      200:
        description: Categoria atualizada
        schema:
          $ref: '#/definitions/Categoria'
      404:
        description: Categoria não encontrada
    """
    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        return jsonify({"error": "Categoria não encontrada"}), 404
    data = request.json
    if 'nome' in data:
        categoria.nome = data['nome']
    if 'cor' in data:
        categoria.cor = data['cor']
    db.session.commit()
    result = CategoriaSchema(**categoria.to_dict()).model_dump()
    return jsonify(result)

@categorias_bp.route('/<int:categoria_id>', methods=['DELETE'])
def delete_categoria(categoria_id):
    """
    Remove uma categoria
    ---
    tags:
      - Categorias
    parameters:
      - name: categoria_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Categoria removida
      404:
        description: Categoria não encontrada
    """
    categoria = Categoria.query.get(categoria_id)
    if not categoria:
        return jsonify({"error": "Categoria não encontrada"}), 404
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({"message": "Categoria removida com sucesso"})