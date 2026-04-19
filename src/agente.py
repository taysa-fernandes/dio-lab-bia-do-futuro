import json
import requests
import pandas as pd
from datetime import datetime
from config import (
    GROQ_API_KEY, GROQ_MODEL,
    TRANSACOES_PATH, HISTORICO_PATH, PERFIL_PATH, PRODUTOS_PATH,
    ALERT_WARNING, ALERT_URGENT, ALERT_OVER
)


# ─────────────────────────────────────────
# 1. CARREGAMENTO DE DADOS
# ─────────────────────────────────────────

def carregar_dados():
    """Carrega todos os arquivos da base de conhecimento."""
    transacoes = pd.read_csv(TRANSACOES_PATH, parse_dates=["data"])
    historico  = pd.read_csv(HISTORICO_PATH, parse_dates=["data"])

    with open(PERFIL_PATH, encoding="utf-8") as f:
        perfil = json.load(f)

    with open(PRODUTOS_PATH, encoding="utf-8") as f:
        produtos = json.load(f)

    return transacoes, historico, perfil, produtos


# ─────────────────────────────────────────
# 2. CÁLCULO DE GASTOS E ALERTAS
# ─────────────────────────────────────────

def calcular_gastos_mes(transacoes: pd.DataFrame, mes: int = None, ano: int = None):
    """Retorna gastos por categoria no mês/ano especificado (padrão: mês atual)."""
    hoje = datetime.today()
    mes  = mes or hoje.month
    ano  = ano or hoje.year

    df = transacoes[
        (transacoes["tipo"] == "saida") &
        (transacoes["data"].dt.month == mes) &
        (transacoes["data"].dt.year  == ano) &
        (transacoes["categoria"] != "receita")
    ]
    return df.groupby("categoria")["valor"].sum().to_dict()


def gerar_alertas(gastos: dict, orcamento: dict) -> list[dict]:
    """Compara gastos com orçamento e gera lista de alertas por categoria."""
    alertas = []
    for cat, limite in orcamento.items():
        gasto = gastos.get(cat, 0)
        pct   = gasto / limite if limite > 0 else 0

        if pct >= ALERT_OVER:
            nivel, emoji = "critico", "🔴"
        elif pct >= ALERT_URGENT:
            nivel, emoji = "urgente", "🚨"
        elif pct >= ALERT_WARNING:
            nivel, emoji = "atencao", "⚠️"
        else:
            nivel, emoji = "ok", "✅"

        alertas.append({
            "categoria": cat,
            "gasto":     gasto,
            "limite":    limite,
            "percentual": round(pct * 100, 1),
            "nivel":     nivel,
            "emoji":     emoji,
        })

    return sorted(alertas, key=lambda x: x["percentual"], reverse=True)


# ─────────────────────────────────────────
# 3. MONTAGEM DO SYSTEM PROMPT
# ─────────────────────────────────────────

