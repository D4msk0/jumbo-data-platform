"""
transform.py
Pipeline stap 2: Bronze → Silver
Schoont de data op en corrigeert datatypes.
Silver = betrouwbare, getypeerde data klaar voor analyse.
"""

from pathlib import Path
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from spark_session import get_spark

# ── Paden ─────────────────────────────────────────────────────────────────────
BASE    = Path(__file__).parent.parent
BRONZE  = BASE / "bronze"
SILVER  = BASE / "silver"


def transform_stores(df: DataFrame) -> DataFrame:
    """Opschonen en verrijken van winkeldata."""
    return (
        df
        .dropDuplicates(["store_id"])
        .filter(F.col("store_id").isNotNull())
        .withColumn("floor_area_m2", F.col("floor_area_m2").cast("integer"))
        .withColumn("opening_year",  F.col("opening_year").cast("integer"))
        .withColumn("ingested_at",   F.current_timestamp())
    )


def transform_products(df: DataFrame) -> DataFrame:
    """Opschonen en verrijken van productdata."""
    return (
        df
        .dropDuplicates(["product_id"])
        .filter(F.col("product_id").isNotNull())
        .withColumn("price_eur",      F.col("price_eur").cast("double"))
        .withColumn("weight_gram",    F.col("weight_gram").cast("integer"))
        .withColumn("is_jumbo_huismerk", F.col("is_jumbo_huismerk").cast("boolean"))
        .withColumn("ingested_at",    F.current_timestamp())
    )


def transform_sales(df: DataFrame) -> DataFrame:
    """Opschonen en verrijken van verkoopdata."""
    return (
        df
        .dropDuplicates(["transaction_id"])
        .filter(F.col("transaction_id").isNotNull())
        .filter(F.col("revenue_eur") >= 0)
        .withColumn("order_date",     F.to_date(F.col("order_date"), "yyyy-MM-dd"))
        .withColumn("quantity",       F.col("quantity").cast("integer"))
        .withColumn("unit_price_eur", F.col("unit_price_eur").cast("double"))
        .withColumn("discount_pct",   F.col("discount_pct").cast("double"))
        .withColumn("revenue_eur",    F.col("revenue_eur").cast("double"))
        .withColumn("year",           F.year(F.col("order_date")))
        .withColumn("month",          F.month(F.col("order_date")))
        .withColumn("ingested_at",    F.current_timestamp())
    )


def run():
    spark = get_spark("Transform-Bronze-Silver")

    datasets = [
        ("stores",   transform_stores),
        ("products", transform_products),
        ("sales",    transform_sales),
    ]

    for name, transform_fn in datasets:
        print(f"\n→ Transform: bronze/{name} → silver/{name}")

        df_bronze = spark.read.format("delta").load(str(BRONZE / name))
        df_silver = transform_fn(df_bronze)

        count_before = df_bronze.count()
        count_after  = df_silver.count()

        df_silver.write.format("delta").mode("overwrite").save(str(SILVER / name))

        print(f"  Rijen voor  : {count_before}")
        print(f"  Rijen na    : {count_after}")
        if count_before != count_after:
            print(f"  ⚠ {count_before - count_after} rijen verwijderd (duplicaten/nulls)")
        print(f"  ✓ Weggeschreven naar silver/{name}")

    print("\n✓ Transform pipeline voltooid — alle data staat in silver/\n")
    spark.stop()


if __name__ == "__main__":
    run()