# FINN · Agente Financeiro Inteligente

## Sobre o projeto

FINN é um protótipo de agente financeiro educativo desenvolvido em Streamlit. O aplicativo carrega dados de exemplo do cliente, gera alertas de orçamento e permite conversar com um modelo de linguagem via API Groq.

O foco atual do projeto é:
- visualização de gastos por categoria
- geração de alertas orçamentários
- suporte a metas e perfil de investidor
- chat interativo com respostas baseadas em dados locais

## Como usar

1. Instale as dependências:

```bash
pip install -r src/requirements.txt
```

2. Crie um arquivo `.env` na pasta `src/` com sua chave Groq:

```bash
GROQ_API_KEY=sua_chave_aqui
```

3. Execute o app:

```bash
cd src
streamlit run app.py
```

> Se `GROQ_API_KEY` não estiver definida, o app exibirá um erro e não carregará.

## Estrutura do projeto

```
📁 dio-lab-bia-do-futuro
├── 📄 README.md
├── 📁 src
│   ├── 📄 app.py              # interface Streamlit do FINN
│   ├── 📄 agente.py           # lógica do agente e chamada à API
│   ├── 📄 config.py           # configuração de caminhos e variáveis
│   └── 📄 requirements.txt    # dependências do projeto
├── 📁 data
│   ├── 📄 transacoes.csv
│   ├── 📄 historico_atendimento.csv
│   ├── 📄 perfil_investidor.json
│   └── 📄 produtos_financeiros.json
├── 📁 docs
│   ├── 📄 01-documentacao-agente.md
│   ├── 📄 02-base-conhecimento.md
│   ├── 📄 03-prompts.md
│   ├── 📄 04-metricas.md
│   └── 📄 05-pitch.md
├── 📁 assets
└── 📁 examples
```

## Dados usados

O projeto utiliza os arquivos em `data/` como base de conhecimento:

- `transacoes.csv` — histórico de transações do cliente
- `historico_atendimento.csv` — atendimentos anteriores
- `perfil_investidor.json` — perfil, orçamento e metas do cliente
- `produtos_financeiros.json` — lista de produtos financeiros disponíveis

## Funcionamento atual

1. `src/app.py` carrega os dados e exibe um dashboard com o perfil do usuário, metas e status de orçamento.
2. `src/agente.py` calcula gastos mensais e gera alertas por categoria.
3. O sistema monta um prompt estruturado para o modelo Groq usando todas as informações do usuário.
4. O chat do FINN encaminha as mensagens para a API Groq e apresenta as respostas na interface.

## Configuração e modelo

- Chave de API: `GROQ_API_KEY` via `.env`
- Modelo usado: `llama-3.3-70b-versatile`

## Rodando no Windows

No PowerShell:

```powershell
cd "c:\Users\taysa\Desktop\DIO\Bootcamp-Gen-AI\Assistente financeiro\dio-lab-bia-do-futuro\src"
pip install -r requirements.txt
streamlit run app.py
```

## Observações

- O app atual depende de internet para a chamada à API Groq.
- A lógica de alertas considera limites definidos em `perfil_investidor.json`.
- O chat deve usar apenas os dados locais disponíveis e não inventar informações.
