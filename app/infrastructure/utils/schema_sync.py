from sqlalchemy import inspect
from app.infrastructure.database import engine, Base

async def sync_schema():
    async with engine.begin() as conn:
        def do_sync(sync_conn):
            inspector = inspect(sync_conn)
            existing_tables = inspector.get_table_names()
            
            for table in Base.metadata.tables.values():
                if table.name not in existing_tables:
                    print(f"🛠️ [Sync]: Creating table '{table.name}'...")
                    table.create(sync_conn)
                else:
                    existing_columns = [c['name'] for c in inspector.get_columns(table.name)]
                    for column in table.columns:
                        if column.name not in existing_columns:
                            print(f"⚡ [Sync]: Adding column '{column.name}' to '{table.name}'...")
                            col_type = column.type.compile(sync_conn.dialect)
                            sync_conn.execute(f"ALTER TABLE {table.name} ADD COLUMN {column.name} {col_type}")

        await conn.run_sync(do_sync)
        print("✅ [Sync]: Schema synced.")
