import customtkinter

class CursoFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.cursos = []
        self.editando_idx = None

        label = customtkinter.CTkLabel(self, text="Gestão de Cursos", font=customtkinter.CTkFont(size=18, weight="bold"))
        label.pack(padx=20, pady=(20, 10))

        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="x")

        customtkinter.CTkLabel(form_frame, text="Nome do Curso:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = customtkinter.CTkEntry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Código:").grid(row=0, column=2, padx=5, pady=5)
        self.codigo_entry = customtkinter.CTkEntry(form_frame)
        self.codigo_entry.grid(row=0, column=3, padx=5, pady=5)

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_curso)
        self.add_btn.grid(row=0, column=4, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_curso(self):
        nome = self.nome_entry.get()
        codigo = self.codigo_entry.get()
        if not nome or not codigo:
            return
        if self.editando_idx is None:
            self.cursos.append({"nome": nome, "codigo": codigo})
        else:
            self.cursos[self.editando_idx] = {"nome": nome, "codigo": codigo}
            self.editando_idx = None
            self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.codigo_entry.delete(0, "end")
        self.atualizar_lista()

    def editar_curso(self, idx):
        curso = self.cursos[idx]
        self.nome_entry.delete(0, "end")
        self.nome_entry.insert(0, curso["nome"])
        self.codigo_entry.delete(0, "end")
        self.codigo_entry.insert(0, curso["codigo"])
        self.editando_idx = idx
        self.add_btn.configure(text="Salvar")

    def excluir_curso(self, idx):
        del self.cursos[idx]
        self.editando_idx = None
        self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.codigo_entry.delete(0, "end")
        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        if not self.cursos:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhum curso cadastrado.").pack()
        else:
            for idx, curso in enumerate(self.cursos):
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                text = f"{curso['nome']} (Código: {curso['codigo']})"
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=idx: self.editar_curso(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=idx: self.excluir_curso(i))
                del_btn.pack(side="right", padx=5)