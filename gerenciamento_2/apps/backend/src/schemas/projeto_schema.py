from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjetoSchema(BaseModel):
    id: int
    nome: str
    descricao: Optional[str] = None  
    criado_em: datetime  