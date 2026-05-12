"""
spark_session.py
Centrale configuratie van de Spark-sessie met Delta Lake support.
Importeer get_spark() in alle andere pipeline-scripts.
"""

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

def get_spark(app_name: str = "JumboDataPlatform") -> SparkSession:
    """
    Maak een Spark-sessie aan met Delta Lake support.
    Als er al een actieve sessie is, wordt die hergebruikt.
    """
    builder = (
        SparkSession.builder
        .appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.sql.shuffle.partitions", "4")   # laag houden voor lokaal gebruik
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    # Minder ruis in de logs
    spark.sparkContext.setLogLevel("WARN")

    return spark


if __name__ == "__main__":
    # Snelle smoke test: werkt Spark + Delta?
    spark = get_spark("SmokeTest")

    print(f"\n✓ Spark versie : {spark.version}")
    print(f"✓ App naam     : {spark.sparkContext.appName}")

    # Schrijf een mini Delta-tabel en lees hem terug
    df = spark.createDataFrame([(1, "Jumbo"), (2, "DataPlatform")], ["id", "naam"])
    df.write.format("delta").mode("overwrite").save("/tmp/smoke_test_delta")

    df_terug = spark.read.format("delta").load("/tmp/smoke_test_delta")
    print(f"✓ Delta Lake   : {df_terug.count()} rijen succesvol geschreven en gelezen\n")

    spark.stop()