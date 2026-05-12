"""
catalog_setup.py
Simuleert een Unity Catalog-structuur met Spark SQL.
In productie (Databricks) zou dit via de Unity Catalog API lopen.
Lokaal gebruiken we Spark SQL om dezelfde hiërarchie aan te tonen:
    catalog → schema (database) → tabel
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "pipelines"))
from spark_session import get_spark

BASE  = Path(__file__).parent.parent
GOLD  = BASE / "gold"


CATALOG = "jumbo_catalog"
SCHEMAS = {
    "retail":     "Verkoopdata en winkelinformatie",
    "products":   "Productcatalogus en categorieën",
    "analytics":  "Geaggregeerde business metrics",
}

# Tabel → (schema, pad, beschrijving, toegang)
TABLES = {
    "omzet_per_winkel": (
        "analytics",
        GOLD / "omzet_per_winkel",
        "Totale omzet, aantal transacties en gemiddeld bedrag per filiaal",
        ["data_analyst", "management"],
    ),
    "omzet_per_categorie": (
        "analytics",
        GOLD / "omzet_per_categorie",
        "Omzet en verkoopvolume per productcategorie",
        ["data_analyst", "management"],
    ),
    "omzet_per_maand": (
        "analytics",
        GOLD / "omzet_per_maand",
        "Maandelijkse omzetontwikkeling over 2024",
        ["data_analyst", "management"],
    ),
    "top_producten": (
        "analytics",
        GOLD / "top_producten",
        "Bestverkopende producten op omzet en volume",
        ["data_analyst", "category_manager"],
    ),
    "stores": (
        "retail",
        BASE / "silver" / "stores",
        "Filiaalinformatie: locatie, formaat en oppervlakte",
        ["data_analyst", "logistics"],
    ),
    "sales": (
        "retail",
        BASE / "silver" / "sales",
        "Ruwe transactiedata na cleaning (Silver-laag)",
        ["data_engineer"],
    ),
    "products": (
        "products",
        BASE / "silver" / "products",
        "Productinformatie: categorie, prijs en gewicht",
        ["data_analyst", "category_manager"],
    ),
}


def run():
    spark = get_spark("CatalogSetup")

    print(f"\n── Catalog: {CATALOG} ──────────────────────────────────────────")

    # Schemas aanmaken
    for schema, beschrijving in SCHEMAS.items():
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {schema} COMMENT '{beschrijving}'")
        print(f"\n  Schema: {schema}")
        print(f"  └─ {beschrijving}")

        # Tabellen registreren die bij dit schema horen
        for tabel, (schema_naam, pad, omschrijving, rollen) in TABLES.items():
            if schema_naam != schema:
                continue

            spark.sql(f"""
                CREATE TABLE IF NOT EXISTS {schema}.{tabel}
                USING delta
                LOCATION '{pad}'
                COMMENT '{omschrijving}'
            """)

            print(f"     ├─ {tabel}")
            print(f"     │   Omschrijving : {omschrijving}")
            print(f"     │   Toegang      : {', '.join(rollen)}")

    # Overzicht van alle geregistreerde tabellen
    print("\n── Geregistreerde tabellen ─────────────────────────────────────")
    for schema in SCHEMAS:
        tabellen = spark.sql(f"SHOW TABLES IN {schema}").collect()
        for rij in tabellen:
            print(f"  {schema}.{rij.tableName}")

    print("\n✓ Catalog setup voltooid\n")
    spark.stop()


if __name__ == "__main__":
    run()