"""
app.py
Self-service analytics dashboard voor het Jumbo Data Platform.
Visualiseert de Gold-laag tabellen via Streamlit.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "pipelines"))

import streamlit as st
import pandas as pd
import plotly.express as px
from spark_session import get_spark

# ── Pagina configuratie ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jumbo Data Platform",
    page_icon="🛒",
    layout="wide",
)

BASE = Path(__file__).parent.parent
GOLD = BASE / "gold"


# ── Data laden (gecached) ─────────────────────────────────────────────────────
@st.cache_data
def load_gold_tables() -> dict[str, pd.DataFrame]:
    spark = get_spark("Dashboard")
    tabellen = {}
    for naam in ["omzet_per_winkel", "omzet_per_categorie", "omzet_per_maand", "top_producten"]:
        tabellen[naam] = spark.read.format("delta").load(str(GOLD / naam)).toPandas()
    spark.stop()
    return tabellen


# ── Layout ────────────────────────────────────────────────────────────────────
st.title("🛒 Jumbo Data Platform — Analytics Dashboard")
st.caption("Self-service analytics op basis van de Gold-laag | Data: 2024")

with st.spinner("Data laden..."):
    data = load_gold_tables()

omzet_winkel     = data["omzet_per_winkel"]
omzet_categorie  = data["omzet_per_categorie"]
omzet_maand      = data["omzet_per_maand"]
top_producten    = data["top_producten"]

# ── KPI's ─────────────────────────────────────────────────────────────────────
st.subheader("📊 KPI's 2024")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Totale omzet",        f"€ {omzet_winkel['totaal_omzet_eur'].sum():,.0f}")
col2.metric("Aantal transacties",  f"{omzet_winkel['aantal_transacties'].sum():,}")
col3.metric("Aantal filialen",     f"{len(omzet_winkel)}")
col4.metric("Gem. transactiebedrag", f"€ {omzet_winkel['gemiddeld_bedrag_eur'].mean():,.2f}")

st.divider()

# ── Omzet per maand ───────────────────────────────────────────────────────────
st.subheader("📈 Omzet per maand")
omzet_maand["periode"] = omzet_maand["month"].apply(lambda m: f"{m:02d}")
fig_maand = px.bar(
    omzet_maand.sort_values("month"),
    x="periode",
    y="totaal_omzet_eur",
    labels={"periode": "Maand", "totaal_omzet_eur": "Omzet (€)"},
    color_discrete_sequence=["#FFD700"],
)
fig_maand.update_layout(showlegend=False)
st.plotly_chart(fig_maand, use_container_width=True)

st.divider()

# ── Omzet per categorie & per winkel ─────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🏷️ Omzet per categorie")
    fig_cat = px.pie(
        omzet_categorie,
        names="category",
        values="totaal_omzet_eur",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    st.subheader("🏪 Omzet per filiaal")
    fig_winkel = px.bar(
        omzet_winkel.sort_values("totaal_omzet_eur"),
        x="totaal_omzet_eur",
        y="store_name",
        orientation="h",
        labels={"totaal_omzet_eur": "Omzet (€)", "store_name": "Filiaal"},
        color_discrete_sequence=["#FFD700"],
    )
    fig_winkel.update_layout(showlegend=False)
    st.plotly_chart(fig_winkel, use_container_width=True)

st.divider()

# ── Top producten ─────────────────────────────────────────────────────────────
st.subheader("🥇 Top 10 producten op omzet")
top10 = top_producten.head(10)[["product_name", "category", "price_eur", "totaal_omzet_eur", "totaal_aantal_verkocht"]]
top10.columns = ["Product", "Categorie", "Prijs (€)", "Omzet (€)", "Verkocht"]
st.dataframe(top10, use_container_width=True, hide_index=True)