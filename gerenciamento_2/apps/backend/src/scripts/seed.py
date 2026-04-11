import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.app import create_app
from src.database import db
from src.models import Projeto, Categoria, Tarefa, Comentario

def seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        if Projeto.query.first():
            print('Banco já populado.')
            return

        projetos = [
            Projeto(nome='Projeto Alpha', descricao='Projeto de desenvolvimento Alpha'),
            Projeto(nome='Projeto Beta', descricao='Projeto de teste Beta'),
            Projeto(nome='Projeto Gamma', descricao='Projeto de estudos avançados'),
        ]
        db.session.add_all(projetos)
        db.session.commit()
        print(f'✓ {len(projetos)} projetos criados')

        categorias = [
            Categoria(nome='Trabalho', cor='#FF0000'),
            Categoria(nome='Pessoal', cor='#00FF00'),
            Categoria(nome='Estudos', cor='#0000FF'),
            Categoria(nome='Urgente', cor='#FFA500'),
        ]
        db.session.add_all(categorias)
        db.session.commit()
        print(f'✓ {len(categorias)} categorias criadas')

        tarefas = [
            Tarefa(
                titulo='Implementar login',
                descricao='Criar tela de login com validação JWT',
                concluida=False,
                prioridade='alta',
                projeto_id=projetos[0].id,
                categoria_id=categorias[0].id
            ),
            Tarefa(
                titulo='Configurar banco',
                descricao='Configurar PostgreSQL com Docker Compose',
                concluida=True,
                prioridade='media',
                projeto_id=projetos[0].id,
                categoria_id=categorias[0].id
            ),
            Tarefa(
                titulo='Ler livro Python',
                descricao='Ler capítulo 5 sobre orientação a objetos',
                concluida=False,
                prioridade='baixa',
                projeto_id=None,
                categoria_id=categorias[2].id
            ),
            Tarefa(
                titulo='Revisar pull requests',
                descricao='Revisar PRs pendentes do time',
                concluida=False,
                prioridade='alta',
                projeto_id=projetos[1].id,
                categoria_id=categorias[0].id
            ),
            Tarefa(
                titulo='Fazer exercícios',
                descricao='Resolver exercícios do capítulo 5',
                concluida=False,
                prioridade='media',
                projeto_id=None,
                categoria_id=categorias[2].id
            ),
        ]
        db.session.add_all(tarefas)
        db.session.commit()
        print(f'✓ {len(tarefas)} tarefas criadas')

        comentarios = [
            Comentario(
                texto='Começar pela autenticação OAuth2 com Google',
                tarefa_id=tarefas[0].id
            ),
            Comentario(
                texto='Usar Docker Compose com PostgreSQL e pgAdmin',
                tarefa_id=tarefas[1].id
            ),
            Comentario(
                texto='Ver exemplos do livro no GitHub',
                tarefa_id=tarefas[2].id
            ),
            Comentario(
                texto='Priorizar PRs com label "critical"',
                tarefa_id=tarefas[3].id
            ),
        ]
        db.session.add_all(comentarios)
        db.session.commit()
        print(f'✓ {len(comentarios)} comentários criados')

        print('\n✅ Dados iniciais inseridos com sucesso!')
        
        print('\n--- RESUMO ---')
        print(f'Projetos: {Projeto.query.count()}')
        print(f'Categorias: {Categoria.query.count()}')
        print(f'Tarefas: {Tarefa.query.count()}')
        print(f'Comentários: {Comentario.query.count()}')

if __name__ == '__main__':
    seed()