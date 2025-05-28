from infrastructure.turma_repository import TurmaRepository
from domain.turma import Turma
import mysql.connector

class TurmaService:
    def __init__(self):
        self.repo = TurmaRepository()

    def cadastrar(self, nome, codigo, curso_id):
        turma = Turma(nome=nome, codigo=codigo, curso_id=curso_id)
        try:
            self.repo.adicionar(turma)
        except mysql.connector.errors.IntegrityError as e:
            if "Duplicate entry" in str(e) and "'turma.codigo'" in str(e):
                raise ValueError("Já existe uma turma com esse código!")
            raise

    def listar(self):
        return self.repo.listar()

    def remover(self, turma_id):
        try:
            self.repo.remover(turma_id)
        except mysql.connector.errors.IntegrityError as e:
            if "foreign key constraint fails" in str(e):
                raise ValueError("Não é possível excluir a turma: existem alunos vinculados a ela.")
            raise

    def atualizar(self, turma_id, nome, codigo, curso_id):
        turma = Turma(nome=nome, codigo=codigo, curso_id=curso_id, id=turma_id)
        try:
            self.repo.atualizar(turma)
        except mysql.connector.errors.IntegrityError as e:
            if "Duplicate entry" in str(e) and "'turma.codigo'" in str(e):
                raise ValueError("Já existe uma turma com esse código!")
            raise