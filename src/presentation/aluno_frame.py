import customtkinter

class AlunoFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.alunos = []
        self.editando_idx = None

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

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_aluno)
        self.add_btn.grid(row=0, column=4, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_aluno(self):
        nome = self.nome_entry.get()
        matricula = self.matricula_entry.get()
        if not nome or not matricula:
            return
        if self.editando_idx is None:
            self.alunos.append({"nome": nome, "matricula": matricula})
        else:
            self.alunos[self.editando_idx] = {"nome": nome, "matricula": matricula}
            self.editando_idx = None
            self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.atualizar_lista()

    def editar_aluno(self, idx):
        aluno = self.alunos[idx]
        self.nome_entry.delete(0, "end")
        self.nome_entry.insert(0, aluno["nome"])
        self.matricula_entry.delete(0, "end")
        self.matricula_entry.insert(0, aluno["matricula"])
        self.editando_idx = idx
        self.add_btn.configure(text="Salvar")

    def excluir_aluno(self, idx):
        del self.alunos[idx]
        self.editando_idx = None
        self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        if not self.alunos:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhum aluno cadastrado.").pack()
        else:
            for idx, aluno in enumerate(self.alunos):
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                text = f"{aluno['nome']} (Matrícula: {aluno['matricula']})"
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=idx: self.editar_aluno(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=idx: self.excluir_aluno(i))
                del_btn.pack(side="right", padx=5)