def montar_system_prompt(perfil: dict, produtos: list, historico: pd.DataFrame,
                          gastos: dict, alertas: list) -> str:
    """Monta o system prompt completo com todos os dados do usuário."""

    orcamento = perfil.get("orcamento_mensal", {})
    mes_atual = datetime.today().strftime("%B/%Y")

    # ── Resumo de gastos com alertas ──
    linhas_gastos = []
    for a in alertas:
        linhas_gastos.append(
            f"  - {a['categoria'].capitalize()}: R$ {a['gasto']:.2f} "
            f"de R$ {a['limite']:.2f} → {a['percentual']}% {a['emoji']}"
        )
    resumo_gastos = "\n".join(linhas_gastos) if linhas_gastos else "  Nenhuma transação registrada este mês."

    # ── Histórico (últimas 3 interações) ──
    hist_recente = historico.sort_values("data", ascending=False).head(3)
    linhas_hist  = [
        f"  - {row['data'].strftime('%d/%m')}: {row['tema']} — {row['resumo']}"
        for _, row in hist_recente.iterrows()
    ]
    resumo_hist = "\n".join(linhas_hist)

    # ── Produtos filtrados por perfil de risco ──
    aceita_risco = perfil.get("aceita_risco", False)
    produtos_ok  = [p for p in produtos if p["risco"] == "baixo"] if not aceita_risco else produtos
    linhas_prod  = [
        f"  - {p['nome']}: {p['rentabilidade']}, aporte mínimo R$ {p['aporte_minimo']:.2f}"
        for p in produtos_ok
    ]
    resumo_prod = "\n".join(linhas_prod)

    # ── Metas ──
    linhas_metas = [
        f"  - {m['meta']}: R$ {m['valor_necessario']:.2f} até {m['prazo']}"
        for m in perfil.get("metas", [])
    ]
    resumo_metas = "\n".join(linhas_metas)

    return f"""Você é o FINN, um agente financeiro educativo e acessível.
Seu objetivo é ajudar o usuário a controlar gastos, emitir alertas de orçamento e orientar sobre investimentos simples.

REGRAS OBRIGATÓRIAS:
1. Use APENAS os dados fornecidos abaixo. Nunca invente valores, produtos ou transações.
2. Use linguagem simples e acessível. Explique termos técnicos com exemplos do cotidiano.
3. Nunca use linguagem alarmista — mesmo em alertas críticos, mantenha tom encorajador.
4. Não recomende investimentos de risco alto se aceita_risco for falso.
5. Se não souber algo, admita e redirecione para o que pode ajudar.
6. Fora do escopo financeiro pessoal, recuse gentilmente e ofereça uma alternativa dentro do seu escopo.
7. Nunca compartilhe dados de outros usuários.

━━━━━━━━━━━━━━━━━━━━━━━━
PERFIL DO USUÁRIO
━━━━━━━━━━━━━━━━━━━━━━━━
- Nome: {perfil['nome']}
- Idade: {perfil['idade']} anos
- Profissão: {perfil['profissao']}
- Renda mensal: R$ {perfil['renda_mensal']:.2f}
- Perfil investidor: {perfil['perfil_investidor'].capitalize()}
- Objetivo principal: {perfil['objetivo_principal']}
- Aceita risco: {'Sim' if aceita_risco else 'Não'}
- Patrimônio total: R$ {perfil['patrimonio_total']:.2f}
- Reserva de emergência atual: R$ {perfil['reserva_emergencia_atual']:.2f}

METAS:
{resumo_metas}

━━━━━━━━━━━━━━━━━━━━━━━━
ORÇAMENTO E GASTOS — {mes_atual}
━━━━━━━━━━━━━━━━━━━━━━━━
{resumo_gastos}

Legenda: ✅ OK | ⚠️ Atenção (≥70%) | 🚨 Urgente (≥90%) | 🔴 Estourado (≥100%)

━━━━━━━━━━━━━━━━━━━━━━━━
PRODUTOS DISPONÍVEIS (compatíveis com o perfil)
━━━━━━━━━━━━━━━━━━━━━━━━
{resumo_prod}

━━━━━━━━━━━━━━━━━━━━━━━━
HISTÓRICO DE ATENDIMENTOS RECENTES
━━━━━━━━━━━━━━━━━━━━━━━━
{resumo_hist}

━━━━━━━━━━━━━━━━━━━━━━━━
Responda à mensagem do usuário com base exclusivamente nas informações acima.
"""


# ─────────────────────────────────────────
# 4. CHAMADA À API DO GROQ
# ─────────────────────────────────────────

def chamar_groq(system_prompt: str, historico_chat: list[dict]) -> str:
    """Envia mensagens para a API do Groq e retorna a resposta."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    # Limita historico a ultimas 6 mensagens para nao estourar contexto
    hist_recente = historico_chat[-6:] if len(historico_chat) > 6 else historico_chat
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + hist_recente,
        "temperature": 0.3,
        "max_tokens": 800,
    }
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if not resp.ok:
        try:
            detalhe = resp.json().get("error", {}).get("message", resp.text)
        except Exception:
            detalhe = resp.text
        raise Exception(f"Groq API erro {resp.status_code}: {detalhe}")
    return resp.json()["choices"][0]["message"]["content"]


# ─────────────────────────────────────────
# 5. FUNÇÃO PRINCIPAL DO AGENTE
# ─────────────────────────────────────────

def responder(mensagem: str, historico_chat: list[dict]) -> tuple[str, list]:
    """Recebe mensagem do usuário e retorna resposta do FINN."""
    transacoes, historico, perfil, produtos = carregar_dados()

    gastos  = calcular_gastos_mes(transacoes)
    alertas = gerar_alertas(gastos, perfil.get("orcamento_mensal", {}))
    system  = montar_system_prompt(perfil, produtos, historico, gastos, alertas)

    historico_chat.append({"role": "user", "content": mensagem})
    resposta = chamar_groq(system, historico_chat)
    historico_chat.append({"role": "assistant", "content": resposta})

    return resposta, historico_chat