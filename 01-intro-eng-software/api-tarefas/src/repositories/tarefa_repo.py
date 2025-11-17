from typing import List, Optional
from src.models.tarefa_schema import TarefaIn, TarefaOut


class TarefaRepository:
    def __init__(self):
        self.tarefas: List[TarefaOut] = []
        self._next_id = 1

    def find(self) -> List[TarefaOut]:
        return self.tarefas

    def find_by_servidor(self, servidor_id: int) -> List[TarefaOut]:
        return [t for t in self.tarefas if t.responsavel_id == servidor_id]

    def get(self, tarefa_id: int) -> Optional[TarefaOut]:
        return next((s for s in self.tarefas if s.id == tarefa_id), None)

    def add(self, data: TarefaIn) -> TarefaOut:
        new_tarefa = TarefaOut(id=self._next_id, **data.model_dump())
        self.tarefas.append(new_tarefa)
        self._next_id += 1
        return new_tarefa

    def delete(self, tarefa_id: int):
        self.tarefas = [s for s in self.tarefas if s.id != tarefa_id]

# Instância global
tarefa_repo = TarefaRepository()
