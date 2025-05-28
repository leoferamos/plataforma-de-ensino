import customtkinter
import tkinter.messagebox
from application.turma_service import TurmaService
from application.curso_service import CursoService

class TurmaFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.service = TurmaService()
        self.curso_service = CursoService()
        self.turmas = self.service.listar()
        self.cursos = self.curso_service.listar()
        self.editando_id = None

        label = customtkinter.CTkLabel(self, text="Gestão de Turmas", font=customtkinter.CTkFont(size=18, weight="bold"))
        label.pack(padx=20, pady=(20, 10))

        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="x")

        customtkinter.CTkLabel(form_frame, text="Nome da Turma:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = customtkinter.CTkEntry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Código:").grid(row=0, column=2, padx=5, pady=5)
        self.codigo_entry = customtkinter.CTkEntry(form_frame)
        self.codigo_entry.grid(row=0, column=3, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Curso:").grid(row=0, column=4, padx=5, pady=5)
        self.curso_var = customtkinter.StringVar()
        curso_nomes = [f"{c.nome} (ID: {c.id})" for c in self.cursos]
        self.curso_dropdown = customtkinter.CTkOptionMenu(form_frame, variable=self.curso_var, values=curso_nomes)
        self.curso_dropdown.grid(row=0, column=5, padx=5, pady=5)

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_turma)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_turma(self):
        nome = self.nome_entry.get()
        codigo = self.codigo_entry.get()
        curso_nome = self.curso_var.get()
        curso_id = None
        for c in self.cursos:
            if f"{c.nome} (ID: {c.id})" == curso_nome:
                curso_id = c.id
        if not nome or not codigo or not curso_id:
            return
        try:
            if self.editando_id is None:
                self.service.cadastrar(nome, codigo, curso_id)
            else:
                self.service.atualizar(self.editando_id, nome, codigo, curso_id)
                self.editando_id = None
                self.add_btn.configure(text="Adicionar")
            self.nome_entry.delete(0, "end")
            self.codigo_entry.delete(0, "end")
            self.atualizar_lista()
        except ValueError as e:
            tkinter.messagebox.showerror("Erro", str(e))

    def editar_turma(self, turma_id):
        turma = next((t for t in self.turmas if getattr(t, "id", None) == turma_id), None)
        if turma:
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, turma.nome)
            self.codigo_entry.delete(0, "end")
            self.codigo_entry.insert(0, turma.codigo)
            curso_nome = ""
            if turma.curso_id is not None:
                curso = next((c for c in self.cursos if c.id == turma.curso_id), None)
                if curso:
                    curso_nome = f"{curso.nome} (ID: {curso.id})"
            self.curso_var.set(curso_nome)
            self.editando_id = turma_id
            self.add_btn.configure(text="Salvar")

    def excluir_turma(self, turma_id):
        try:
            self.service.remover(turma_id)
            self.editando_id = None
            self.add_btn.configure(text="Adicionar")
            self.nome_entry.delete(0, "end")
            self.codigo_entry.delete(0, "end")
            self.atualizar_lista()
        except ValueError as e:
            tkinter.messagebox.showerror("Erro", str(e))

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        self.turmas = self.service.listar()
        self.cursos = self.curso_service.listar()
        if not self.turmas:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhuma turma cadastrada.").pack()
        else:
            for turma in self.turmas:
                curso_nome = ""
                if turma.curso_id is not None:
                    curso = next((c for c in self.cursos if c.id == turma.curso_id), None)
                    if curso:
                        curso_nome = f"{curso.nome} (ID: {curso.id})"
                self.curso_var.set(curso_nome)
                text = f"{turma.nome} (Código: {turma.codigo}){curso_nome}"
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=turma.id: self.editar_turma(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=turma.id: self.excluir_turma(i))
                del_btn.pack(side="right", padx=5)