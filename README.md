# 🏗️ Jumbo Data Platform — Portfolio Project

> Een hands-on dataplatform gebouwd met **Delta Lake**, **PySpark** en **Databricks-concepten**,
> als demonstratie van vaardigheden voor de rol van **Junior Data Platform Engineer bij Jumbo**.

---

## 🎯 Doel van dit project

Dit project bootst een moderne **Lakehouse-architectuur** na, vergelijkbaar met het dataplatform
dat Jumbo inzet op Azure & Databricks. Het laat zien dat ik in staat ben om:

- Een schaalbaar dataplatform op te zetten met de **Medallion Architecture** (Bronze → Silver → Gold)
- **Data Landing Zones** in te richten en te beheren
- **Data governance** toe te passen (Unity Catalog-concepten: catalogi, schema's, rechten)
- **Self-service analytics** mogelijk te maken via SQL en dashboards
- Platform performance te monitoren en incidenten te signaleren

---

## 📐 Architectuur

```
landing_zone/          ← Ruwe brondata (CSV, JSON) — de "ingang" van het platform
    └── sales/
    └── products/
    └── stores/

bronze/                ← Onbewerkte data, omgezet naar Delta-formaat (immutable)
silver/                ← Gecleande, getransformeerde data
gold/                  ← Business-klare tabellen voor analytics & dashboards

pipelines/             ← PySpark-scripts voor elke laag
    └── ingest.py          # Landing Zone → Bronze
    └── transform.py       # Bronze → Silver
    └── aggregate.py       # Silver → Gold

governance/            ← Data governance: rechten, catalog-structuur, data dictionary
    └── catalog_setup.py
    └── access_policy.md
    └── data_dictionary.md

monitoring/            ← Platform health, logging, alerting
    └── pipeline_monitor.py

dashboard/             ← Self-service analytics & visualisaties
    └── app.py             # Streamlit dashboard
```

---

## 🗺️ Stappenplan

De onderstaande stappen worden één voor één doorlopen. Elke stap resulteert in een commit.

| Stap | Onderwerp | Status |
|------|-----------|--------|
| 1 | Project initialiseren: Git, mappenstructuur, `requirements.txt` | ✅ Klaar |
| 2 | Synthetische brondata genereren (sales, products, stores) | ✅ Klaar |
| 3 | Spark-sessie opzetten met Delta Lake support | ✅ Klaar |
| 4 | Ingest pipeline: Landing Zone → Bronze | ✅ Klaar |
| 5 | Transform pipeline: Bronze → Silver (cleaning & typing) | ✅ Klaar |
| 6 | Aggregate pipeline: Silver → Gold (business metrics) | ✅ Klaar |
| 7 | Data governance: catalog-structuur en toegangsbeleid documenteren | 🔄 Bezig |
| 8 | Monitoring: pipeline logging en basismetrics | ⬜ Todo |
| 9 | Self-service dashboard met Streamlit | ⬜ Todo |
| 10 | Databricks Community Edition: project draaien in de cloud | ⬜ Todo |

---

## 🛠️ Tech Stack

| Tool | Waarvoor |
|------|----------|
| Python 3.11+ | Primaire taal |
| PySpark + Delta Lake | Gedistribueerde dataverwerking & opslag |
| SQL (Spark SQL) | Data queries & transformaties |
| Streamlit | Self-service analytics dashboard |
| Databricks Community Edition | Cloudomgeving (later in het project) |
| Git + GitHub | Versiebeheer |

---

## 🚀 Lokaal opstarten

> ⚠️ *Wordt ingevuld naarmate het project vordert.*

```bash
# Stap 1: clone het project
git clone https://github.com/<jouw-gebruikersnaam>/jumbo-data-platform.git
cd jumbo-data-platform

# Stap 2: installeer dependencies
pip install -r requirements.txt

# Stap 3: draai de pipeline
python pipelines/ingest.py
python pipelines/transform.py
python pipelines/aggregate.py

# Stap 4: start het dashboard
streamlit run dashboard/app.py
```

---

## 📚 Concepten die dit project aantoont

- **Medallion Architecture** — gelaagde dataopslag (Bronze/Silver/Gold)
- **Delta Lake** — ACID-transacties, time travel, schema enforcement
- **Data Landing Zones** — gecontroleerde ingang voor brondata
- **Unity Catalog (conceptueel)** — catalog → schema → tabel hiërarchie met rechten
- **Self-Service Analytics** — eindgebruikers kunnen zelf data bevragen
- **Pipeline Monitoring** — zichtbaarheid op platformgezondheid
- **Data Governance** — wie mag wat zien en gebruiken

---

## 👤 Over dit project

Gebouwd door **Maarten en Claude** als portfolio ter ondersteuning van de sollicitatie voor
**Junior Data Platform Engineer** bij **Jumbo Supermarkten**.

---

*🔄 Dit README wordt bijgewerkt na elke voltooide stap.*
