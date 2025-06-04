import customtkinter
from shared.utils import montar_arvore_curso_turmas, matriz_adjacencias, gerar_texto_arvore, gerar_texto_matriz, gerar_imagem_arvore, gerar_imagem_matriz
from application.curso_service import CursoService
from application.turma_service import TurmaService
from application.curso_prerequisito_service import CursoPrerequisitoService
from PIL import Image

class RelatorioFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.curso_service = CursoService()
        self.turma_service = TurmaService()

        title = customtkinter.CTkLabel(self, text="Relatório de Estruturas de Dados", font=customtkinter.CTkFont(size=18, weight="bold"))
        title.pack(padx=20, pady=(20, 10))

        # Frame da Árvore
        arvore_frame = customtkinter.CTkFrame(self)
        arvore_frame.pack(padx=20, pady=(10, 10), fill="x")
        arvore_label = customtkinter.CTkLabel(arvore_frame, text="Árvore: Cursos e suas Turmas", font=customtkinter.CTkFont(size=15, weight="bold"))
        arvore_label.pack(anchor="w", pady=(0, 5))

        # Aumente o tamanho do campo de texto e da imagem
        self.arvore_text = customtkinter.CTkTextbox(arvore_frame, width=1200, height=350)
        self.arvore_text.pack(side="left", padx=(0, 10), pady=(0, 10), fill="both", expand=True)
        self.arvore_text.configure(state="normal")
        self.arvore_text.delete("1.0", "end")
        self.arvore_text.insert("end", self.gerar_texto_arvore())
        self.arvore_text.configure(state="disabled")

        self.gerar_imagem_arvore("arvore.png")
        arvore_img = customtkinter.CTkImage(Image.open("arvore.png"), size=(500, 350))
        arvore_img_label = customtkinter.CTkLabel(arvore_frame, image=arvore_img, text="")
        arvore_img_label.pack(side="left", padx=10, pady=(0, 10))

        # Frame da Matriz de Adjacências
        matriz_frame = customtkinter.CTkFrame(self)
        matriz_frame.pack(padx=20, pady=(10, 10), fill="x")
        matriz_label = customtkinter.CTkLabel(matriz_frame, text="Matriz de Adjacências: Prérequisitos entre Cursos", font=customtkinter.CTkFont(size=15, weight="bold"))
        matriz_label.pack(anchor="w", pady=(0, 5))

        # Aumente o tamanho do campo de texto e da imagem
        self.matriz_text = customtkinter.CTkTextbox(matriz_frame, width=1200, height=350)
        self.matriz_text.pack(side="left", padx=(0, 10), pady=(0, 10), fill="both", expand=True)
        self.matriz_text.configure(state="normal")
        self.matriz_text.delete("1.0", "end")
        self.matriz_text.insert("end", self.gerar_texto_matriz())
        self.matriz_text.configure(state="disabled")

        self.gerar_imagem_matriz("matriz_adjacencia.png")
        matriz_img = customtkinter.CTkImage(Image.open("matriz_adjacencia.png"), size=(500, 350))
        matriz_img_label = customtkinter.CTkLabel(matriz_frame, image=matriz_img, text="")
        matriz_img_label.pack(side="left", padx=10, pady=(0, 10))

        explicacao_label = customtkinter.CTkLabel(
            self,
            text=(
                "Este relatório demonstra o uso de estruturas de dados não-lineares no sistema:\n"
                "- Árvore: Cada curso é um nó raiz e suas turmas são filhos (hierarquia Curso → Turmas).\n"
                "- Matriz de Adjacências: Representa um grafo de pré-requisitos entre cursos."
            ),
            font=customtkinter.CTkFont(size=13),
            justify="left",
            wraplength=900
        )
        explicacao_label.pack(padx=20, pady=(0, 10), anchor="w")

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

    def gerar_imagem_arvore(self, img_path="arvore.png"):
        cursos = self.curso_service.listar()
        turmas = self.turma_service.listar()
        from shared.utils import gerar_imagem_arvore
        gerar_imagem_arvore(cursos, turmas, img_path)

    def gerar_imagem_matriz(self, img_path="matriz_adjacencia.png"):
        cursos = self.curso_service.listar()
        prerequisitos = CursoPrerequisitoService().listar()
        from shared.utils import gerar_imagem_matriz
        gerar_imagem_matriz(cursos, prerequisitos, img_path)