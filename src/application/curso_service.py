from infrastructure.curso_repository import CursoRepository
from domain.curso import Curso

class CursoService:
    def __init__(self):
        self.repo = CursoRepository()

    def cadastrar(self, nome, codigo):
        curso = Curso(nome=nome, codigo=codigo)
        self.repo.adicionar(curso)
        return curso

    def listar(self):
        return self.repo.listar()

    def remover(self, curso_id):
        self.repo.remover(curso_id)

    def atualizar(self, curso_id, nome, codigo):
        curso = Curso(nome=nome, codigo=codigo)
        curso.id = curso_id
        self.repo.atualizar(curso)
        return curso