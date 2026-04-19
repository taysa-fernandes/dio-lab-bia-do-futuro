import streamlit as st
from agente import responder, carregar_dados, calcular_gastos_mes, gerar_alertas
from config import GROQ_API_KEY
from datetime import datetime

# ─────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="FINN · Agente Financeiro",
    page_icon="💰",
    layout="wide",
)

# ─────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo geral */
    .stApp { background-color: #f0f4f8; }

    /* Header */
    .finn-header {
        background: linear-gradient(135deg, #1F4E79 0%, #2E75B6 100%);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        color: white;
    }
    .finn-header h1 { margin: 0; font-size: 2rem; }
    .finn-header p  { margin: 4px 0 0; opacity: 0.85; font-size: 0.95rem; }

    /* Cards de alerta */
    .alert-card {
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        color: #1a1a1a !important;
    }
    .alert-ok       { background: #e8f5e9; border-left: 4px solid #43a047; }
    .alert-atencao  { background: #fff8e1; border-left: 4px solid #ffa000; }
    .alert-urgente  { background: #fff3e0; border-left: 4px solid #e65100; }
    .alert-critico  { background: #ffebee; border-left: 4px solid #c62828; }

    /* Barra de progresso customizada */
    .prog-bar-wrap { background: #c8d8e8; border-radius: 8px; height: 10px; margin: 4px 0 8px; }
    .prog-bar-fill { height: 10px; border-radius: 8px; }

    /* Chat bubbles */
    .chat-user {
        background: #1F4E79; color: white;
        border-radius: 16px 16px 4px 16px;
        padding: 12px 16px; margin: 8px 0;
        max-width: 80%; margin-left: auto;
        text-align: right;
    }
    .chat-finn {
        background: white; color: #1a1a2e;
        border-radius: 16px 16px 16px 4px;
        padding: 12px 16px; margin: 8px 0;
        max-width: 80%;
        border: 1px solid #d0e4f5;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .chat-label-finn { font-size: 0.75rem; color: #2E75B6; font-weight: 600; margin-bottom: 4px; }
    .chat-label-user { font-size: 0.75rem; color: #aaa; margin-bottom: 4px; text-align: right; }

    /* Input */
    .stChatInput { border-radius: 12px; }

    /* Sidebar — texto branco geral, exceto cards de alerta */
    section[data-testid="stSidebar"] { background: #1F4E79; }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] small { color: white !important; }
    section[data-testid="stSidebar"] .alert-card,
    section[data-testid="stSidebar"] .alert-card * { color: #1a1a1a !important; }
    section[data-testid="stSidebar"] .stMetric { background: rgba(255,255,255,0.1); border-radius: 8px; padding: 8px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# VALIDAÇÃO DE API KEY
# ─────────────────────────────────────────
if not GROQ_API_KEY:
    st.error("⚠️ **GROQ_API_KEY não encontrada.** Crie um arquivo `.env` com sua chave antes de rodar.")
    st.code("GROQ_API_KEY=sua_chave_aqui", language="bash")
    st.stop()


# ─────────────────────────────────────────
# CARREGAMENTO DE DADOS
# ─────────────────────────────────────────
@st.cache_data(ttl=60)
def carregar_tudo():
    return carregar_dados()

transacoes, historico, perfil, produtos = carregar_tudo()
gastos  = calcular_gastos_mes(transacoes)
alertas = gerar_alertas(gastos, perfil.get("orcamento_mensal", {}))


# ─────────────────────────────────────────
# SIDEBAR — PAINEL FINANCEIRO
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 FINN")
    st.markdown(f"Olá, **{perfil['nome'].split()[0]}**! 👋")
    st.divider()

    st.markdown("### 📊 Orçamento do Mês")
    mes_atual = datetime.today().strftime("%B/%Y")
    st.caption(mes_atual)

    for a in alertas:
        pct   = min(a["percentual"], 100)
        cor   = {"ok": "#43a047", "atencao": "#ffa000", "urgente": "#e65100", "critico": "#c62828"}[a["nivel"]]
        classe = f"alert-{a['nivel']}"
        st.markdown(f"""
        <div class="alert-card {classe}">
            <b>{a['emoji']} {a['categoria'].capitalize()}</b><br>
            R$ {a['gasto']:.2f} / R$ {a['limite']:.2f} &nbsp;·&nbsp; {a['percentual']}%
            <div class="prog-bar-wrap">
                <div class="prog-bar-fill" style="width:{pct}%; background:{cor};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### 🎯 Metas")
    for m in perfil.get("metas", []):
        st.markdown(f"**{m['meta']}**")
        st.caption(f"R$ {m['valor_necessario']:,.2f} até {m['prazo']}")

    st.divider()
    st.markdown(f'''
    <div style="color:white;">
        <p style="font-size:1rem; font-weight:700; margin-bottom:10px;">👤 Perfil</p>
        <p style="margin:6px 0; color:white;">💵 Renda: <b>R$ {perfil["renda_mensal"]:,.2f}</b></p>
        <p style="margin:6px 0; color:white;">📈 Tipo: <b>{perfil["perfil_investidor"].capitalize()}</b></p>
        <p style="margin:6px 0; color:white;">🛡️ Aceita risco: <b>{"Sim" if perfil["aceita_risco"] else "Não"}</b></p>
    </div>
    ''', unsafe_allow_html=True)


# ─────────────────────────────────────────
# ÁREA PRINCIPAL — CHAT
# ─────────────────────────────────────────
st.markdown("""
<div class="finn-header">
    <h1>💬 Converse com o FINN</h1>
    <p>Seu agente financeiro educativo · Controle de gastos e alertas inteligentes</p>
</div>
""", unsafe_allow_html=True)

# Estado da sessão
if "historico_chat" not in st.session_state:
    st.session_state.historico_chat = []

if "mensagens_ui" not in st.session_state:
    # Mensagem de boas-vindas
    nome = perfil["nome"].split()[0]

    # Alerta de abertura se houver categorias em risco
    alertas_urgentes = [a for a in alertas if a["nivel"] in ("urgente", "critico")]
    aviso = ""
    if alertas_urgentes:
        cats = ", ".join(a["categoria"] for a in alertas_urgentes)
        aviso = f"\n\n⚠️ Antes de começar: **{cats}** {'está' if len(alertas_urgentes)==1 else 'estão'} com orçamento crítico este mês. Quer ver os detalhes?"

    st.session_state.mensagens_ui = [{
        "role": "assistant",
        "content": f"Oi, {nome}! Sou o **FINN**, seu parceiro financeiro 💰\n\n"
                   f"Posso te ajudar com:\n"
                   f"- 📊 Ver seus gastos e alertas do mês\n"
                   f"- 🎯 Acompanhar o progresso nas suas metas\n"
                   f"- 💡 Entender onde investir o que sobrar\n"
                   f"- 📚 Explicar qualquer conceito financeiro{aviso}\n\n"
                   f"Como posso te ajudar hoje?"
    }]

# Renderiza histórico de mensagens
for msg in st.session_state.mensagens_ui:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end;">
            <div>
                <div class="chat-label-user">Você</div>
                <div class="chat-user">{msg['content']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start;">
            <div>
                <div class="chat-label-finn">💰 FINN</div>
                <div class="chat-finn">{msg['content'].replace(chr(10), '<br>')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# INPUT DO USUÁRIO
# ─────────────────────────────────────────
sugestoes = [
    "Como estão meus gastos esse mês?",
    "Qual o meu progresso nas metas?",
    "Tenho dinheiro sobrando, onde investir?",
    "O que é Tesouro Selic?",
]

cols = st.columns(len(sugestoes))
for i, sug in enumerate(sugestoes):
    if cols[i].button(sug, use_container_width=True):
        st.session_state._sugestao = sug

pergunta = st.chat_input("Digite sua mensagem para o FINN...")

# Prioriza sugestão clicada
if hasattr(st.session_state, "_sugestao") and st.session_state._sugestao:
    pergunta = st.session_state._sugestao
    del st.session_state._sugestao

if pergunta:
    st.session_state.mensagens_ui.append({"role": "user", "content": pergunta})

    with st.spinner("FINN está pensando..."):
        try:
            resposta, st.session_state.historico_chat = responder(
                pergunta, st.session_state.historico_chat
            )
            st.session_state.mensagens_ui.append({"role": "assistant", "content": resposta})
        except Exception as e:
            st.session_state.mensagens_ui.append({
                "role": "assistant",
                "content": f"Ops, tive um problema técnico: `{e}`. Tente novamente em instantes."
            })

    st.rerun()