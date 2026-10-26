import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

st.set_page_config(page_title="TechFix - Gestão de O.S.", layout="wide", page_icon="💻")

supabase_url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
supabase_key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))

if not supabase_url or not supabase_key:
    st.error("Credenciais do Supabase não encontradas.")
    st.stop()

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(supabase_url, supabase_key)

supabase = get_supabase_client()

STATUS_LIST = ['Aberto', 'Em análise', 'Aguardando peça', 'Concluído', 'Entregue']

def carregar_dados():
    try:
        response = supabase.table("ordens_servico").select(
            "id, modelo_computador, problema_relatado, status, data_abertura, data_atualizacao, cliente_id, clientes(id, nome, email, celular_whatsapp, endereco)"
        ).order("id", desc=True).execute()
        
        registros = []
        for item in response.data:
            cli = item.get("clientes") or {}
            registros.append({
                "OS": item.get("id"),
                "Cliente ID": cli.get("id"),
                "Cliente": cli.get("nome"),
                "E-mail": cli.get("email"),
                "WhatsApp": cli.get("celular_whatsapp"),
                "Endereço": cli.get("endereco"),
                "Equipamento": item.get("modelo_computador"),
                "Problema": item.get("problema_relatado"),
                "Status": item.get("status"),
                "Data Abertura": item.get("data_abertura"),
                "Última Atualização": item.get("data_atualizacao")
            })
        return pd.DataFrame(registros)
    except Exception as e:
        st.error(f"Erro ao buscar registros: {e}")
        return pd.DataFrame()

df_ordens = carregar_dados()

# Sidebar
st.sidebar.title("🔍 Filtros de Busca")
filtro_nome = st.sidebar.text_input("Filtrar por Cliente:")
filtro_email = st.sidebar.text_input("Filtrar por E-mail:")
filtro_status = st.sidebar.multiselect("Filtrar por Status:", STATUS_LIST, default=[])

df_filtrado = df_ordens.copy()
if not df_filtrado.empty:
    if filtro_nome:
        df_filtrado = df_filtrado[df_filtrado["Cliente"].str.contains(filtro_nome, case=False, na=False)]
    if filtro_email:
        df_filtrado = df_filtrado[df_filtrado["E-mail"].str.contains(filtro_email, case=False, na=False)]
    if filtro_status:
        df_filtrado = df_filtrado[df_filtrado["Status"].isin(filtro_status)]

st.title("💻 Painel Administrativo — TechFix Informática")

tab_consultar, tab_cadastrar, tab_editar_excluir, tab_indicadores = st.tabs([
    "📋 Consultar Ordens", 
    "➕ Nova O.S.", 
    "✏️ Editar / Excluir", 
    "📊 Indicadores"
])

with tab_consultar:
    st.subheader("Ordens de Serviço Registradas")
    if df_filtrado.empty:
        st.info("Nenhuma ordem de serviço encontrada.")
    else:
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
        csv_data = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Exportar Dados Filtrados (CSV)",
            data=csv_data,
            file_name="ordens_servico_techfix.csv",
            mime="text/csv"
        )

