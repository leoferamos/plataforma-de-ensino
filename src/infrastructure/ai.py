import re
import os
import requests
from .ai_context import CONTEXT
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")  # valor padrão

def contem_dado_pessoal(pergunta: str) -> bool:
    # Detecta CPF (11 dígitos seguidos)
    if re.search(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", pergunta):
        return True
    # Detecta e-mail
    if re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", pergunta):
        return True
    # Detecta números longos (ex: matrícula, RG, tokens)
    if re.search(r"\b\d{6,}\b", pergunta):
        return True
    return False

def perguntar_ia(pergunta: str) -> str:
    if contem_dado_pessoal(pergunta):
        return "Desculpe, não posso responder perguntas que envolvam dados pessoais ou sensíveis."
    prompt = CONTEXT + "\n\nPergunta do usuário: " + pergunta
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": GEMINI_API_KEY}
    try:
        resp = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        if resp.status_code == 200:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"Erro ao consultar IA: código {resp.status_code}"
    except Exception as e:
        return f"Erro ao consultar IA: {e}"