from infrastructure.professor_repository import ProfessorRepository
from domain.professor import Professor

class ProfessorService:
    def __init__(self):
        self.repo = ProfessorRepository()

    def cadastrar(self, nome, siape, email=None, cpf=None):
        professor = Professor(nome=nome, siape=siape)
        professor.email = email
        professor.cpf = cpf
        professor_id = self.repo.adicionar(professor)
        professor.id = professor_id  # <-- seta o id no objeto
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

    def associar_cursos(self, professor_id, cursos_ids):
        self.repo.associar_cursos(professor_id, cursos_ids)

    def get_cursos_ids(self, professor_id):
        return self.repo.get_cursos_ids(professor_id)