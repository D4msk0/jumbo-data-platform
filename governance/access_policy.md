# Access Policy — Jumbo Data Platform

> Dit document beschrijft wie toegang heeft tot welke data binnen het platform.
> In productie wordt dit afgedwongen via **Databricks Unity Catalog** met role-based access control (RBAC).

---

## Rollen

| Rol | Omschrijving |
|-----|-------------|
| `data_engineer` | Toegang tot alle lagen (Bronze, Silver, Gold). Beheert pipelines. |
| `data_analyst` | Toegang tot Silver en Gold. Geen schrijfrechten. |
| `category_manager` | Toegang tot productdata en top_producten in Gold. |
| `logistics` | Toegang tot winkelinformatie (stores). |
| `management` | Leestoegang tot alle Gold-tabellen. |

---

## Toegangsmatrix

| Tabel | data_engineer | data_analyst | category_manager | logistics | management |
|-------|:---:|:---:|:---:|:---:|:---:|
| `bronze/*` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `silver/sales` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `silver/stores` | ✅ | ✅ | ❌ | ✅ | ❌ |
| `silver/products` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `gold/omzet_per_winkel` | ✅ | ✅ | ❌ | ❌ | ✅ |
| `gold/omzet_per_categorie` | ✅ | ✅ | ❌ | ❌ | ✅ |
| `gold/omzet_per_maand` | ✅ | ✅ | ❌ | ❌ | ✅ |
| `gold/top_producten` | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## Principes

- **Least privilege** — gebruikers krijgen alleen toegang tot wat ze nodig hebben.
- **Laag-isolatie** — Bronze is uitsluitend toegankelijk voor engineers; ruwe data blijft afgeschermd.
- **Audit logging** — alle datatoegang wordt gelogd (in productie via Unity Catalog audit logs).
- **Geen persoonsdata** — dit platform verwerkt geen klantpersoonsgegevens (AVG-by-design).