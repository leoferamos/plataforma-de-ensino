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

        self.arvore_text = customtkinter.CTkTextbox(arvore_frame, width=700, height=250)
        self.arvore_text.pack(side="left", padx=(0, 10), pady=(0, 10), fill="both", expand=True)
        self.arvore_text.configure(state="normal")
        self.arvore_text.delete("1.0", "end")
        self.arvore_text.insert("end", self.gerar_texto_arvore())
        self.arvore_text.configure(state="disabled")

        # Centraliza o botão usando um frame auxiliar
        arvore_btn_frame = customtkinter.CTkFrame(arvore_frame, fg_color="transparent")
        arvore_btn_frame.pack(side="left", fill="y", expand=True)
        arvore_btn = customtkinter.CTkButton(arvore_btn_frame, text="Gerar Visualmente", command=self.abrir_arvore_grande)
        arvore_btn.pack(pady=(80, 0), anchor="center")

        # Frame da Matriz de Adjacências
        matriz_frame = customtkinter.CTkFrame(self)
        matriz_frame.pack(padx=20, pady=(10, 10), fill="x")
        matriz_label = customtkinter.CTkLabel(matriz_frame, text="Matriz de Adjacências: Prérequisitos entre Cursos", font=customtkinter.CTkFont(size=15, weight="bold"))
        matriz_label.pack(anchor="w", pady=(0, 5))

        self.matriz_text = customtkinter.CTkTextbox(matriz_frame, width=700, height=250)
        self.matriz_text.pack(side="left", padx=(0, 10), pady=(0, 10), fill="both", expand=True)
        self.matriz_text.configure(state="normal")
        self.matriz_text.delete("1.0", "end")
        self.matriz_text.insert("end", self.gerar_texto_matriz())
        self.matriz_text.configure(state="disabled")

        matriz_btn_frame = customtkinter.CTkFrame(matriz_frame, fg_color="transparent")
        matriz_btn_frame.pack(side="left", fill="y", expand=True)
        matriz_btn = customtkinter.CTkButton(matriz_btn_frame, text="Gerar Visualmente", command=self.abrir_matriz_grande)
        matriz_btn.pack(pady=(80, 0), anchor="center")

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

    def abrir_arvore_grande(self):
        self.gerar_imagem_arvore("arvore_grande.png")
        self._abrir_imagem_modal("arvore_grande.png", "Árvore: Cursos e Turmas")

    def abrir_matriz_grande(self):
        self.gerar_imagem_matriz("matriz_grande.png")
        self._abrir_imagem_modal("matriz_grande.png", "Matriz de Adjacência de Pré-requisitos")

    def _abrir_imagem_modal(self, img_path, titulo):
        modal = customtkinter.CTkToplevel(self)
        modal.title(titulo)
        modal.geometry("900x700")
        modal.attributes("-alpha", 0.0)  # Começa transparente

        img = customtkinter.CTkImage(Image.open(img_path), size=(850, 650))
        img_label = customtkinter.CTkLabel(modal, image=img, text="")
        img_label.pack(expand=True, fill="both", padx=20, pady=20)

        # Fade-in
        self._fade_in(modal)

        # Botão de fechar centralizado
        close_btn = customtkinter.CTkButton(modal, text="Fechar", command=lambda: self._fade_out(modal))
        close_btn.pack(pady=10)

    def _fade_in(self, window, alpha=0.0):
        alpha = round(alpha + 0.05, 2)
        if alpha >= 1.0:
            window.attributes("-alpha", 1.0)
        else:
            window.attributes("-alpha", alpha)
            window.after(15, lambda: self._fade_in(window, alpha))

    def _fade_out(self, window, alpha=None):
        if alpha is None:
            alpha = window.attributes("-alpha")
        alpha = round(float(alpha) - 0.05, 2)
        if alpha <= 0.0:
            window.destroy()
        else:
            window.attributes("-alpha", alpha)
            window.after(15, lambda: self._fade_out(window, alpha))

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