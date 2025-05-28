class Professor:
    def __init__(self, nome: str, siape: str):
        self.nome = nome
        self.siape = siape

    def __repr__(self):
        return f"Professor(nome={self.nome!r}, siape={self.siape!r})"