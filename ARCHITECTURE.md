# Sudan Mining Hub - Architecture v1

## Core System
- FastAPI app in app/main.py
- Active routers system (DO NOT REMOVE)
- Authentication handled via routers/auth.py

## Modules
- routers/ = active API layer
- app/services/ = business logic (future migration)
- app/db/ = database layer (future abstraction)

## Rules
- No direct database imports outside db layer
- No mixing old and new architecture without migration plan
- Routers remain active until full refactor approval

