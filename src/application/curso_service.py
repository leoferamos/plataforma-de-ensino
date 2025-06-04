from infrastructure.curso_repository import CursoRepository
from domain.curso import Curso
import mysql.connector

class CursoService:
    def __init__(self):
        self.repo = CursoRepository()

    def cadastrar(self, nome, codigo, categoria, grau):
        curso = Curso(nome=nome, codigo=codigo, categoria=categoria, grau=grau)
        curso.id = self.repo.adicionar(curso) 
        return curso

    def listar(self):
        return self.repo.listar()

    def remover(self, curso_id):
        try:
            self.repo.remover(curso_id)
        except mysql.connector.errors.IntegrityError as e:
            if "foreign key constraint fails" in str(e):
                raise ValueError("Não é possível excluir o curso: existem vínculos com turmas, professores ou pré-requisitos.")
            raise

    def atualizar(self, curso_id, nome, codigo, categoria, grau):
        curso = Curso(nome=nome, codigo=codigo, categoria=categoria, grau=grau, id=curso_id)
        self.repo.atualizar(curso)
        return curso