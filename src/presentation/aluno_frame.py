import customtkinter
from application.aluno_service import AlunoService
from application.turma_service import TurmaService
import datetime
import tkinter.messagebox
import tkinter as tk
import re

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

        customtkinter.CTkLabel(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = customtkinter.CTkEntry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="CPF:").grid(row=1, column=2, padx=5, pady=5)
        self.cpf_entry = customtkinter.CTkEntry(form_frame)
        self.cpf_entry.grid(row=1, column=3, padx=5, pady=5)

        customtkinter.CTkLabel(form_frame, text="Data Nasc.:").grid(row=1, column=4, padx=5, pady=5)
        self.data_nasc_entry = customtkinter.CTkEntry(form_frame)
        self.data_nasc_entry.grid(row=1, column=5, padx=5, pady=5)
        self.data_nasc_entry.bind("<KeyRelease>", self.on_data_nasc_keyrelease)

        customtkinter.CTkLabel(form_frame, text="Turma:").grid(row=0, column=4, padx=5, pady=5)
        self.turma_var = customtkinter.StringVar()
        turma_nomes = [f"{t.nome} (ID: {t.id})" for t in self.turmas]
        self.turma_dropdown = customtkinter.CTkOptionMenu(form_frame, variable=self.turma_var, values=turma_nomes)
        self.turma_dropdown.grid(row=0, column=5, padx=5, pady=5)

        self.add_btn = customtkinter.CTkButton(form_frame, text="Adicionar", command=self.adicionar_ou_salvar_aluno)
        self.add_btn.grid(row=0, column=6, padx=10, pady=5, rowspan=2)

        self.lista_frame = customtkinter.CTkFrame(self)
        self.lista_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.atualizar_lista()

    def on_data_nasc_keyrelease(self, event):
        texto = self.data_nasc_entry.get()
        # Remove tudo que não for número
        numeros = re.sub(r'\D', '', texto)
        # Limita a 8 dígitos (DDMMAAAA)
        numeros = numeros[:8]
        # Monta a string formatada
        formatada = ""
        if len(numeros) > 0:
            formatada += numeros[:2]
        if len(numeros) > 2:
            formatada += "/" + numeros[2:4]
        if len(numeros) > 4:
            formatada += "/" + numeros[4:8]
        # Evita loop infinito de eventos
        if texto != formatada:
            self.data_nasc_entry.delete(0, "end")
            self.data_nasc_entry.insert(0, formatada)

    def adicionar_ou_salvar_aluno(self):
        nome = self.nome_entry.get()
        matricula = self.matricula_entry.get()
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
        # Validação e conversão do formato
        if data_nascimento:
            try:
                # Converte de DD/MM/AAAA para YYYY-MM-DD
                dt = datetime.datetime.strptime(data_nascimento, "%d/%m/%Y")
                data_nascimento_db = dt.strftime("%Y-%m-%d")
            except ValueError:
                tkinter.messagebox.showerror("Erro", "Data de nascimento inválida! Use o formato DD/MM/AAAA.")
                return
        else:
            data_nascimento_db = None
        turma_nome = self.turma_var.get()
        turma_id = None
        for t in self.turmas:
            if f"{t.nome} (ID: {t.id})" == turma_nome:
                turma_id = t.id
        if not nome or not matricula or not turma_id:
            return
        try:
            if self.editando_id is None:
                self.service.cadastrar(nome, matricula, email, cpf, data_nascimento_db, turma_id)
            else:
                self.service.atualizar(self.editando_id, nome, matricula, email, cpf, data_nascimento_db)
                self.editando_id = None
                self.add_btn.configure(text="Adicionar")
        except ValueError as e:
            tkinter.messagebox.showerror("Erro", str(e))
            return
        self.nome_entry.delete(0, "end")
        self.matricula_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.cpf_entry.delete(0, "end")
        self.data_nasc_entry.delete(0, "end")
        self.turma_var.set("")
        self.atualizar_lista()

    def editar_aluno(self, aluno_id):
        aluno = next((a for a in self.alunos if getattr(a, "id", None) == aluno_id), None)
        if aluno:
            self.nome_entry.delete(0, "end")
            self.nome_entry.insert(0, aluno.nome)
            self.matricula_entry.delete(0, "end")
            self.matricula_entry.insert(0, aluno.matricula)
            self.email_entry.delete(0, "end")
            self.email_entry.insert(0, aluno.email or "")
            self.cpf_entry.delete(0, "end")
            self.cpf_entry.insert(0, aluno.cpf or "")
            self.data_nasc_entry.delete(0, "end")
            # Conversão de YYYY-MM-DD ou datetime.date para DD/MM/AAAA
            if aluno.data_nascimento:
                try:
                    if isinstance(aluno.data_nascimento, datetime.date):
                        dt = aluno.data_nascimento
                    else:
                        dt = datetime.datetime.strptime(aluno.data_nascimento, "%Y-%m-%d")
                    data_nasc_str = dt.strftime("%d/%m/%Y")
                except Exception:
                    data_nasc_str = str(aluno.data_nascimento)
                self.data_nasc_entry.insert(0, data_nasc_str)
            else:
                self.data_nasc_entry.insert(0, "")
            turma_nome = ""
            if aluno.turma_id:
                turma = next((t for t in self.turmas if t.id == aluno.turma_id), None)
                if turma:
                    turma_nome = f"{turma.nome} (ID: {turma.id})"
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
        self.turmas = self.turma_service.listar()
        if not self.alunos:
            customtkinter.CTkLabel(self.lista_frame, text="Nenhum aluno cadastrado.").pack()
        else:
            for aluno in self.alunos:
                turma_nome = ""
                if aluno.turma_id:
                    turma = next((t for t in self.turmas if t.id == aluno.turma_id), None)
                    if turma:
                        turma_nome = f" - Turma: {turma.nome} (ID: {turma.id})"
                text = (
                    f"{aluno.nome} (Matrícula: {aluno.matricula})"
                    f" | Email: {aluno.email or '-'}"
                    f" | CPF: {aluno.cpf or '-'}"
                    f" | Nasc.: {aluno.data_nascimento or '-'}"
                    f"{turma_nome}"
                )
                row_frame = customtkinter.CTkFrame(self.lista_frame)
                row_frame.pack(fill="x", padx=5, pady=2)
                customtkinter.CTkLabel(row_frame, text=text).pack(side="left", padx=10)
                edit_btn = customtkinter.CTkButton(row_frame, text="Editar", width=80,
                                                   command=lambda i=aluno.id: self.editar_aluno(i))
                edit_btn.pack(side="right", padx=5)
                del_btn = customtkinter.CTkButton(row_frame, text="Excluir", width=80, fg_color="red",
                                                  command=lambda i=aluno.id: self.excluir_aluno(i))
                del_btn.pack(side="right", padx=5)