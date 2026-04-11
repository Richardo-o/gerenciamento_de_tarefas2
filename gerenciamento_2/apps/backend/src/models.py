from datetime import datetime, timezone
from src.database import db


class Projeto(db.Model):
    __tablename__ = 'projetos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    tarefas = db.relationship('Tarefa', backref='projeto', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'criado_em': self.criado_em.isoformat()
        }


class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    cor = db.Column(db.String(7), default='#000000')

    tarefas = db.relationship('Tarefa', backref='categoria', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cor': self.cor
        }


class Tarefa(db.Model):
    __tablename__ = 'tarefas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    concluida = db.Column(db.Boolean, default=False)
    prioridade = db.Column(db.String(10), default='media')
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)

    comentarios = db.relationship('Comentario', backref='tarefa', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'concluida': self.concluida,
            'prioridade': self.prioridade,
            'criado_em': self.criado_em.isoformat(),
            'projeto_id': self.projeto_id,
            'categoria_id': self.categoria_id
        }


class Comentario(db.Model):
    __tablename__ = 'comentarios'

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefas.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'texto': self.texto,
            'criado_em': self.criado_em.isoformat(),
            'tarefa_id': self.tarefa_id
        }