class Professor:
    def __init__(self, nome, siape, email=None, cpf=None, id=None):
        self.id = id
        self.nome = nome
        self.siape = siape
        self.email = email
        self.cpf = cpf

    def __repr__(self):
        return f"Professor(nome={self.nome!r}, siape={self.siape!r})"