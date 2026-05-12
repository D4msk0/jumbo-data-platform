"""
ingest.py
Pipeline stap 1: Landing Zone → Bronze
Leest ruwe CSV-bestanden in en schrijft ze weg als Delta-tabellen.
Bronze = onbewerkte data, exact zoals ontvangen, maar in Delta-formaat.
"""

from pathlib import Path
from pyspark.sql import DataFrame
from spark_session import get_spark

# ── Paden ─────────────────────────────────────────────────────────────────────
BASE        = Path(__file__).parent.parent
LANDING     = BASE / "landing_zone"
BRONZE      = BASE / "bronze"


def ingest_csv(spark, source: Path, destination: Path, name: str) -> DataFrame:
    """Lees een CSV in vanuit de landing zone en schrijf weg als Delta."""
    print(f"\n→ Ingest: {source.relative_to(BASE)}")

    df = spark.read.csv(
        str(source),
        header=True,
        inferSchema=True,
    )

    print(f"  Kolommen : {df.columns}")
    print(f"  Rijen    : {df.count()}")

    df.write.format("delta").mode("overwrite").save(str(destination))
    print(f"  ✓ Weggeschreven naar bronze/{name}")

    return df


def run():
    spark = get_spark("Ingest-LandingZone-Bronze")

    ingest_csv(
        spark,
        source=LANDING / "stores" / "stores.csv",
        destination=BRONZE / "stores",
        name="stores",
    )

    ingest_csv(
        spark,
        source=LANDING / "products" / "products.csv",
        destination=BRONZE / "products",
        name="products",
    )

    ingest_csv(
        spark,
        source=LANDING / "sales" / "sales_2024.csv",
        destination=BRONZE / "sales",
        name="sales",
    )

    print("\n✓ Ingest pipeline voltooid — alle data staat in bronze/\n")
    spark.stop()


if __name__ == "__main__":
    run()