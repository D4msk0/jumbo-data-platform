"""
aggregate.py
Pipeline stap 3: Silver → Gold
Berekent business metrics voor analytics en dashboards.
Gold = geaggregeerde, business-klare tabellen.
"""

from pathlib import Path
from pyspark.sql import functions as F
from spark_session import get_spark

# ── Paden ─────────────────────────────────────────────────────────────────────
BASE   = Path(__file__).parent.parent
SILVER = BASE / "silver"
GOLD   = BASE / "gold"


def run():
    spark = get_spark("Aggregate-Silver-Gold")

    # ── Inlezen ───────────────────────────────────────────────────────────────
    sales    = spark.read.format("delta").load(str(SILVER / "sales"))
    stores   = spark.read.format("delta").load(str(SILVER / "stores"))
    products = spark.read.format("delta").load(str(SILVER / "products"))

    # Verrijk sales met store- en productinfo
    sales_enriched = (
        sales
        .join(stores,   on="store_id",   how="left")
        .join(products, on="product_id", how="left")
    )

    # ── 1. Omzet per winkel ───────────────────────────────────────────────────
    print("\n→ Aggregatie: omzet per winkel")
    omzet_per_winkel = (
        sales_enriched
        .groupBy("store_id", "store_name", "city", "format")
        .agg(
            F.sum("revenue_eur").alias("totaal_omzet_eur"),
            F.count("transaction_id").alias("aantal_transacties"),
            F.avg("revenue_eur").alias("gemiddeld_bedrag_eur"),
        )
        .withColumn("totaal_omzet_eur",      F.round("totaal_omzet_eur", 2))
        .withColumn("gemiddeld_bedrag_eur",  F.round("gemiddeld_bedrag_eur", 2))
        .orderBy(F.desc("totaal_omzet_eur"))
    )
    omzet_per_winkel.write.format("delta").mode("overwrite").save(str(GOLD / "omzet_per_winkel"))
    print(f"  ✓ {omzet_per_winkel.count()} winkels weggeschreven naar gold/omzet_per_winkel")

    # ── 2. Omzet per categorie ────────────────────────────────────────────────
    print("\n→ Aggregatie: omzet per productcategorie")
    omzet_per_categorie = (
        sales_enriched
        .groupBy("category")
        .agg(
            F.sum("revenue_eur").alias("totaal_omzet_eur"),
            F.sum("quantity").alias("totaal_aantal_verkocht"),
            F.countDistinct("product_id").alias("aantal_producten"),
        )
        .withColumn("totaal_omzet_eur", F.round("totaal_omzet_eur", 2))
        .orderBy(F.desc("totaal_omzet_eur"))
    )
    omzet_per_categorie.write.format("delta").mode("overwrite").save(str(GOLD / "omzet_per_categorie"))
    print(f"  ✓ {omzet_per_categorie.count()} categorieën weggeschreven naar gold/omzet_per_categorie")

    # ── 3. Omzet per maand ────────────────────────────────────────────────────
    print("\n→ Aggregatie: omzet per maand")
    omzet_per_maand = (
        sales_enriched
        .groupBy("year", "month")
        .agg(
            F.sum("revenue_eur").alias("totaal_omzet_eur"),
            F.count("transaction_id").alias("aantal_transacties"),
        )
        .withColumn("totaal_omzet_eur", F.round("totaal_omzet_eur", 2))
        .orderBy("year", "month")
    )
    omzet_per_maand.write.format("delta").mode("overwrite").save(str(GOLD / "omzet_per_maand"))
    print(f"  ✓ {omzet_per_maand.count()} maanden weggeschreven naar gold/omzet_per_maand")

    # ── 4. Top producten ──────────────────────────────────────────────────────
    print("\n→ Aggregatie: top producten")
    top_producten = (
        sales_enriched
        .groupBy("product_id", "product_name", "category", "price_eur")
        .agg(
            F.sum("revenue_eur").alias("totaal_omzet_eur"),
            F.sum("quantity").alias("totaal_aantal_verkocht"),
        )
        .withColumn("totaal_omzet_eur", F.round("totaal_omzet_eur", 2))
        .orderBy(F.desc("totaal_omzet_eur"))
    )
    top_producten.write.format("delta").mode("overwrite").save(str(GOLD / "top_producten"))
    print(f"  ✓ {top_producten.count()} producten weggeschreven naar gold/top_producten")

    print("\n✓ Aggregate pipeline voltooid — alle metrics staan in gold/\n")
    spark.stop()


if __name__ == "__main__":
    run()