import customtkinter
from application.curso_service import CursoService
from application.curso_prerequisito_service import CursoPrerequisitoService
import tkinter.messagebox

GRAUS = ["Bacharelado", "Mestrado", "Doutorado"]
CATEGORIAS = [
    "Tecnologia",
    "Saúde",
    "Humanas",
    "Exatas",
    "Biológicas",
    "Engenharias",
    "Artes",
    "Direito",
    "Educação",
    "Negócios"
]

class CursoFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.service = CursoService()
        self.prereq_service = CursoPrerequisitoService()
        self.cursos = self.service.listar()
        self.editando_id = None

        label = customtkinter.CTkLabel(self, text="Gestão de Cursos", font=customtkinter.CTkFont(size=18, weight="bold"))
        label.pack(padx=20, pady=(20, 10))

        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="x")

        customtkinter.CTkLabel(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = customtkinter.CTkEntry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Código:").grid(row=0, column=2, padx=5, pady=5)
        self.codigo_entry = customtkinter.CTkEntry(form_frame)
        self.codigo_entry.grid(row=0, column=3, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Categoria:").grid(row=0, column=4, padx=5, pady=5)
        self.categoria_var = customtkinter.StringVar(value=CATEGORIAS[0])
        self.categoria_combo = customtkinter.CTkOptionMenu(
            form_frame, variable=self.categoria_var, values=CATEGORIAS, command=self.atualizar_prerequisitos
        )
        self.categoria_combo.grid(row=0, column=5, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Grau:").grid(row=0, column=7, padx=5, pady=5)
        self.grau_var = customtkinter.StringVar(value=GRAUS[0])
        self.grau_menu = customtkinter.CTkOptionMenu(form_frame, variable=self.grau_var, values=GRAUS, command=self.atualizar_prerequisitos)
        self.grau_menu.grid(row=0, column=8, padx=5, pady=5)

        # Pré-requisitos (checkboxes dinâmicos)
        customtkinter.CTkLabel(form_frame, text="Pré-requisitos:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.prereq_vars = {}
        self.prereq_checks = []
        self.prereq_frame = customtkinter.CTkFrame(form_frame)
        self.prereq_frame.grid(row=1, column=1, columnspan=8, sticky="w")
        self.atualizar_prerequisitos()

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_curso)
        self.add_btn.grid(row=2, column=0, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def obter_categorias_existentes(self):
        cursos = self.service.listar()
        categorias = sorted(set(c.categoria for c in cursos if c.categoria))
        return categorias

    def atualizar_prerequisitos(self, *args):
        # Limpa checkboxes antigos
        for chk in getattr(self, "prereq_checks", []):
            chk.destroy()
        self.prereq_vars = {}
        self.prereq_checks = []

        categoria = self.categoria_var.get()
        grau = self.grau_var.get()
        self.cursos = self.service.listar()
        if grau == "Mestrado":
            prereq_cursos = [c for c in self.cursos if c.grau == "Bacharelado" and c.categoria == categoria]
        elif grau == "Doutorado":
            prereq_cursos = [c for c in self.cursos if c.grau == "Mestrado" and c.categoria == categoria]
        else:
            prereq_cursos = []

        for i, curso in enumerate(prereq_cursos):
            var = customtkinter.BooleanVar()
            chk = customtkinter.CTkCheckBox(self.prereq_frame, text=f"{curso.nome} (ID: {curso.id})", variable=var)
            chk.grid(row=0, column=i, padx=2, pady=2, sticky="w")
            self.prereq_vars[curso.id] = var
            self.prereq_checks.append(chk)

    def adicionar_ou_salvar_curso(self):
        nome = self.nome_entry.get()
        codigo = self.codigo_entry.get()
        categoria = self.categoria_var.get()
        grau = self.grau_var.get()
        prerequisitos = [cid for cid, var in self.prereq_vars.items() if var.get()]
        if not nome or not codigo or not categoria or not grau:
            tkinter.messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        if self.editando_id is None:
            curso = self.service.cadastrar(nome, codigo, categoria, grau)
            for prereq_id in prerequisitos:
                self.prereq_service.adicionar(curso.id, prereq_id)
        else:
            self.service.atualizar(self.editando_id, nome, codigo, categoria, grau)
            self.prereq_service.remover_todos(self.editando_id)
            for prereq_id in prerequisitos:
                self.prereq_service.adicionar(self.editando_id, prereq_id)
            self.editando_id = None
            self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.codigo_entry.delete(0, "end")
        self.grau_var.set(GRAUS[0])
        self.categoria_var.set(CATEGORIAS[0])
        self.atualizar_prerequisitos()
        self.atualizar_lista()

    def editar_curso(self, curso_id):
        curso = next((c for c in self.cursos if getattr(c, "id", None) == curso_id), None)
        if curso:
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, curso.nome)
            self.codigo_entry.delete(0, "end")
            self.codigo_entry.insert(0, curso.codigo)
            self.categoria_var.set(getattr(curso, "categoria", CATEGORIAS[0]))
            self.grau_var.set(getattr(curso, "grau", GRAUS[0]))
            self.editando_id = curso_id
            self.add_btn.configure(text="Salvar")
            self.atualizar_prerequisitos()

    def excluir_curso(self, curso_id):
        try:
            self.service.remover(curso_id)
            self.editando_id = None
            self.add_btn.configure(text="Adicionar")
            self.nome_entry.delete(0, "end")
            self.codigo_entry.delete(0, "end")
            self.grau_var.set(GRAUS[0])
            self.categoria_var.set(CATEGORIAS[0])
            self.atualizar_prerequisitos()
            self.atualizar_lista()
        except ValueError as e:
            tkinter.messagebox.showerror("Erro", str(e))

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        self.cursos = self.service.listar()
        if not self.cursos:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhum curso cadastrado.").pack()
        else:
            for curso in self.cursos:
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                text = f"{curso.nome} (Código: {curso.codigo}) - Categoria: {getattr(curso, 'categoria', '')} - Grau: {getattr(curso, 'grau', '')}"
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=curso.id: self.editar_curso(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=curso.id: self.excluir_curso(i))
                del_btn.pack(side="right", padx=5)