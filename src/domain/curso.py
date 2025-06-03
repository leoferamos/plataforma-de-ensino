class Curso:
    def __init__(self, nome, codigo, categoria=None, grau=None, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.categoria = categoria
        self.grau = grau

    def __repr__(self):
        return f"Curso(nome={self.nome!r}, codigo={self.codigo!r}, categoria={self.categoria!r}, grau={self.grau!r})"