import streamlit as st
import sqlite3
import pandas as pd
import os

# Configuração da Página
st.set_page_config(
    page_title="IT & Operations Intelligence Hub",
    page_icon="💻",
    layout="wide"
)

# Caminho do Banco de Dados
db_path = os.path.join("data", "it_operations.db")

@st.cache_data
def load_data():
    if not os.path.exists(db_path):
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    conn = sqlite3.connect(db_path)
    df_assets = pd.read_sql("SELECT * FROM assets", conn)
    df_incidents = pd.read_sql("SELECT * FROM incidents", conn)
    df_telemetry = pd.read_sql("SELECT * FROM telemetry", conn)
    conn.close()
    return df_assets, df_incidents, df_telemetry

df_assets, df_incidents, df_telemetry = load_data()

# Título Principal
st.title("💻 IT & Operations Intelligence Hub")
st.markdown("Painel executivo integrado de **Ciência de Dados** e **Governança de TI (ITIL 4)** para suporte à tomada de decisão.")

if df_assets.empty or df_incidents.empty:
    st.warning("Nenhum dado encontrado no banco. Execute os scripts de população do banco na pasta `src/`.")
else:
    # 📊 Métricas Principais (KPI Cards)
    st.subheader("📌 Indicadores Chave de Desempenho (KPIs)")
    
    total_assets = len(df_assets)
    total_incidents = len(df_incidents)
    
    # Cálculo de SLA
    df_incidents["sla_met"] = pd.to_numeric(df_incidents["sla_met"])
    sla_rate = (df_incidents["sla_met"].sum() / total_incidents) * 100 if total_incidents > 0 else 0
    
    # Cálculo de MTTR
    df_incidents["open_date"] = pd.to_datetime(df_incidents["open_date"])
    df_incidents["close_date"] = pd.to_datetime(df_incidents["close_date"])
    mttr = (df_incidents["close_date"] - df_incidents["open_date"]).dt.total_seconds().mean() / 3600

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Ativos", total_assets)
    col2.metric("Total de Incidentes", total_incidents)
    col3.metric("Taxa de Cumprimento de SLA", f"{sla_rate:.1f}%")
    col4.metric("MTTR Médio", f"{mttr:.1f} horas")

    st.divider()

    # 📈 Seção de Visualizações e Tabelas
    tab1, tab2, tab3 = st.tabs(["📊 Gestão de Incidentes (ITSM)", "🖥️ Infraestrutura & Telemetria", "📦 Inventário de Ativos"])

    with tab1:
        st.subheader("Histórico de Chamados e Prioridades")
        st.dataframe(df_incidents[["incident_id", "asset_id", "priority", "open_date", "close_date", "sla_met"]], use_container_width=True)

    with tab2:
        st.subheader("Métricas de Uso de Hardware")
        if not df_telemetry.empty:
            st.line_chart(df_telemetry.set_index("timestamp")[["cpu_usage", "memory_usage", "temperature"]])
            st.dataframe(df_telemetry, use_container_width=True)
        else:
            st.info("Sem dados de telemetria disponíveis.")

    with tab3:
        st.subheader("Ativos de TI Cadastrados")
        st.dataframe(df_assets, use_container_width=True)