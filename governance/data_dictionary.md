# Data Dictionary — Jumbo Data Platform

> Beschrijving van alle tabellen en kolommen in het platform.

---

## silver.stores

Winkelinformatie na cleaning.

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `store_id` | string | Unieke identifier (bijv. ST001) |
| `store_name` | string | Volledige winkelnaam |
| `city` | string | Vestigingsstad |
| `format` | string | Winkelformaat (Superstore / Stadswinkel / Buurtwinkel) |
| `opening_year` | integer | Jaar van opening |
| `floor_area_m2` | integer | Verkoopvloeroppervlak in m² |
| `ingested_at` | timestamp | Tijdstip van inladen in het platform |

---

## silver.products

Productinformatie na cleaning.

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `product_id` | string | Unieke identifier (bijv. PR0001) |
| `product_name` | string | Productnaam |
| `category` | string | Productcategorie |
| `price_eur` | double | Verkoopprijs in euro's |
| `is_jumbo_huismerk` | boolean | True als het een Jumbo huismerkartikel is |
| `weight_gram` | integer | Gewicht in gram |
| `ingested_at` | timestamp | Tijdstip van inladen in het platform |

---

## silver.sales

Transactiedata na cleaning.

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `transaction_id` | string | Unieke transactie-identifier (bijv. TX000001) |
| `order_date` | date | Datum van de transactie |
| `store_id` | string | Verwijzing naar stores.store_id |
| `product_id` | string | Verwijzing naar products.product_id |
| `quantity` | integer | Aantal verkochte eenheden |
| `unit_price_eur` | double | Prijs per eenheid in euro's |
| `discount_pct` | double | Kortingspercentage (0.0 – 1.0) |
| `revenue_eur` | double | Gerealiseerde omzet (na korting) |
| `payment_method` | string | Betaalmethode (pin / cash / app) |
| `year` | integer | Jaar afgeleid van order_date |
| `month` | integer | Maand afgeleid van order_date |
| `ingested_at` | timestamp | Tijdstip van inladen in het platform |

---

## gold.omzet_per_winkel

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `store_id` | string | Winkelidentifier |
| `store_name` | string | Winkelnaam |
| `city` | string | Vestigingsstad |
| `format` | string | Winkelformaat |
| `totaal_omzet_eur` | double | Totale omzet in euro's |
| `aantal_transacties` | long | Aantal transacties |
| `gemiddeld_bedrag_eur` | double | Gemiddeld transactiebedrag |

---

## gold.omzet_per_categorie

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `category` | string | Productcategorie |
| `totaal_omzet_eur` | double | Totale omzet in euro's |
| `totaal_aantal_verkocht` | long | Totaal aantal verkochte eenheden |
| `aantal_producten` | long | Aantal unieke producten in de categorie |

---

## gold.omzet_per_maand

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `year` | integer | Jaar |
| `month` | integer | Maand (1–12) |
| `totaal_omzet_eur` | double | Totale omzet in euro's |
| `aantal_transacties` | long | Aantal transacties |

---

## gold.top_producten

| Kolom | Type | Omschrijving |
|-------|------|-------------|
| `product_id` | string | Productidentifier |
| `product_name` | string | Productnaam |
| `category` | string | Productcategorie |
| `price_eur` | double | Verkoopprijs |
| `totaal_omzet_eur` | double | Totale omzet in euro's |
| `totaal_aantal_verkocht` | long | Totaal aantal verkochte eenheden |