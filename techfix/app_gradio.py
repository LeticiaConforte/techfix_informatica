import os
import re
import gradio as gr
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Defina SUPABASE_URL e SUPABASE_KEY no arquivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

def validar_campos(nome, endereco, email, celular, modelo, problema):
    if not all([nome.strip(), endereco.strip(), email.strip(), celular.strip(), modelo.strip(), problema.strip()]):
        return False, "⚠️ Todos os campos são obrigatórios."
    
    if not re.match(EMAIL_REGEX, email.strip()):
        return False, "⚠️ E-mail inválido. Utilize o formato: exemplo@dominio.com"
        
    celular_limpo = re.sub(r"\D", "", celular)
    if not (10 <= len(celular_limpo) <= 13):
        return False, "⚠️ Celular inválido. Insira apenas números com DDD (10 a 13 dígitos)."
        
    return True, celular_limpo

def cadastrar_atendimento(nome, endereco, email, celular, modelo, problema):
    valido, msg_ou_celular = validar_campos(nome, endereco, email, celular, modelo, problema)
    if not valido:
        return f"❌ {msg_ou_celular}"

    celular_limpo = msg_ou_celular
    email_limpo = email.strip().lower()

    try:
        res_cliente = supabase.table("clientes").select("id").eq("email", email_limpo).execute()
        
        if res_cliente.data and len(res_cliente.data) > 0:
            cliente_id = res_cliente.data[0]["id"]
            supabase.table("clientes").update({
                "nome": nome.strip(),
                "endereco": endereco.strip(),
                "celular_whatsapp": celular_limpo
            }).eq("id", cliente_id).execute()
        else:
            novo_cliente = supabase.table("clientes").insert({
                "nome": nome.strip(),
                "endereco": endereco.strip(),
                "email": email_limpo,
                "celular_whatsapp": celular_limpo
            }).execute()
            cliente_id = novo_cliente.data[0]["id"]

        nova_os = supabase.table("ordens_servico").insert({
            "cliente_id": cliente_id,
            "modelo_computador": modelo.strip(),
            "problema_relatado": problema.strip(),
            "status": "Aberto"
        }).execute()

        os_id = nova_os.data[0]["id"]
        return f"✅ Ordem de Serviço Nº {os_id} cadastrada com sucesso!"

    except Exception as e:
        return f"❌ Erro ao registrar atendimento no banco: {str(e)}"

with gr.Blocks(title="TechFix - Balcão de Atendimento") as demo:
    gr.Markdown("# 🛠️ TechFix Informática")
    gr.Markdown("Preencha o formulário para abrir uma nova Ordem de Serviço.")

    with gr.Row():
        with gr.Column(scale=1):
            txt_nome = gr.Textbox(label="Nome do Cliente", placeholder="Ex: João da Silva")
            txt_email = gr.Textbox(label="E-mail", placeholder="joao@email.com")
            txt_celular = gr.Textbox(label="Celular/WhatsApp (somente números)", placeholder="19999998888")
            txt_endereco = gr.Textbox(label="Endereço Completo", placeholder="Rua das Flores, 123 - Centro")

        with gr.Column(scale=1):
            txt_modelo = gr.Textbox(label="Modelo do Equipamento", placeholder="Ex: Notebook Dell Inspiron 15")
            txt_problema = gr.Textbox(label="Problema Apresentado", placeholder="Descreva o defeito detalhadamente...", lines=5)

    btn_cadastrar = gr.Button("Cadastrar Ordem de Serviço", variant="primary")
    btn_limpar = gr.Button("Limpar Formulário")
    txt_resultado = gr.Textbox(label="Status do Envio", interactive=False)

    btn_cadastrar.click(
        fn=cadastrar_atendimento,
        inputs=[txt_nome, txt_endereco, txt_email, txt_celular, txt_modelo, txt_problema],
        outputs=txt_resultado
    )

    btn_limpar.click(
        fn=lambda: ("", "", "", "", "", "", ""),
        inputs=[],
        outputs=[txt_nome, txt_endereco, txt_email, txt_celular, txt_modelo, txt_problema, txt_resultado]
    )

if __name__ == "__main__":
    demo.launch(share=True)
