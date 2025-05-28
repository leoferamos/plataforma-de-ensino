from infrastructure.aluno_repository import AlunoRepository
from domain.aluno import Aluno
import datetime
import re

class AlunoService:
    def __init__(self):
        self.repo = AlunoRepository()

    def cpf_existe(self, cpf, ignorar_id=None):
        # Verifica em alunos
        for aluno in self.repo.listar():
            if aluno.cpf == cpf and (ignorar_id is None or aluno.id != ignorar_id):
                return True
        # Verifica em professores
        from application.professor_service import ProfessorService
        for professor in ProfessorService().listar():
            if professor.cpf == cpf:
                return True
        return False

    def cadastrar(self, nome, matricula, email=None, cpf=None, data_nascimento=None, turma_id=None):
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Email inválido.")
        if cpf:
            cpf_numeros = ''.join(filter(str.isdigit, cpf))
            if len(cpf_numeros) != 11:
                raise ValueError("CPF deve ter exatamente 11 números.")
            if not cpf_numeros.isdigit():
                raise ValueError("CPF deve conter apenas números.")
        if cpf and self.cpf_existe(cpf):
            raise ValueError("CPF já cadastrado para outro aluno ou professor.")
        # Validação da data
        if data_nascimento:
            try:
                datetime.datetime.strptime(data_nascimento, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Data de nascimento inválida! Use o formato YYYY-MM-DD.")
        aluno = Aluno(nome=nome, matricula=matricula, email=email, cpf=cpf, data_nascimento=data_nascimento, turma_id=turma_id)
        self.repo.adicionar(aluno)
        return aluno

    def listar(self):
        return self.repo.listar()

    def remover(self, aluno_id):
        self.repo.remover(aluno_id)

    def atualizar(self, aluno_id, nome, matricula, email=None, cpf=None, data_nascimento=None):
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Email inválido.")
        if cpf:
            cpf_numeros = ''.join(filter(str.isdigit, cpf))
            if len(cpf_numeros) != 11:
                raise ValueError("CPF deve ter exatamente 11 números.")
            if not cpf_numeros.isdigit():
                raise ValueError("CPF deve conter apenas números.")
        if cpf and self.cpf_existe(cpf, ignorar_id=aluno_id):
            raise ValueError("CPF já cadastrado para outro aluno ou professor.")
        aluno = Aluno(nome=nome, matricula=matricula)
        aluno.id = aluno_id
        aluno.email = email
        aluno.cpf = cpf
        aluno.data_nascimento = data_nascimento
        self.repo.atualizar(aluno)
        return aluno

        self.curso_var.set(f"{turma.curso.nome} (ID: {turma.curso_id})" if turma.curso_id is not None else "")