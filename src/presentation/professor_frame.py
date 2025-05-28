import customtkinter
from application.professor_service import ProfessorService
from application.curso_service import CursoService

class ProfessorFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.service = ProfessorService()
        self.curso_service = CursoService()
        self.professores = self.service.listar()
        self.cursos = self.curso_service.listar()
        self.editando_id = None

        label = customtkinter.CTkLabel(self, text="Gestão de Professores", font=customtkinter.CTkFont(size=18, weight="bold"))
        label.pack(padx=20, pady=(20, 10))

        form_frame = customtkinter.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="x")

        customtkinter.CTkLabel(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = customtkinter.CTkEntry(form_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="SIAPE:").grid(row=0, column=2, padx=5, pady=5)
        self.siape_entry = customtkinter.CTkEntry(form_frame)
        self.siape_entry.grid(row=0, column=3, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Cursos:").grid(row=1, column=0, padx=5, pady=5)
        self.curso_vars = []
        for i, curso in enumerate(self.cursos):
            var = customtkinter.BooleanVar()
            chk = customtkinter.CTkCheckBox(form_frame, text=f"{curso.nome} (ID: {curso.id})", variable=var)
            chk.grid(row=1, column=1+i, padx=2, pady=5)
            self.curso_vars.append((curso.id, var))

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_professor)
        self.add_btn.grid(row=0, column=4, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_professor(self):
        nome = self.nome_entry.get()
        siape = self.siape_entry.get()
        if not nome or not siape:
            return
        cursos_ids = [cid for cid, var in self.curso_vars if var.get()]
        if self.editando_id is None:
            prof = self.service.cadastrar(nome, siape)
            self.service.associar_cursos(prof.id, cursos_ids)
        else:
            self.service.atualizar(self.editando_id, nome, siape)
            self.service.associar_cursos(self.editando_id, cursos_ids)
            self.editando_id = None
            self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.siape_entry.delete(0, "end")
        for _, var in self.curso_vars:
            var.set(False)
        self.atualizar_lista()

    def editar_professor(self, professor_id):
        professor = next((p for p in self.professores if getattr(p, "id", None) == professor_id), None)
        if professor:
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, professor.nome)
            self.siape_entry.delete(0, "end")
            self.siape_entry.insert(0, professor.siape)
            self.editando_id = professor_id
            self.add_btn.configure(text="Salvar")

    def excluir_professor(self, professor_id):
        self.service.remover(professor_id)
        self.editando_id = None
        self.add_btn.configure(text="Adicionar")
        self.nome_entry.delete(0, "end")
        self.siape_entry.delete(0, "end")
        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()
        self.professores = self.service.listar()
        if not self.professores:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhum professor cadastrado.").pack()
        else:
            for professor in self.professores:
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                text = f"{professor.nome} (SIAPE: {professor.siape})"
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=professor.id: self.editar_professor(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=professor.id: self.excluir_professor(i))
                del_btn.pack(side="right", padx=5)