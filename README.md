# 💻 IT & Operations Intelligence Hub

> Um hub integrado de **Ciência de Dados** e **Governança de TI (ITIL 4)** desenvolvido para centralizar o monitoramento de ativos, gestão de incidentes (ITSM) e análise preditiva de infraestrutura.

---

## 🚀 Sobre o Projeto
O **IT & Operations Intelligence Hub** simula um ambiente corporativo moderno onde a operação de suporte, a governança de serviços e a engenharia de dados trabalham em conjunto. O projeto une a profundidade técnica da análise de dados com a visão estratégica de gestão e otimização de recursos (FinOps e SLA).

---

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Linguagem:** Python
* **Manipulação & Análise de Dados:** Pandas, NumPy
* **Banco de Dados & SQL:** SQLite (Modelagem Relacional)
* **Visualização & Dashboard Interativo:** Streamlit
* **Governança & Práticas de TI:** ITIL 4 (Métricas de MTTR, SLA e Capacidade)
* **Controle de Versão:** Git & GitHub

---

## 📂 Arquitetura do Repositório

```text
it-operations-hub/
│
├── data/                  # Banco de dados SQLite (it_operations.db)
├── notebooks/             # Jupyter Notebooks para análise exploratória
├── src/                   # Scripts de ETL, criação de banco e cálculo de KPIs
│   ├── create_db.py       # Estruturação das tabelas relacionais
│   ├── populate_db.py     # Geração de dados simulados (Mock Data)
│   └── kpi_calculator.py  # Script de métricas ITIL
├── dashboard/             # Aplicação web interativa
│   └── app.py             # Dashboard em Streamlit
├── docs/                  # Documentações e diagramas
└── README.md              # Documentação principal do projeto