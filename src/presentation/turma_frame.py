import customtkinter
from application.turma_service import TurmaService

class TurmaFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.service = TurmaService()
        self.turmas = self.service.listar()
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

        customtkinter.CTkLabel(form_frame, text="ID do Curso:").grid(row=0, column=4, padx=5, pady=5)
        self.curso_id_entry = customtkinter.CTkEntry(form_frame)
        self.curso_id_entry.grid(row=0, column=5, padx=5, pady=5)

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_turma)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_turma(self):
        nome = self.nome_entry.get()
        codigo = self.codigo_entry.get()
        curso_id = self.curso_id_entry.get()
        curso_id = int(curso_id) if curso_id.isdigit() else None
        if not nome or not codigo:
            return
        if self.editando_id is None:
            self.service.cadastrar(nome, codigo, curso_id)
        else:
            self.service.atualizar(self.editando_id, nome, codigo, curso_id)
            self.editando_id = None
            self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.codigo_entry.delete(0, "end")
        self.curso_id_entry.delete(0, "end")
        self.atualizar_lista()

    def editar_turma(self, turma_id):
        turma = next((t for t in self.turmas if getattr(t, "id", None) == turma_id), None)
        if turma:
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, turma.nome)
            self.codigo_entry.delete(0, "end")
            self.codigo_entry.insert(0, turma.codigo)
            self.curso_id_entry.delete(0, "end")
            self.curso_id_entry.insert(0, turma.curso_id if turma.curso_id is not None else "")
            self.editando_id = turma_id
            self.add_btn.configure(text="Salvar")

    def excluir_turma(self, turma_id):
        self.service.remover(turma_id)
        self.editando_id = None
        self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.codigo_entry.delete(0, "end")
        self.curso_id_entry.delete(0, "end")
        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        self.turmas = self.service.listar()
        if not self.turmas:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhuma turma cadastrada.").pack()
        else:
            for turma in self.turmas:
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                text = f"{turma.nome} (Código: {turma.codigo}, Curso ID: {turma.curso_id})"
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=turma.id: self.editar_turma(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=turma.id: self.excluir_turma(i))
                del_btn.pack(side="right", padx=5)