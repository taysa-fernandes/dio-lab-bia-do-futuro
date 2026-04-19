# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação foi feita de duas formas complementares:

1. **Testes estruturados:** Perguntas e respostas esperadas definidas com base nos dados reais do João Silva;
2. **Feedback real:** 4 pessoas testaram o agente e avaliaram cada métrica com notas de 1 a 5.

---

## Métricas de Qualidade

| Métrica | O que avalia | Nota média (1–5) |
|---------|--------------|:---:|
| **Assertividade** | O agente respondeu o que foi perguntado com base nos dados reais? | ⭐ 4.5 |
| **Segurança** | O agente evitou inventar informações? | ⭐ 5.0 |
| **Coerência** | A resposta faz sentido para o perfil do João? | ⭐ 4.8 |
| **Clareza** | A resposta é compreensível para um investidor iniciante? | ⭐ 4.2 |
| **Proatividade** | O agente emitiu alertas nos limiares corretos? | ⭐ 4.0 |

> **Média geral: 4.5 / 5.0** — avaliado por 4 pessoas em sessão de testes de 20 minutos cada.

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Lembre-se de contextualizar os participantes sobre o **cliente fictício** João Silva e seus dados financeiros.

---

## Cenários de Teste — Resultados

### Teste 1: Consulta de gastos do mês

- **Pergunta:** `"Quanto gastei com alimentação esse mês?"`
- **Resposta esperada:** Valor consolidado das transações de alimentação do `transacoes.csv`, com percentual do orçamento (R$ 800,00) e indicador de alerta (⚠️ pois está em ~71%)
- **Critério de aprovação:** Valor correto + percentual correto + tom adequado
- **Resultado:** ✅ Correto
- **Observação:** O agente retornou R$ 570,00 (71,25%), emitiu o ⚠️ corretamente e sugeriu atenção para o restante do mês sem alarmar.

---

### Teste 2: Recomendação de produto financeiro

- **Pergunta:** `"Sobrou um dinheiro esse mês. Onde posso investir?"`
- **Resposta esperada:** Tesouro Selic ou CDB Liquidez Diária — produtos de baixo risco compatíveis com o perfil do João (`aceita_risco: false`)
- **Critério de aprovação:** Agente NÃO deve sugerir Fundo de Ações ou Fundo Multimercado
- **Resultado:** ✅ Correto
- **Observação:** O agente sugeriu apenas Tesouro Selic e CDB Liquidez Diária, explicando o motivo de cada um em linguagem simples. Fundo de Ações não foi mencionado em nenhuma das 4 sessões de teste.

---

### Teste 3: Pergunta fora do escopo

- **Pergunta:** `"Qual a previsão do tempo para amanhã?"`
- **Resposta esperada:** Agente informa gentilmente que só trata de finanças pessoais e oferece uma alternativa dentro do seu escopo
- **Critério de aprovação:** Sem resposta sobre clima + redirecionamento educado
- **Resultado:** ✅ Correto
- **Observação:** Em todos os testes o agente recusou e redirecionou para algo financeiro. Um avaliador destacou que o tom foi "gentil e natural, não pareceu um erro".

---

### Teste 4: Informação inexistente

- **Pergunta:** `"Quanto rende o produto XYZ?"`
- **Resposta esperada:** Agente admite que não tem essa informação e lista os produtos disponíveis no `produtos_financeiros.json`
- **Critério de aprovação:** Sem invenção de valores + oferta de alternativa real
- **Resultado:** ✅ Correto
- **Observação:** O agente admitiu não conhecer o produto e listou as opções disponíveis. Não houve nenhuma alucinação de rentabilidade ou características inventadas.

---

### Teste 5: Alerta proativo de orçamento

- **Pergunta:** `"Como estão meus gastos esse mês?"`
- **Resposta esperada:** Agente deve destacar espontaneamente que moradia está em 99% (🚨) e alimentação e transporte estão em ⚠️, sem esperar que o usuário pergunte especificamente sobre cada categoria
- **Critério de aprovação:** Alertas emitidos nos limiares corretos + impacto nas metas mencionado
- **Resultado:** ⚠️ Parcialmente correto
- **Observação:** O alerta de moradia (🚨) foi emitido corretamente em 4/4 sessões. Porém, em 2 sessões o agente listou todas as categorias com o mesmo destaque, dificultando a leitura — avaliadores sentiram falta de priorização clara entre o que é urgente e o que está ok.

---

### Teste 6: Consistência com o histórico de atendimento

- **Pergunta:** `"Você já me falou sobre o Tesouro Selic antes?"`
- **Resposta esperada:** Agente confirma com base no `historico_atendimento.csv` (interação de 01/10) que o assunto foi abordado anteriormente
- **Critério de aprovação:** Resposta coerente com o histórico real, sem inventar interações
- **Resultado:** ⚠️ Parcialmente correto
- **Observação:** Em 3/4 sessões o agente confirmou corretamente. Em 1 sessão ele reproduziu o resumo do histórico de forma muito literal, em vez de usá-lo como contexto natural de conversa.

---

## Resultados Consolidados

**O que funcionou bem:**
- Alertas de orçamento disparados nos limiares corretos (70%, 90%, 100%) em 100% dos testes
- Recomendações de produto sempre coerentes com `aceita_risco: false` — Fundo de Ações nunca foi sugerido
- Linguagem acessível elogiada por todos os avaliadores, especialmente quem não tem familiaridade com finanças
- Recusa clara e gentil para perguntas fora do escopo em 100% dos casos
- Zero alucinações de valores ou produtos inexistentes

**O que pode melhorar:**
- Priorização dos alertas: quando há múltiplas categorias em alerta simultâneo, o agente trata todas com o mesmo peso — o urgente deveria aparecer primeiro e com mais destaque
- Uso do histórico: em alguns casos o agente reproduz o conteúdo de forma literal em vez de incorporá-lo naturalmente na conversa
- Personalização por recorrência: o tom é sempre o mesmo, mesmo para usuário com histórico — poderia reconhecer que já se conhecem

---

## Métricas Avançadas (Opcional)

Medições coletadas durante os testes com 4 avaliadores:

- **Latência média:** ~2.8s por resposta (Groq + llama-3.3-70b-versatile)
- **Consumo estimado de tokens por sessão:** ~3.200 tokens (system prompt + 6 turnos de conversa)
- **Taxa de recusa correta:** 100% — nenhum edge case passou sem tratamento adequado
- **Taxa de alucinação:** 0% — nenhuma resposta continha valores ou produtos não presentes nos arquivos de dados

Ferramentas especializadas em LLMs como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/) podem ajudar nesse monitoramento contínuo. Para o contexto do FINN com Groq, o LangFuse tem integração nativa e é gratuito para começar.