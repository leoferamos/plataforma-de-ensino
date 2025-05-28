import customtkinter
import tkinter.messagebox
import re
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

        customtkinter.CTkLabel(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = customtkinter.CTkEntry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="CPF:").grid(row=1, column=2, padx=5, pady=5)
        self.cpf_entry = customtkinter.CTkEntry(form_frame)
        self.cpf_entry.grid(row=1, column=3, padx=5, pady=5)

        # Label para cursos
        customtkinter.CTkLabel(form_frame, text="Cursos:").grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        # Frame rolável para os cursos
        self.cursos_scroll = customtkinter.CTkScrollableFrame(form_frame, width=350, height=60)
        self.cursos_scroll.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        self.curso_vars = []
        for i, curso in enumerate(self.cursos):
            var = customtkinter.BooleanVar()
            chk = customtkinter.CTkCheckBox(self.cursos_scroll, text=f"{curso.nome} (ID: {curso.id})", variable=var)
            chk.grid(row=i // 3, column=i % 3, padx=2, pady=2, sticky="w")
            self.curso_vars.append((curso.id, var))

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_professor)
        self.add_btn.grid(row=0, column=4, padx=10, pady=5)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def adicionar_ou_salvar_professor(self):
        nome = self.nome_entry.get()
        siape = self.siape_entry.get()
        email = self.email_entry.get()
        cpf = self.cpf_entry.get()
        # Validação de CPF na interface
        if cpf:
            cpf_numeros = ''.join(filter(str.isdigit, cpf))
            if len(cpf_numeros) != 11:
                tkinter.messagebox.showerror("Erro", "CPF deve ter exatamente 11 números.")
                return
            if not cpf_numeros.isdigit():
                tkinter.messagebox.showerror("Erro", "CPF deve conter apenas números.")
                return
        # Validação de email
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                tkinter.messagebox.showerror("Erro", "Email inválido.")
                return
        cursos_ids = [cid for cid, var in self.curso_vars if var.get()]
        try:
            if self.editando_id is None:
                prof = self.service.cadastrar(nome, siape, email, cpf)
                self.service.associar_cursos(prof.id, cursos_ids)
            else:
                self.service.atualizar(self.editando_id, nome, siape, email, cpf)
                self.service.associar_cursos(self.editando_id, cursos_ids)
                self.editando_id = None
                self.add_btn.configure(text="Adicionar")
        except ValueError as e:
            tkinter.messagebox.showerror("Erro", str(e))
            return
        self.nome_entry.delete(0, "end")
        self.siape_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.cpf_entry.delete(0, "end")
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
            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, professor.email or "")
            self.cpf_entry.delete(0, "end")
            self.cpf_entry.insert(0, professor.cpf or "")
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
        self.cursos = self.curso_service.listar()
        for professor in self.professores:
            # Buscar cursos associados a este professor
            cursos_ids = self.service.get_cursos_ids(professor.id)  # Você vai criar esse método
            cursos_nomes = [c.nome for c in self.cursos if c.id in cursos_ids]
            cursos_str = ", ".join(cursos_nomes) if cursos_nomes else "Nenhum curso"
            text = (
                f"{professor.nome} (SIAPE: {professor.siape})"
                f" | Email: {professor.email or '-'}"
                f" | CPF: {professor.cpf or '-'}"
                f" - Cursos: {cursos_str}"
            )
            row_frame = customtkinter.CTkFrame(self.lista_frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
            edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                               command=lambda i=professor.id: self.editar_professor(i))
            edit_btn.pack(side="right", padx=5)
            del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                              command=lambda i=professor.id: self.excluir_professor(i))
            del_btn.pack(side="right", padx=5)