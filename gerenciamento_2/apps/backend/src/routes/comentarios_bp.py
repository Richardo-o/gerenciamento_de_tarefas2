from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from src.schemas.comentario_schema import ComentarioSchema
from src.models import Comentario, Tarefa
from src.database import db

comentarios_bp = Blueprint('comentarios', __name__)

@comentarios_bp.route('/', methods=['GET'])
def get_comentarios():
    """
    Lista todos os comentários
    ---
    tags:
      - Comentarios
    responses:
      200:
        description: Lista de comentários
        schema:
          type: array
          items:
            $ref: '#/definitions/Comentario'
    """
    comentarios = Comentario.query.all()
    result = [ComentarioSchema(**c.to_dict()).model_dump() for c in comentarios]
    return jsonify(result)

@comentarios_bp.route('/<int:comentario_id>', methods=['GET'])
def get_comentario_by_id(comentario_id):
    """
    Obtém um comentário pelo ID
    ---
    tags:
      - Comentarios
    parameters:
      - name: comentario_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Comentário encontrado
        schema:
          $ref: '#/definitions/Comentario'
      404:
        description: Comentário não encontrado
    """
    comentario = Comentario.query.get(comentario_id)
    if comentario:
        result = ComentarioSchema(**comentario.to_dict()).model_dump()
        return jsonify(result)
    return jsonify({"error": "Comentário não encontrado"}), 404

@comentarios_bp.route('/tarefa/<int:tarefa_id>', methods=['GET'])
def get_comentarios_by_tarefa(tarefa_id):
    """
    Lista comentários de uma tarefa específica
    ---
    tags:
      - Comentarios
    parameters:
      - name: tarefa_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de comentários da tarefa
        schema:
          type: array
          items:
            $ref: '#/definitions/Comentario'
      404:
        description: Tarefa não encontrada
    """
    tarefa = Tarefa.query.get(tarefa_id)
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    comentarios = Comentario.query.filter_by(tarefa_id=tarefa_id).all()
    result = [ComentarioSchema(**c.to_dict()).model_dump() for c in comentarios]
    return jsonify(result)

@comentarios_bp.route('/', methods=['POST'])
def create_comentario():
    """
    Cria um novo comentário
    ---
    tags:
      - Comentarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            texto:
              type: string
            tarefa_id:
              type: integer
    responses:
      201:
        description: Comentário criado
        schema:
          $ref: '#/definitions/Comentario'
      400:
        description: Dados inválidos
      404:
        description: Tarefa não encontrada
    """
    data = request.json
    tarefa = Tarefa.query.get(data.get('tarefa_id'))
    if not tarefa:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    novo_comentario = Comentario(
        texto=data.get('texto'),
        criado_em=datetime.now(timezone.utc),
        tarefa_id=data.get('tarefa_id')
    )
    db.session.add(novo_comentario)
    db.session.commit()
    result = ComentarioSchema(**novo_comentario.to_dict()).model_dump()
    return jsonify(result), 201

@comentarios_bp.route('/<int:comentario_id>', methods=['PUT'])
def update_comentario(comentario_id):
    """
    Atualiza um comentário
    ---
    tags:
      - Comentarios
    parameters:
      - name: comentario_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            texto:
              type: string
    responses:
      200:
        description: Comentário atualizado
        schema:
          $ref: '#/definitions/Comentario'
      404:
        description: Comentário não encontrado
    """
    comentario = Comentario.query.get(comentario_id)
    if not comentario:
        return jsonify({"error": "Comentário não encontrado"}), 404
    data = request.json
    if 'texto' in data:
        comentario.texto = data['texto']
    db.session.commit()
    result = ComentarioSchema(**comentario.to_dict()).model_dump()
    return jsonify(result)

@comentarios_bp.route('/<int:comentario_id>', methods=['DELETE'])
def delete_comentario(comentario_id):
    """
    Remove um comentário
    ---
    tags:
      - Comentarios
    parameters:
      - name: comentario_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Comentário removido
      404:
        description: Comentário não encontrado
    """
    comentario = Comentario.query.get(comentario_id)
    if not comentario:
        return jsonify({"error": "Comentário não encontrado"}), 404
    db.session.delete(comentario)
    db.session.commit()
    return jsonify({"message": "Comentário removido com sucesso"})