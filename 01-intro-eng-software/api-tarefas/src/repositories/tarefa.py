from typing import List, Optional
from src.models.tarefa_schema import TarefaIn, TarefaOut


class TarefaRepository:
    def __init__(self):
        self.tarefas: List[TarefaOut] = []
        self._next_id = 1

    def find(self) -> List[TarefaOut]:
        return self.tarefas

    def get(self, servidor_id: int) -> Optional[TarefaOut]:
        return next((s for s in self.tarefas if s.id == servidor_id), None)

    def add(self, data: TarefaIn) -> TarefaOut:
        new_tarefa = TarefaOut(id=self._next_id, **data.model_dump())
        self.tarefas.append(new_tarefa)
        self._next_id += 1
        return new_tarefa

    def delete(self, servidor_id: int):
        self.tarefas = [s for s in self.tarefas if s.id != servidor_id]

# Instância global
tarefa_repo = TarefaRepository()
