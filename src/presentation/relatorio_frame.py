import customtkinter
from shared.utils import montar_arvore_curso_turmas, matriz_adjacencias, gerar_texto_arvore, gerar_texto_matriz
from application.curso_service import CursoService
from application.turma_service import TurmaService
from application.curso_prerequisito_service import CursoPrerequisitoService
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image

class RelatorioFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.curso_service = CursoService()
        self.turma_service = TurmaService()

        title = customtkinter.CTkLabel(self, text="Relatório de Estruturas de Dados", font=customtkinter.CTkFont(size=18, weight="bold"))
        title.pack(padx=20, pady=(20, 10))

        # Árvore Curso -> Turmas
        arvore_label = customtkinter.CTkLabel(self, text="Árvore: Cursos e suas Turmas", font=customtkinter.CTkFont(size=15, weight="bold"))
        arvore_label.pack(padx=20, pady=(10, 2), anchor="w")

        self.arvore_text = customtkinter.CTkTextbox(self, width=600, height=150)
        self.arvore_text.pack(padx=20, pady=(0, 10), fill="x")
        self.arvore_text.configure(state="normal")
        self.arvore_text.delete("1.0", "end")
        self.arvore_text.insert("end", self.gerar_texto_arvore())
        self.arvore_text.configure(state="disabled")

        # Matriz de Adjacências
        matriz_label = customtkinter.CTkLabel(self, text="Matriz de Adjacências: Prérequisitos entre Cursos", font=customtkinter.CTkFont(size=15, weight="bold"))
        matriz_label.pack(padx=20, pady=(10, 2), anchor="w")

        self.matriz_text = customtkinter.CTkTextbox(self, width=600, height=150)
        self.matriz_text.pack(padx=20, pady=(0, 10), fill="x")
        self.matriz_text.configure(state="normal")
        self.matriz_text.delete("1.0", "end")
        self.matriz_text.insert("end", self.gerar_texto_matriz())
        self.matriz_text.configure(state="disabled")

        explicacao_label = customtkinter.CTkLabel(
            self,
            text=(
                "Este relatório demonstra o uso de estruturas de dados não-lineares no sistema:\n"
                "- Árvore: Cada curso é um nó raiz e suas turmas são filhos (hierarquia Curso → Turmas).\n"
                "- Matriz de Adjacências: Representa um grafo de pré-requisitos entre cursos."
            ),
            font=customtkinter.CTkFont(size=13),
            justify="left",
            wraplength=600
        )
        explicacao_label.pack(padx=20, pady=(0, 10), anchor="w")

        self.atualizar_relatorio()

        self.gerar_grafo_cursos("grafo_cursos.png")
        img = customtkinter.CTkImage(Image.open("grafo_cursos.png"), size=(400, 240))
        img_label = customtkinter.CTkLabel(self, image=img, text="")
        img_label.pack(padx=20, pady=10)

    def atualizar_relatorio(self):
        self.arvore_text.configure(state="normal")
        self.arvore_text.delete("1.0", "end")
        self.arvore_text.insert("end", self.gerar_texto_arvore())
        self.arvore_text.configure(state="disabled")

        self.matriz_text.configure(state="normal")
        self.matriz_text.delete("1.0", "end")
        self.matriz_text.insert("end", self.gerar_texto_matriz())
        self.matriz_text.configure(state="disabled")

    def gerar_texto_arvore(self):
        cursos = self.curso_service.listar()
        turmas = self.turma_service.listar()
        arvore = montar_arvore_curso_turmas(cursos, turmas)
        return gerar_texto_arvore(arvore)

    def gerar_texto_matriz(self):
        cursos = self.curso_service.listar()
        prerequisitos = CursoPrerequisitoService().listar()
        matriz = matriz_adjacencias(cursos, prerequisitos)
        return gerar_texto_matriz(matriz, cursos)

    def gerar_grafo_cursos(self, img_path="grafo_cursos.png"):
        cursos = self.curso_service.listar()
        prerequisitos = CursoPrerequisitoService().listar()
        from shared.utils import gerar_grafo_cursos
        gerar_grafo_cursos(cursos, prerequisitos, img_path)