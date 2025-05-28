from infrastructure.professor_repository import ProfessorRepository
from domain.professor import Professor

class ProfessorService:
    def __init__(self):
        self.repo = ProfessorRepository()

    def cpf_existe(self, cpf, ignorar_id=None):
        # Verifica em professores
        for professor in self.repo.listar():
            if professor.cpf == cpf and (ignorar_id is None or professor.id != ignorar_id):
                return True
        # Verifica em alunos
        from application.aluno_service import AlunoService
        for aluno in AlunoService().listar():
            if aluno.cpf == cpf:
                return True
        return False

    def cadastrar(self, nome, siape, email=None, cpf=None):
        if cpf and self.cpf_existe(cpf):
            raise ValueError("CPF já cadastrado para outro professor ou aluno.")
        professor = Professor(nome=nome, siape=siape, email=email, cpf=cpf)
        professor_id = self.repo.adicionar(professor)
        professor.id = professor_id
        return professor

    def listar(self):
        return self.repo.listar()

    def remover(self, professor_id):
        self.repo.remover(professor_id)

    def atualizar(self, professor_id, nome, siape, email=None, cpf=None):
        if cpf and self.cpf_existe(cpf, ignorar_id=professor_id):
            raise ValueError("CPF já cadastrado para outro professor ou aluno.")
        professor = Professor(nome=nome, siape=siape, email=email, cpf=cpf, id=professor_id)
        self.repo.atualizar(professor)
        return professor

    def associar_cursos(self, professor_id, cursos_ids):
        self.repo.associar_cursos(professor_id, cursos_ids)

    def get_cursos_ids(self, professor_id):
        return self.repo.get_cursos_ids(professor_id)