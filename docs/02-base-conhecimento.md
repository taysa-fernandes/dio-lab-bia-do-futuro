# Base de Conhecimento

## Dados Utilizados

Todos os quatro arquivos mockados da pasta `data/` são utilizados pelo FINN, cada um com um papel específico no fluxo do agente:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `transacoes.csv` | CSV | Analisar padrão de gastos, categorizar despesas e calcular o percentual de uso do orçamento por categoria |
| `historico_atendimento.csv` | CSV | Personalizar o tom das respostas com base em interações anteriores e evitar repetir alertas já emitidos |
| `perfil_investidor.json` | JSON | Definir os limites de orçamento por categoria e adaptar as sugestões ao perfil financeiro do usuário |
| `produtos_financeiros.json` | JSON | Sugerir destinos para o valor economizado (ex: CDB, Tesouro Direto) de forma contextualizada ao perfil |
 
---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Os dados mockados foram utilizados como base, com as seguintes adaptações para o contexto do FINN:
 
- **`transacoes.csv`**: utilizado sem alterações; já possui as colunas `categoria` e `tipo` (entrada/saída) necessárias para o agrupamento de gastos e cálculo de alertas por limiar.
- **`perfil_investidor.json`**: expandido com o campo `orcamento_mensal` contendo os limites mensais por categoria (alimentação R$800, moradia R$1.400, transporte R$400, lazer R$200, saúde R$300).
- **`historico_atendimento.csv`**: mantido sem alterações; utilizado apenas para leitura e contexto conversacional.
- **`produtos_financeiros.json`**: mantido sem alterações; consultado somente quando o agente identifica saldo disponível para sugestão de investimento.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos são carregados uma única vez no início da sessão, assim que o usuário se autentica. O conteúdo é lido, processado e mantido em memória durante toda a conversa. Não há consultas repetidas ao disco durante o fluxo — o estado é atualizado em memória à medida que novos gastos são registrados.
 
```python
# Exemplo de carregamento no início da sessão
import pandas as pd
import json
 
transacoes = pd.read_csv("data/transacoes.csv")
historico   = pd.read_csv("data/historico_atendimento.csv")
 
with open("data/perfil_investidor.json") as f:
    perfil = json.load(f)
 
with open("data/produtos_financeiros.json") as f:
    produtos = json.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados vão no **system prompt**, montados de forma estruturada antes de cada interação. O perfil do investidor e o resumo de gastos do mês atual são sempre incluídos. O histórico de atendimento é incluído de forma resumida (últimas 3 interações) para manter o contexto sem estourar a janela de tokens. Os produtos financeiros só são injetados no prompt quando o agente identifica oportunidade de sugestão de investimento.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

Abaixo um exemplo real de como os dados são formatados e enviados ao modelo no system prompt:
 
```
Você é o FINN, um agente financeiro educativo e acessível.
Seu objetivo é ajudar o usuário a controlar gastos e emitir alertas antes que o orçamento seja estourado.
Responda sempre em linguagem simples, sem jargões. Nunca invente dados — use apenas as informações abaixo.
 
---
 
PERFIL DO USUÁRIO:
- Nome: Taysa Fernandes
- Perfil de investidor: Moderado
- Renda mensal: R$ 5.000,00
- Objetivo principal: Construir reserva de emergência
- Aceita risco: Não
 
ORÇAMENTO MENSAL POR CATEGORIA:
- Alimentação:  R$ 800,00
- Moradia:      R$ 1.400,00
- Transporte:   R$ 400,00
- Lazer:        R$ 200,00
- Saúde:        R$ 300,00
 
GASTOS DO MÊS ATUAL (outubro/2025):
- Alimentação:  R$ 570,00  → 71% do orçamento ⚠️
- Moradia:      R$ 1.380,00 → 99% do orçamento 🚨
- Transporte:   R$ 295,00  → 74% do orçamento ⚠️
- Lazer:        R$ 55,90   → 28% do orçamento ✅
- Saúde:        R$ 188,00  → 63% do orçamento ✅
 
ÚLTIMAS INTERAÇÕES:
- 01/10: Cliente perguntou sobre funcionamento do Tesouro Selic.
- 12/10: Cliente acompanhou progresso da reserva de emergência.
- 25/10: Cliente atualizou dados cadastrais.
 
PRODUTOS DISPONÍVEIS (perfil sem risco):
- Tesouro Selic — 100% da Selic, aporte mínimo R$ 30,00
- CDB Liquidez Diária — 102% do CDI, aporte mínimo R$ 100,00
 
---
 
Responda à mensagem do usuário com base exclusivamente nas informações acima.
```