with tab_cadastrar:
    st.subheader("Abertura Manual de Ordem de Serviço")
    with st.form("form_cadastrar_os", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            novo_nome = st.text_input("Nome do Cliente*")
            novo_email = st.text_input("E-mail*")
            novo_celular = st.text_input("Celular/WhatsApp (números)*")
            novo_endereco = st.text_input("Endereço Completo*")
        with col2:
            novo_modelo = st.text_input("Modelo do Equipamento*")
            novo_status = st.selectbox("Status Inicial", STATUS_LIST, index=0)
            novo_problema = st.text_area("Problema Relatado*")

        if st.form_submit_button("Gravar no Banco"):
            if not all([novo_nome, novo_email, novo_celular, novo_endereco, novo_modelo, novo_problema]):
                st.warning("Preencha todos os campos obrigatórios.")
            else:
                try:
                    res_cli = supabase.table("clientes").select("id").eq("email", novo_email.strip().lower()).execute()
                    if res_cli.data:
                        c_id = res_cli.data[0]["id"]
                    else:
                        insert_cli = supabase.table("clientes").insert({
                            "nome": novo_nome.strip(),
                            "email": novo_email.strip().lower(),
                            "celular_whatsapp": novo_celular.strip(),
                            "endereco": novo_endereco.strip()
                        }).execute()
                        c_id = insert_cli.data[0]["id"]

                    supabase.table("ordens_servico").insert({
                        "cliente_id": c_id,
                        "modelo_computador": novo_modelo.strip(),
                        "problema_relatado": novo_problema.strip(),
                        "status": novo_status
                    }).execute()
                    st.success("Ordem de Serviço criada com sucesso!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Erro ao cadastrar: {ex}")

with tab_editar_excluir:
    st.subheader("Gerenciamento de Registros")
    if df_ordens.empty:
        st.info("Nenhuma ordem disponível para edição.")
    else:
        opcoes_os = df_ordens["OS"].tolist()
        os_selecionada = st.selectbox("Selecione a OS pelo ID:", opcoes_os)
        linha = df_ordens[df_ordens["OS"] == os_selecionada].iloc[0]
        
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            st.markdown("##### Dados do Cliente")
            ed_nome = st.text_input("Nome", value=linha["Cliente"])
            ed_email = st.text_input("E-mail", value=linha["E-mail"])
            ed_whats = st.text_input("WhatsApp", value=linha["WhatsApp"])
            ed_end = st.text_input("Endereço", value=linha["Endereço"])
        
        with col_ed2:
            st.markdown("##### Dados do Chamado")
            ed_status = st.selectbox("Status", STATUS_LIST, index=STATUS_LIST.index(linha["Status"]))
            ed_modelo = st.text_input("Modelo", value=linha["Equipamento"])
            ed_prob = st.text_area("Problema", value=linha["Problema"])

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("💾 Salvar Alterações", use_container_width=True):
                try:
                    supabase.table("clientes").update({
                        "nome": ed_nome, "email": ed_email,
                        "celular_whatsapp": ed_whats, "endereco": ed_end
                    }).eq("id", int(linha["Cliente ID"])).execute()

                    supabase.table("ordens_servico").update({
                        "status": ed_status,
                        "modelo_computador": ed_modelo,
                        "problema_relatado": ed_prob
                    }).eq("id", int(os_selecionada)).execute()

                    st.success("Atualizado com sucesso!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Erro: {ex}")

        with col_b2:
            st.markdown("##### Zona de Exclusão")
            confirmacao = st.checkbox(f"Confirmar exclusão da OS #{os_selecionada}")
            if st.button("🗑️ Excluir O.S.", type="primary", disabled=not confirmacao, use_container_width=True):
                try:
                    supabase.table("ordens_servico").delete().eq("id", int(os_selecionada)).execute()
                    st.success(f"OS #{os_selecionada} excluída!")
                    st.rerun()
                except Exception as ex:
                    st.error(f"Erro ao remover: {ex}")

with tab_indicadores:
    st.subheader("Métricas Gerais")
    if df_ordens.empty:
        st.info("Sem dados para indicadores.")
    else:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total de Chamados", len(df_ordens))
        col_m2.metric("Abertos", len(df_ordens[df_ordens["Status"] == "Aberto"]))
        col_m3.metric("Em Análise / Aguardando", len(df_ordens[df_ordens["Status"].isin(["Em análise", "Aguardando peça"])]))
        col_m4.metric("Finalizados", len(df_ordens[df_ordens["Status"].isin(["Concluído", "Entregue"])]))

        st.markdown("---")
        st.subheader("Distribuição por Status")
        contagem = df_ordens["Status"].value_counts().reindex(STATUS_LIST, fill_value=0)
        st.bar_chart(contagem)
