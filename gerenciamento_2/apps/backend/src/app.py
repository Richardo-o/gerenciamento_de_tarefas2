from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
import os
from src.database import db

# IMPORTS CORRETOS com src.
from src.schemas.projeto_schema import ProjetoSchema
from src.schemas.tarefa_schema import TarefaSchema
from src.schemas.categoria_schema import CategoriaSchema
from src.schemas.comentario_schema import ComentarioSchema

load_dotenv()

def create_app():
    app = Flask(__name__)

    from src.database import init_db
    init_db(app)

    app.config['SWAGGER'] = {
        'title': 'API de Gerenciamento de Projetos e Tarefas',
        'uiversion': 3,
        'description': 'API para gerenciamento de projetos, tarefas, categorias e comentários',
        'specs_route': '/apidocs/'
    }

    swagger_template = {
        "tags": [
            {"name": "Projetos"},
            {"name": "Tarefas"},
            {"name": "Categorias"},
            {"name": "Comentarios"}
        ],
        "definitions": {
            "Projeto": ProjetoSchema.model_json_schema(),
            "Tarefa": TarefaSchema.model_json_schema(),
            "Categoria": CategoriaSchema.model_json_schema(),
            "Comentario": ComentarioSchema.model_json_schema(),
            "Error": {
                "type": "object",
                "properties": {"error": {"type": "string"}}
            }
        }
    }

    Swagger(app, template=swagger_template)

    from src.routes.projetos_bp import projetos_bp
    from src.routes.tarefas_bp import tarefas_bp
    from src.routes.categorias_bp import categorias_bp
    from src.routes.comentarios_bp import comentarios_bp
    
    app.register_blueprint(projetos_bp, url_prefix='/api/projetos')
    app.register_blueprint(tarefas_bp, url_prefix='/api/tarefas')
    app.register_blueprint(categorias_bp, url_prefix='/api/categorias')
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)