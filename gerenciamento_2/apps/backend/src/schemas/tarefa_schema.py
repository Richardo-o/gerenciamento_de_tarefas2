from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TarefaSchema(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None 
    concluida: bool  
    prioridade: str  
    criado_em: datetime  
    projeto_id: Optional[int] = None  
    categoria_id: Optional[int] = None  