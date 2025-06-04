import customtkinter
from infrastructure.ai import perguntar_ia

class ChatBotFrame(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Assistente IA - Plataforma de Ensino")
        self.geometry("420x540")
        self.resizable(False, False)
        self.configure(bg="#222222")
        self.attributes("-topmost", True)

        # Área de mensagens (rolável)
        self.chat_area = customtkinter.CTkTextbox(self, width=400, height=400, font=("Arial", 13))
        self.chat_area.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        self.chat_area.configure(state="disabled")

        # Campo de entrada e botão
        input_frame = customtkinter.CTkFrame(self, fg_color="#222222")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.input_var = customtkinter.StringVar()
        self.input_entry = customtkinter.CTkEntry(input_frame, textvariable=self.input_var, width=300, font=("Arial", 13))
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self.enviar_pergunta)

        send_btn = customtkinter.CTkButton(input_frame, text="Enviar", width=80, command=self.enviar_pergunta)
        send_btn.pack(side="right")

        # Mensagem inicial
        self.adicionar_mensagem("IA", "Olá! Sou o assistente da Plataforma de Ensino. Pergunte sobre o funcionamento do sistema.")

    def adicionar_mensagem(self, remetente, texto):
        self.chat_area.configure(state="normal")
        if remetente == "Você":
            self.chat_area.insert("end", f"\nVocê: {texto}\n", "user")
        else:
            self.chat_area.insert("end", f"\nIA: {texto}\n", "ia")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")

    def enviar_pergunta(self, event=None):
        pergunta = self.input_var.get().strip()
        if not pergunta:
            return
        self.adicionar_mensagem("Você", pergunta)
        self.input_var.set("")
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", "\nIA está digitando...\n", "ia")
        self.chat_area.configure(state="disabled")
        self.chat_area.see("end")
        self.after(100, lambda: self.responder_ia(pergunta))

    def responder_ia(self, pergunta):
        resposta = perguntar_ia(pergunta)
        # Remove "IA está digitando..."
        self.chat_area.configure(state="normal")
        self.chat_area.delete("end-3l", "end-1l")
        self.chat_area.configure(state="disabled")
        self.adicionar_mensagem("IA", resposta)