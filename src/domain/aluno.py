class Aluno:
    def __init__(self, nome: str, matricula: str, turma_id: int = None):
        self.nome = nome
        self.matricula = matricula
        self.turma_id = turma_id

    def __repr__(self):
        return f"Aluno(nome={self.nome!r}, matricula={self.matricula!r}, turma_id={self.turma_id!r})"