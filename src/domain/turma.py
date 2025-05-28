class Turma:
    def __init__(self, nome: str, codigo: str):
        self.nome = nome
        self.codigo = codigo

    def __repr__(self):
        return f"Turma(nome={self.nome!r}, codigo={self.codigo!r})"