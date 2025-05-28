from infrastructure.turma_repository import TurmaRepository
from domain.turma import Turma

class TurmaService:
    def __init__(self):
        self.repo = TurmaRepository()

    def cadastrar(self, nome, codigo, curso_id=None):
        turma = Turma(nome=nome, codigo=codigo)
        turma.curso_id = curso_id
        self.repo.adicionar(turma)
        return turma

    def listar(self):
        return self.repo.listar()

    def remover(self, turma_id):
        self.repo.remover(turma_id)

    def atualizar(self, turma_id, nome, codigo, curso_id=None):
        turma = Turma(nome=nome, codigo=codigo)
        turma.id = turma_id
        turma.curso_id = curso_id
        self.repo.atualizar(turma)
        return turma