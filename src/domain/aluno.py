class Aluno:
    def __init__(self, nome: str, matricula: str):
        self.nome = nome
        self.matricula = matricula

    def __repr__(self):
        return f"Aluno(nome={self.nome!r}, matricula={self.matricula!r})"