import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TRANSACOES_PATH = os.path.join(DATA_DIR, "transacoes.csv")
HISTORICO_PATH = os.path.join(DATA_DIR, "historico_atendimento.csv")
PERFIL_PATH = os.path.join(DATA_DIR, "perfil_investidor.json")
PRODUTOS_PATH = os.path.join(DATA_DIR, "produtos_financeiros.json")

ALERT_WARNING = 0.70   # ⚠️ amarelo
ALERT_URGENT  = 0.90   # 🚨 laranja
ALERT_OVER    = 1.00   # 🔴 vermelho