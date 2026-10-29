import sqlite3
import pandas as pd
import os

def calculate_it_kpis():
    db_path = os.path.join("data", "it_operations.db")
    if not os.path.exists(db_path):
        print("Banco de dados não encontrado! Execute o populate_db.py primeiro.")
        return

    # Conectar ao SQLite
    conn = sqlite3.connect(db_path)

    # Carregar as tabelas em DataFrames do Pandas
    df_incidents = pd.read_sql("SELECT * FROM incidents", conn)
    df_telemetry = pd.read_sql("SELECT * FROM telemetry", conn)
    df_assets = pd.read_sql("SELECT * FROM assets", conn)

    conn.close()

    print("=" * 60)
    print(" 📊 RELATÓRIO EXECUTIVO DE KPIs DE TI & GOVERNANÇA (ITIL 4) ")
    print("=" * 60)

    # 1. Governança de Incidentes & SLA
    if not df_incidents.empty:
        total_incidents = len(df_incidents)
        sla_met_count = df_incidents["sla_met"].sum()
        sla_compliance_rate = (sla_met_count / total_incidents) * 100

        # Cálculo do MTTR (Mean Time to Repair em horas)
        df_incidents["open_date"] = pd.to_datetime(df_incidents["open_date"])
        df_incidents["close_date"] = pd.to_datetime(df_incidents["close_date"])
        df_incidents["repair_time_hours"] = (df_incidents["close_date"] - df_incidents["open_date"]).dt.total_seconds() / 3600
        mean_tt_repair = df_incidents["repair_time_hours"].mean()

        print(f"\n[ITSM / Gestão de Incidentes & Nível de Serviço]")
        print(f"• Total de Incidentes Registrados : {total_incidents}")
        print(f"• Taxa de Cumprimento de SLA      : {sla_compliance_rate:.2f}%")
        print(f"• MTTR (Tempo Médio de Reparo)    : {mean_tt_repair:.2f} horas")

    # 2. Telemetria e Capacidade de Hardware
    if not df_telemetry.empty:
        avg_cpu = df_telemetry["cpu_usage"].mean()
        avg_mem = df_telemetry["memory_usage"].mean()
        avg_temp = df_telemetry["temperature"].mean()

        print(f"\n[Infraestrutura / Monitoramento de Capacidade]")
        print(f"• Uso Médio de CPU                : {avg_cpu:.2f}%")
        print(f"• Uso Médio de Memória RAM        : {avg_mem:.2f}%")
        print(f"• Temperatura Média dos Ativos    : {avg_temp:.2f} °C")

    # 3. Gestão de Ativos
    if not df_assets.empty:
        total_assets = len(df_assets)
        active_assets = len(df_assets[df_assets["status"] == "Ativo"])
        print(f"\n[Gestão de Ativos / IT Asset Management]")
        print(f"• Total de Ativos Cadastrados     : {total_assets}")
        print(f"• Ativos Operacionais (Ativos)    : {active_assets}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    calculate_it_kpis()