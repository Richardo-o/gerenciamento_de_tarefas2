from pydantic import BaseModel
from datetime import datetime

class ComentarioSchema(BaseModel):
    id: int
    texto: str
    criado_em: datetime  
    tarefa_id: int