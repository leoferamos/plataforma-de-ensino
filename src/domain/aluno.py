class Aluno:
    def __init__(self, nome, matricula, email=None, cpf=None, data_nascimento=None, turma_id=None, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.email = email
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.turma_id = turma_id