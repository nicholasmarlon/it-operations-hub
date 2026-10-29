import sqlite3
import os

def create_database():
    # Garante que a pasta 'data' existe para receber o arquivo do banco
    os.makedirs("data", exist_ok=True)
    db_path = os.path.join("data", "it_operations.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela 1: Ativos de TI (Hardware e Inventário)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            asset_id TEXT PRIMARY KEY,
            asset_type TEXT NOT NULL,
            location TEXT NOT NULL,
            purchase_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Tabela 2: Incidentes de Suporte (Governança ITSM & SLA)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id TEXT PRIMARY KEY,
            asset_id TEXT,
            open_date TEXT,
            close_date TEXT,
            priority TEXT,
            sla_met INTEGER,
            FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
        )
    """)

    # Tabela 3: Telemetria de Desempenho e Saúde do Ativo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            telemetry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT,
            timestamp TEXT,
            cpu_usage REAL,
            memory_usage REAL,
            temperature REAL,
            battery_health REAL,
            FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"Banco de dados SQLite 'it_operations.db' criado com sucesso em: {db_path}")

if __name__ == "__main__":
    create_database()