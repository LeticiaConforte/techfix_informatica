# 🛠️ TechFix Informática — Sistema de Gestão de Ordens de Serviço

> **Atividade Prática:** Integração de Interface Web com Banco de Dados em Nuvem (Supabase + Gradio + Streamlit).

---

## 📌 Resumo da Atividade

A loja fictícia **TechFix Informática** realizava seus atendimentos técnicos anotando os dados em fichas de papel, o que gerava perda de informações, lentidão no contato com os clientes e ausência de controle sobre os reparos.

Esta solução substitui o papel por uma arquitetura em nuvem composta por duas aplicações integradas a um banco de dados centralizado:
1. **Atendimento de Balcão / Mobile (Gradio):** Interface responsiva voltada para o atendente cadastrar rapidamente o cliente, equipamento e problema apresentado diretamente pelo smartphone ou computador, reaproveitando clientes cadastrados e gerando o número da Ordem de Serviço (O.S.).
2. **Painel Gerencial (Streamlit):** Aplicação para o gerente e corpo técnico realizarem a gestão completa (CRUD) das ordens, aplicar filtros avançados, atualizar status de reparo, analisar métricas em tempo real e exportar relatórios em CSV.
3. **Persistência Relacional (Supabase / PostgreSQL):** Banco de dados relacional em nuvem com integridade referencial, validações de formato (e-mail e telefone) e triggers de auditoria.

---

## 🌐 Links das Aplicações em Produção

* 📊 **Painel Administrativo (Streamlit Cloud):** [https://techfixinformatica.streamlit.app](https://techfixinformatica.streamlit.app)
* 📱 **Interface de Cadastro (Gradio Link Público / HuggingFace Spaces):** *(Insira aqui o link temporário do `gradio.live` ou o link do seu Space no Hugging Face)*

---

## 🏗️ Arquitetura e Tecnologias

* **Banco de Dados:** PostgreSQL hospedado no [Supabase](https://supabase.com) (tabelas `clientes` e `ordens_servico`).
* **Frontend Mobile / Balcão:** Python + [Gradio](https://gradio.app) (`gr.Blocks` com visualização responsiva).
* **Painel Administrativo:** Python + [Streamlit](https://streamlit.io) (CRUD com `st.tabs`, métricas com `st.metric` e gráficos interativos).
* **Comunicação com o Banco:** `supabase-py` consumindo a API REST oficial.
* **Segurança:** Chaves sensíveis gerenciadas via variáveis de ambiente (`.env` e Streamlit Secrets).

---

## 📂 Estrutura do Repositório

```text
techfix/
├── sql/
│   └── schema.sql            # DDL completo com tabelas, PK, FK, CHECK e Triggers
├── app_gradio.py             # Aplicação de atendimento (Gradio)
├── app_streamlit.py          # Painel de gestão do gerente (Streamlit)
├── requirements.txt          # Dependências do projeto
├── .env.example              # Modelo de variáveis de ambiente (sem credenciais)
├── README.md                 # Documentação e instruções de execução
└── evidencias/               # Capturas de tela de funcionamento
    ├── 01_gradio_mobile.png
    ├── 02_cadastro_sucesso.png
    ├── 03_supabase_tabelas.png
    └── 04_streamlit_dashboard.png
