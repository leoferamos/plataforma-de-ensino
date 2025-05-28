class Turma:
    def __init__(self, nome, codigo, curso_id=None, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.curso_id = curso_id

    def __repr__(self):
        return f"Turma(nome={self.nome!r}, codigo={self.codigo!r})"