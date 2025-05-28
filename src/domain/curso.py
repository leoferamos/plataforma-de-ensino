class Curso:
    def __init__(self, nome, codigo, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo

    def __repr__(self):
        return f"Curso(nome={self.nome!r}, codigo={self.codigo!r})"