# Código da Aplicação

Esta pasta contém o código do agente financeiro **FINN** — controle de gastos e alertas para investidores iniciantes.

## Estrutura

```
src/
├── app.py              # Interface principal (Streamlit)
├── agente.py           # Lógica do agente: carregamento de dados, alertas e chamada à API
├── config.py           # Configurações: caminhos, modelo e limiares de alerta
├── requirements.txt    # Dependências do projeto
└── .env.example        # Modelo do arquivo de variáveis de ambiente
```

## Pré-requisitos

- Python 3.10+
- Conta gratuita no [Groq Console](https://console.groq.com) para obter a API key

## Como Rodar

**1. Clone o repositório e entre na pasta:**
```bash
git clone https://github.com/taysa-fernandes/dio-lab-bia-do-futuro.git
cd dio-lab-bia-do-futuro
```

**2. Crie o arquivo `.env` com sua chave:**
```bash
cp src/.env.example src/.env
# Abra o .env e preencha com sua chave Groq
```

```env
GROQ_API_KEY=sua_chave_aqui
```

**3. Instale as dependências:**
```bash
pip install -r src/requirements.txt
```

**4. Rode a aplicação:**
```bash
cd src
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`.

## Dependências

```
streamlit==1.35.0
requests==2.31.0
pandas==2.2.2
python-dotenv==1.0.1
```

## Observações

- O arquivo `.env` **não deve ser commitado** — ele já está no `.gitignore`
- Os arquivos de dados (`data/`) devem estar na raiz do projeto, um nível acima de `src/`
- O modelo utilizado é o `llama3-70b-8192` via API do Groq