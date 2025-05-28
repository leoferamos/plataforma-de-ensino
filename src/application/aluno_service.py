from infrastructure.aluno_repository import AlunoRepository
from domain.aluno import Aluno

class AlunoService:
    def __init__(self):
        self.repo = AlunoRepository()

    def cadastrar(self, nome, matricula, email=None, cpf=None, data_nascimento=None, turma_id=None):
        aluno = Aluno(nome=nome, matricula=matricula, turma_id=turma_id)
        aluno.email = email
        aluno.cpf = cpf
        aluno.data_nascimento = data_nascimento
        self.repo.adicionar(aluno)
        return aluno

    def listar(self):
        return self.repo.listar()

    def remover(self, aluno_id):
        self.repo.remover(aluno_id)

    def atualizar(self, aluno_id, nome, matricula, email=None, cpf=None, data_nascimento=None):
        aluno = Aluno(nome=nome, matricula=matricula)
        aluno.id = aluno_id
        aluno.email = email
        aluno.cpf = cpf
        aluno.data_nascimento = data_nascimento
        self.repo.atualizar(aluno)
        return aluno