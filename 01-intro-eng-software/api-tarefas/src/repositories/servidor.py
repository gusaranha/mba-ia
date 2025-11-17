from typing import List, Optional
from src.models.servidor_schema import ServidorOut, ServidorIn


class ServidorRepository:
    def __init__(self):
        self.servidores: List[ServidorOut] = []
        self._next_id = 1

    def find(self) -> List[ServidorOut]:
        return self.servidores

    def get(self, servidor_id: int) -> Optional[ServidorOut]:
        return next((s for s in self.servidores if s.id == servidor_id), None)

    def add(self, data: ServidorIn) -> ServidorOut:
        new_servidor = ServidorOut(id=self._next_id, **data.model_dump())
        self.servidores.append(new_servidor)
        self._next_id += 1
        return new_servidor

    def delete(self, servidor_id: int):
        self.servidores = [s for s in self.servidores if s.id != servidor_id]

# Instância global
servidor_repo = ServidorRepository()
