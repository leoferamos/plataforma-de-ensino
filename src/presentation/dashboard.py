import customtkinter
from presentation.forms import AlunoFrame, ProfessorFrame, CursoFrame, TurmaFrame
from presentation.relatorio_frame import RelatorioFrame 

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Plataforma de Ensino Presencial")
        self.geometry(f"{1100}x{580}")

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Plataforma Ensino", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_alunos = customtkinter.CTkButton(self.sidebar_frame, text="Alunos", command=self.show_alunos)
        self.btn_alunos.grid(row=1, column=0, padx=20, pady=10)
        self.btn_professores = customtkinter.CTkButton(self.sidebar_frame, text="Professores", command=self.show_professores)
        self.btn_professores.grid(row=2, column=0, padx=20, pady=10)
        self.btn_cursos = customtkinter.CTkButton(self.sidebar_frame, text="Cursos", command=self.show_cursos)
        self.btn_cursos.grid(row=3, column=0, padx=20, pady=10)
        self.btn_turmas = customtkinter.CTkButton(self.sidebar_frame, text="Turmas", command=self.show_turmas)
        self.btn_turmas.grid(row=4, column=0, padx=20, pady=10)
        self.btn_relatorio = customtkinter.CTkButton(self.sidebar_frame, text="Relatório", command=self.show_relatorio)  # Adicione este botão
        self.btn_relatorio.grid(row=5, column=0, padx=20, pady=10)  

        tema_frame = customtkinter.CTkFrame(self.sidebar_frame, fg_color="transparent")
        tema_frame.grid(row=7, column=0, padx=20, pady=(10, 10), sticky="ew")
        self.appearance_mode_label = customtkinter.CTkLabel(tema_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.pack(side="left")
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            tema_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.pack(side="left", padx=(5, 0))

        # Main content area
        self.main_content = customtkinter.CTkFrame(self)
        self.main_content.grid(row=0, column=1, sticky="nsew")
        self.current_frame = None

        self.show_alunos()  # Tela inicial

    def clear_main_content(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def show_alunos(self):
        self.clear_main_content()
        self.current_frame = AlunoFrame(self.main_content)
        self.current_frame.pack(fill="both", expand=True)

    def show_professores(self):
        self.clear_main_content()
        self.current_frame = ProfessorFrame(self.main_content)
        self.current_frame.pack(fill="both", expand=True)

    def show_cursos(self):
        self.clear_main_content()
        self.current_frame = CursoFrame(self.main_content)
        self.current_frame.pack(fill="both", expand=True)

    def show_turmas(self):
        self.clear_main_content()
        self.current_frame = TurmaFrame(self.main_content)
        self.current_frame.pack(fill="both", expand=True)

    def show_relatorio(self): 
        self.clear_main_content()
        self.current_frame = RelatorioFrame(self.main_content) 
        self.current_frame.pack(fill="both", expand=True)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()