"""
pipeline_monitor.py
Monitort de gezondheid van het dataplatform.
Controleert of alle Delta-tabellen bestaan, rijen bevatten,
en of de data recent genoeg is.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "pipelines"))

from datetime import date
from pyspark.sql import functions as F
from spark_session import get_spark

# ── Paden ─────────────────────────────────────────────────────────────────────
BASE   = Path(__file__).parent.parent
BRONZE = BASE / "bronze"
SILVER = BASE / "silver"
GOLD   = BASE / "gold"

# ── Te controleren tabellen ───────────────────────────────────────────────────
CHECKS = [
    ("bronze", "stores",              BRONZE / "stores"),
    ("bronze", "products",            BRONZE / "products"),
    ("bronze", "sales",               BRONZE / "sales"),
    ("silver", "stores",              SILVER / "stores"),
    ("silver", "products",            SILVER / "products"),
    ("silver", "sales",               SILVER / "sales"),
    ("gold",   "omzet_per_winkel",    GOLD   / "omzet_per_winkel"),
    ("gold",   "omzet_per_categorie", GOLD   / "omzet_per_categorie"),
    ("gold",   "omzet_per_maand",     GOLD   / "omzet_per_maand"),
    ("gold",   "top_producten",       GOLD   / "top_producten"),
]


def check_table(spark, laag: str, naam: str, pad: Path) -> dict:
    """Controleer of een Delta-tabel bestaat en rijen bevat."""
    result = {
        "laag":   laag,
        "tabel":  naam,
        "status": "❌ FOUT",
        "rijen":  0,
        "detail": "",
    }

    if not pad.exists():
        result["detail"] = "Map bestaat niet"
        return result

    try:
        df = spark.read.format("delta").load(str(pad))
        count = df.count()

        if count == 0:
            result["status"] = "⚠️  LEEG"
            result["detail"] = "Tabel bestaat maar bevat geen rijen"
        else:
            result["status"] = "✅ OK"
            result["rijen"]  = count

            # Controleer versheid van sales-data
            if naam == "sales" and "ingested_at" in df.columns:
                laatste = df.agg(F.max("ingested_at")).collect()[0][0]
                result["detail"] = f"Laatste ingest: {laatste}"

    except Exception as e:
        result["detail"] = str(e)[:80]

    return result


def print_rapport(resultaten: list[dict]) -> None:
    print("\n" + "─" * 60)
    print("  PLATFORM HEALTH RAPPORT")
    print(f"  {date.today()}")
    print("─" * 60)

    huidige_laag = None
    fouten = 0

    for r in resultaten:
        if r["laag"] != huidige_laag:
            huidige_laag = r["laag"]
            print(f"\n  [{huidige_laag.upper()}]")

        rijen_str = f"{r['rijen']:>6,} rijen" if r["rijen"] else "       "
        detail    = f"  ← {r['detail']}" if r["detail"] else ""
        print(f"    {r['status']}  {r['tabel']:<25} {rijen_str}{detail}")

        if "FOUT" in r["status"]:
            fouten += 1

    print("\n" + "─" * 60)
    if fouten == 0:
        print("  ✅ Alle checks geslaagd — platform is gezond")
    else:
        print(f"  ❌ {fouten} check(s) mislukt — actie vereist")
    print("─" * 60 + "\n")


def run():
    spark = get_spark("PlatformMonitor")

    resultaten = [
        check_table(spark, laag, naam, pad)
        for laag, naam, pad in CHECKS
    ]

    print_rapport(resultaten)
    spark.stop()


if __name__ == "__main__":
    run()