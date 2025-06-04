from infrastructure.curso_prerequisito_repository import CursoPrerequisitoRepository

class CursoPrerequisitoService:
    def __init__(self):
        self.repo = CursoPrerequisitoRepository()

    def listar(self):
        return self.repo.listar()

    def adicionar(self, curso_id, prerequisito_id):
        self.repo.adicionar(curso_id, prerequisito_id)

    def remover_todos(self, curso_id):
        self.repo.remover_todos(curso_id)

    def remover_todos_como_prerequisito(self, prereq_id):
        self.repo.remover_todos_como_prerequisito(prereq_id)