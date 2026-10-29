import sqlite3
import os
import random
from datetime import datetime, timedelta

def populate_database():
    db_path = os.path.join("data", "it_operations.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Inserir Ativos de TI (Assets)
    asset_types = ["Notebook Dell", "Servidor Rack", "Workstation HP", "Notebook Lenovo"]
    locations = ["Matriz - SP", "Filial - RJ", "Centro de Distribuição - ES"]
    statuses = ["Ativo", "Em Manutenção", "Ativo"]

    assets_data = []
    for i in range(1, 16):  # 15 ativos
        asset_id = f"AST-{100 + i}"
        atype = random.choice(asset_types)
        loc = random.choice(locations)
        p_date = (datetime.now() - timedelta(days=random.randint(100, 700))).strftime("%Y-%m-%d")
        status = random.choice(statuses)
        assets_data.append((asset_id, atype, loc, p_date, status))

    cursor.executemany("""
        INSERT OR IGNORE INTO assets (asset_id, asset_type, location, purchase_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, assets_data)

    # 2. Inserir Incidentes (ITSM & SLA)
    priorities = ["Baixa", "Média", "Alta", "Crítica"]
    incidents_data = []
    
    for j in range(1, 50):  # 50 incidentes simulados
        inc_id = f"INC-{5000 + j}"
        asset_id = random.choice(assets_data)[0]
        open_dt = datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 10))
        close_dt = open_dt + timedelta(hours=random.randint(1, 48))
        priority = random.choice(priorities)
        
        # Regra simples de SLA: prioridade alta/crítica exige resolução mais rápida
        sla_met = 1 if (close_dt - open_dt).total_seconds() / 3600 <= 24 else 0

        incidents_data.append((
            inc_id, asset_id, 
            open_dt.strftime("%Y-%m-%d %H:%M:%S"), 
            close_dt.strftime("%Y-%m-%d %H:%M:%S"), 
            priority, sla_met
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO incidents (incident_id, asset_id, open_date, close_date, priority, sla_met)
        VALUES (?, ?, ?, ?, ?, ?)
    """, incidents_data)

    # 3. Inserir Telemetria de Hardware
    telemetry_data = []
    for asset in assets_data:
        a_id = asset[0]
        for k in range(5):  # 5 leituras por ativo
            ts = (datetime.now() - timedelta(days=k)).strftime("%Y-%m-%d %H:%M:%S")
            cpu = round(random.uniform(15.0, 95.0), 2)
            mem = round(random.uniform(30.0, 90.0), 2)
            temp = round(random.uniform(45.0, 85.0), 2)
            battery = round(random.uniform(60.0, 100.0), 2)
            
            telemetry_data.append((a_id, ts, cpu, mem, temp, battery))

    cursor.executemany("""
        INSERT INTO telemetry (asset_id, timestamp, cpu_usage, memory_usage, temperature, battery_health)
        VALUES (?, ?, ?, ?, ?, ?)
    """, telemetry_data)

    conn.commit()
    conn.close()
    print("Banco de dados populado com sucesso com dados simulados de TI!")

if __name__ == "__main__":
    populate_database()