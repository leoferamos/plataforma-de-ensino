from infrastructure.professor_repository import ProfessorRepository
from domain.professor import Professor

class ProfessorService:
    def __init__(self):
        self.repo = ProfessorRepository()

    def cadastrar(self, nome, siape, email=None, cpf=None):
        professor = Professor(nome=nome, siape=siape)
        professor.email = email
        professor.cpf = cpf
        self.repo.adicionar(professor)
        return professor

    def listar(self):
        return self.repo.listar()

    def remover(self, professor_id):
        self.repo.remover(professor_id)

    def atualizar(self, professor_id, nome, siape, email=None, cpf=None):
        professor = Professor(nome=nome, siape=siape)
        professor.id = professor_id
        professor.email = email
        professor.cpf = cpf
        self.repo.atualizar(professor)
        return professor