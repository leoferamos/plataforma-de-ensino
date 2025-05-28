import customtkinter
from application.aluno_service import AlunoService
from application.turma_service import TurmaService

class AlunoFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.service = AlunoService()
        self.turma_service = TurmaService()
        self.alunos = self.service.listar()
        self.turmas = self.turma_service.listar()
        self.editando_id = None

        label = customtkinter.CTkLabel(self, text="Gestão de Alunos", font=customtkinter.CTkFont(size=18, weight="bold"))
        label.pack(padx=20, pady=(20, 10))

        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="x")

        customtkinter.CTkLabel(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = customtkinter.CTkEntry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Matrícula:").grid(row=0, column=2, padx=5, pady=5)
        self.matricula_entry = customtkinter.CTkEntry(form_frame)
        self.matricula_entry.grid(row=0, column=3, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Turma:").grid(row=0, column=4, padx=5, pady=5)
        self.turma_var = customtkinter.StringVar()
        turma_nomes = [f"{t.nome} (ID: {t.id})" for t in self.turmas]
        self.turma_dropdown = customtkinter.CTkOptionMenu(form_frame, variable=self.turma_var, values=turma_nomes)
        self.turma_dropdown.grid(row=0, column=5, padx=5, pady=5)

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_aluno)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_aluno(self):
        nome = self.nome_entry.get()
        matricula = self.matricula_entry.get()
        turma_nome = self.turma_var.get()
        turma_id = None
        for t in self.turmas:
            if f"{t.nome} (ID: {t.id})" == turma_nome:
                turma_id = t.id
        if not nome or not matricula or not turma_id:
            return
        if self.editando_id is None:
            self.service.cadastrar(nome, matricula, turma_id=turma_id)
        else:
            self.service.atualizar(self.editando_id, nome, matricula, turma_id=turma_id)
            self.editando_id = None
            self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.turma_var.set("")
        self.atualizar_lista()

    def editar_aluno(self, aluno_id):
        aluno = next((a for a in self.alunos if getattr(a, "id", None) == aluno_id), None)
        if aluno:
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, aluno.nome)
            self.matricula_entry.delete(0, "end")
            self.matricula_entry.insert(0, aluno.matricula)
            turma_nome = f"{aluno.turma.nome} (ID: {aluno.turma.id})" if aluno.turma else ""
            self.turma_var.set(turma_nome)
            self.editando_id = aluno_id
            self.add_btn.configure(text="Salvar")

    def excluir_aluno(self, aluno_id):
        self.service.remover(aluno_id)
        self.editando_id = None
        self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.turma_var.set("")
        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        self.alunos = self.service.listar()
        if not self.alunos:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhum aluno cadastrado.").pack()
        else:
            for aluno in self.alunos:
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                turma_info = f" - Turma: {aluno.turma.nome} (ID: {aluno.turma.id})" if aluno.turma else ""
                text = f"{aluno.nome} (Matrícula: {aluno.matricula}){turma_info}"
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=aluno.id: self.editar_aluno(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=aluno.id: self.excluir_aluno(i))
                del_btn.pack(side="right", padx=5)