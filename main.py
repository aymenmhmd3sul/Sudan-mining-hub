from fastapi import FastAPI
from sqlalchemy import text
import database

app = FastAPI()

@app.get("/api/v1/market/items")
def get_items():
    try:
        with database.engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM market_items"))
            rows = result.fetchall()

            return {
                "count": len(rows),
                "data": [dict(row._mapping) for row in rows]
            }

    except Exception as e:
        return {"error": str(e)}
