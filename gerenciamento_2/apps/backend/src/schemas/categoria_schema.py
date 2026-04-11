from pydantic import BaseModel

class CategoriaSchema(BaseModel):
    id: int
    nome: str
    cor: str
    