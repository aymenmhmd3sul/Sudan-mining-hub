# Sudan Mining Hub - Architecture Layer Documentation

## 🔐 1. Authentication & Security (Stabilized)
* **Core Security:** `app/core/security.py` 
  * *Schemes:* `pbkdf2_sha256` (Primary) & `sha256_crypt` (Legacy Support).
  * *JWT Config:* HS256 with 32-byte production secure key.
* **Database Entry:** `app/core/db.py`
  * Single Source of Truth for SQLite database operations on `local.db`.

## 📂 2. Directory Mappings
* Routers are systematically isolated in `app/routers/`.
* Legacy routers and adapters are strictly moved to `./legacy/` to prevent Python runtime conflicts.
