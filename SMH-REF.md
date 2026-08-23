# SMH-REF — Sudan Mining Hub Living Project Reference

Updated: 2026-08-23

## CURRENT STATE
- Repository: aymenmhmd3sul/Sudan-mining-hub
- Current branch: preview-interactive-gateway-i18n-20260817
- Current commit at reference creation: a4638fd65d079e09e06cc081828cae8ec9b927eb
- Production: https://sudan-mining-hub-3.onrender.com
- Stack: FastAPI + Uvicorn + Jinja2 + SQLAlchemy/SQLModel + PostgreSQL + centralized i18n.

## CURRENT MISSION
Restore and preserve the canonical interactive Gateway while completing i18n correctly.

DO NOT blindly rollback Gateway to 3d81c60.
DO NOT replace the current Gateway with an old version.
Treat 3d81c60 as historical interactive evidence only.

## GATEWAY
Current files:
- app/templates/gateway.html
- app/static/js/gateway_v2_stable.js

Historical interactive baseline:
- 3d81c60
- old gateway.js
- old gateway.html

Current JS contains:
- password visibility
- language menu
- login via POST /auth/login
- visitor navigation
- Arabic/English switching
- server language/direction handling
- modal history handling
- showDetail()
- openCategory()
- requireAuth()
- toggleLanguage()
- search filtering
- state filtering
- category filtering

Current HTML has extensive i18n conversion from:
t.key
to:
t("key")

It also contains gateway data-* attributes for language/auth messages.

## GATEWAY RULE
The Gateway must remain:
- interactive
- mobile-first
- searchable
- filterable by state/category
- browsable
- capable of showing item details
- capable of authentication protection
- capable of language switching

Interaction must never be sacrificed merely to make i18n work.

## I18N
Supported languages:
- ar
- en

Language source:
request.state.lang

Direction:
- ar = rtl
- en = ltr

Known previous failure:
the translation helper was registered incorrectly, causing t(...) to resolve to Arabic instead of the request language.

Rule:
1. preserve canonical Gateway
2. fix request-aware translation
3. remove/replace hard-coded UI text
4. verify Arabic
5. verify English
6. verify interaction in both languages

## ROLES
Canonical roles:
- admin
- merchant
- buyer
- agent
- visitor

Canonical workspaces:
- admin -> /admin
- merchant -> /merchant/workspace/dashboard
- buyer -> /buyer/dashboard
- agent -> /agent/dashboard
- visitor -> public Gateway

Routing must be role-based.
Never route based on email, demo account, hard-coded user, or legacy template.

## AUTH
Known production flow:
- POST /auth/register -> 201
- GET /login -> 200
- POST /auth/login -> 200
- redirect according to authenticated role

Known dependencies:
- require_buyer
- require_merchant
- require_agent

## BUYER
Previous missing template recovery:
- buyer/dashboard/index.html restored from 84064e699bc5fad1d0259a16b4bd44899c23628a
- layouts/buyer_layout.html restored

Restored does not automatically mean final canonical UI.

## MERCHANT
Merchant workspace is intended as a production command center covering concepts such as:
- deals
- escrow
- balance
- earnings
- products
- rooms
- withdrawals
- licenses
- trust/profile
- bottom navigation

All merchants must use the same canonical workspace structure with user-specific data.

## SUBSCRIPTIONS
Relevant:
- app/models/subscription.py
- app/services/plan_access_service.py

Important commit:
- c5b794b — fix: track subscription model required by marketplace

## RENDER
Service:
Sudan-mining-hub-3

Runtime:
Python 3.12.3

Start:
uvicorn app.main:app --host 0.0.0.0 --port $PORT

Never assume a GitHub branch push changes production.
Verify Render's configured branch and deployed SHA.

## BRANCHES
Important branches:
- main
- preview-interactive-gateway-i18n-20260817
- backup/preview-interactive-gateway-i18n-20260822
- fix/i18n-full-audit
- fix/restore-gateway-ui
- ui-v3-global-gateway
- stable-platform
- stable-recovery
- agent/production-mvp-local-gateway

## LEGACY POLICY
Historical/backup files are evidence, not production candidates by default.

Do not blindly delete:
- before_*
- *.bak
- *.backup*
- restore*
- historical Gateway files
- diagnostic artifacts

Classify first.

## SINGLE SOURCE OF TRUTH
For every production UI:
- one canonical router
- one canonical template
- one canonical layout
- one canonical static asset set
- one canonical access rule

Avoid mixing v1/v2/historical implementations.

## SAFETY PROTOCOL
Before modifying production-facing code:
1. git branch --show-current
2. git rev-parse HEAD
3. git status
4. inspect relevant router/template/static references
5. backup/snapshot when necessary
6. smallest safe change
7. compile/import test
8. route test
9. UI behavior test
10. commit
11. push intended branch
12. verify remote SHA
13. verify Render deployment

## CURRENT NEXT STEP
1. Verify current branch/commit/status.
2. Inspect canonical Gateway router/template/static references.
3. Compare current Gateway against 3d81c60 only as historical evidence.
4. Test interactive functions independently.
5. Test Arabic and English independently.
6. Fix only the actual defect.
7. Preserve the interactive Gateway.
8. Update this SMH-REF after the verified milestone.

## SESSION SHORTCUT
At the beginning of a future session:
Say:
SMH-REF

Then use this document as the project bootstrap reference instead of repeating broad discovery.

Historical reference:
SMH-CONTEXT.md
