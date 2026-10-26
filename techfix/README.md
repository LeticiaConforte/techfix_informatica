# 🛠️ TechFix Informática — Sistema de Ordens de Serviço

Solução integrada para automação de ordens de serviço (O.S.) substituindo fichas físicas de papel por banco de dados relacional em nuvem, interface mobile de balcão e painel gerencial web.

---

## 🏗️ Arquitetura da Solução

* **Banco de Dados:** PostgreSQL hospedado no **Supabase**, com validação de formato de e-mail/telefone, integridade referencial e triggers de atualização.
* **Interface de Atendimento (Mobile / Balcão):** Desenvolvida com **Gradio (gr.Blocks)** para cadastro ágil e reaproveitamento de clientes via e-mail.
* **Painel Administrativo:** Construído em **Streamlit**, provendo operações de CRUD completas, filtros dinâmicos, métricas e visualizações analíticas de status.

---

## 📂 Estrutura do Repositório

```text
techfix/
├── sql/
│   └── schema.sql            # Script de criação das tabelas e constraints
├── app_gradio.py             # Aplicação de atendimento (Gradio)
├── app_streamlit.py          # Painel administrativo (Streamlit)
├── requirements.txt          # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
├── README.md                 # Instruções e documentação
└── evidencias/               # Capturas de tela comprobatórias
    ├── 01_gradio_mobile.png
    ├── 02_cadastro_sucesso.png
    ├── 03_supabase_tabelas.png
    └── 04_streamlit_dashboard.png
