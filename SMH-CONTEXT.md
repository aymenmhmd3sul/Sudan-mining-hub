# SMH-CONTEXT
# Sudan Mining Hub — Project Reference
# Last updated: 2026-08-22

## 1. PROJECT IDENTITY

Project: Sudan Mining Hub
Repository: aymenmhmd3sul/Sudan-mining-hub
Production URL: https://sudan-mining-hub-3.onrender.com

Primary stack:
- FastAPI
- Uvicorn
- Jinja2
- SQLAlchemy / SQLModel
- PostgreSQL
- Neon
- JWT / cookie authentication
- Centralized i18n
- Mobile-first web workspaces

## 2. CURRENT PRODUCTION BRANCH

Current deployment branch:
preview-interactive-gateway-i18n-20260817

Latest known deployed commit:
ba07d653446a866e36a873b88f7c7551c109002f

Recent important commits:
- c5b794b — fix: track subscription model required by marketplace
- ba07d65 — fix: restore buyer dashboard templates

## 3. ROLES

Canonical application roles:
- admin
- merchant
- buyer
- agent
- visitor

Rule:
Every authenticated user must reach the workspace belonging to their actual role.

The workspace must NOT depend on:
- email address
- pre-existing demo account
- hard-coded user
- old template
- old backup router

## 4. WORKSPACES

Buyer:
 /buyer/dashboard

Merchant:
 /merchant/workspace/dashboard

Agent:
 /agent/dashboard

Admin:
 /admin

Visitor:
 public browsing / gateway only

## 5. CURRENT ARCHITECTURE

app/main.py currently registers:
- merchant_views
- buyer_views
- agent_views
- admin_views
- admin_users
- language
- web
- negotiation
- marketplace
- escrow

Authentication and authorization are handled through:
app/core/dependencies.py

Important dependency functions:
- require_buyer
- require_merchant
- require_agent

## 6. GATEWAY

The root gateway is a critical production interface.

Required behavior:
- interactive
- mobile-first
- search/browse experience
- opportunities/services discovery
- authentication actions
- language switching
- must not be replaced by an old static dashboard
- must not regress to a translation-corrupted historical version

Canonical gateway files must be explicitly verified before replacement.

## 7. INTERNATIONALIZATION

Languages:
- ar
- en

Language state is carried through request.state.lang.
Direction:
- ar -> rtl
- en -> ltr

Central translation system exists.

Important rule:
Do not restore historical templates merely because they contain translated text.

Before changing i18n:
1. identify canonical UI
2. preserve interaction logic
3. then apply translation
4. verify Arabic and English separately

## 8. DASHBOARD RULE

The dashboard is a workspace, not a static welcome page.

A newly registered user must receive the same structural workspace as another user with the same role.

Example:
buyer A and buyer B -> same buyer workspace structure.

Their personal data may differ:
- name
- requests
- offers
- deals
- financial records
- notifications

But the UI architecture must remain consistent.

## 9. CURRENT BUYER ISSUE / RECOVERY

A previous deployment failed because:
buyer/dashboard/index.html
was missing.

It was restored from commit:
84064e699bc5fad1d0259a16b4bd44899c23628a

Also restored:
app/templates/layouts/buyer_layout.html

This restoration solved TemplateNotFound, but the restored template was an older UI and is NOT automatically considered the canonical buyer workspace.

Therefore:
RESTORED != CANONICAL

The correct next step is to identify the intended current buyer workspace and restore its full UI without reintroducing old centralized-i18n corruption.

## 10. MERCHANT REFERENCE

Merchant dashboard is known to contain the richer production-style workspace.

Expected concepts:
- executive/merchant command center
- active deals
- escrow
- balance
- earnings
- products
- rooms
- withdrawals
- licenses
- profile/trust
- bottom navigation

The Hagoo account demonstrated that the merchant workspace can load correctly.

Important:
The existence of a working Hagoo dashboard does NOT justify user-specific routing.

All merchants must receive the same workspace structure with their own data.

## 11. AGENT

Agent workspace must follow the same principle:
- role-based access
- canonical template
- user-specific data
- no hard-coded account routing
- no historical backup template as production UI

## 12. AUTHENTICATION

Known production flow:
POST /auth/register -> 201
GET /login -> 200
POST /auth/login -> 200
then role-specific dashboard

Previous production log showed:
GET /buyer/dashboard -> 500
because buyer/dashboard/index.html was missing.

After restoring the template:
GET /buyer/dashboard -> 200

Authentication errors from crawlers without tokens are not evidence of a broken user session.

## 13. SUBSCRIPTION

Subscription model is now tracked in Git.

File:
app/models/subscription.py

Required by:
app/services/plan_access_service.py

Commit:
c5b794b

Both imports were verified locally:
Subscription import
PlanAccessService import

Full app import also passed.

## 14. RENDER

Service:
Sudan-mining-hub-3

Production:
https://sudan-mining-hub-3.onrender.com

Runtime:
Python 3.12.3

Start command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT

Current deployment branch:
preview-interactive-gateway-i18n-20260817

Important:
Render deployment follows the Git branch configured for the service.
Do not assume pushing another branch changes production.

## 15. NEON

Production database:
Neon PostgreSQL

Connection details/secrets:
NOT STORED IN THIS FILE.

Never place:
- DATABASE_URL
- passwords
- JWT secret
- API tokens
- Render secrets
- Neon credentials

inside SMH-CONTEXT.md.

Only document:
- variable names
- database purpose
- migration status
- schema notes
- production/non-production distinction

## 16. GITHUB BRANCH DISCIPLINE

Important branches previously used include:
- main
- merchant-marketplace-offers
- preview-interactive-gateway-i18n-20260817
- stable/recovery branches
- UI/recovery branches

Rule:
Before modifying production-facing code:
1. identify current branch
2. identify current commit
3. inspect git status
4. create backup/snapshot if necessary
5. verify locally
6. commit
7. push intended branch
8. verify remote SHA
9. verify Render deployment

## 17. LEGACY FILE POLICY

There are many files named:
before_*
*.bak
*.backup*
corrupted-*
restore*
old diagnostic files
historical gateway files

These are historical evidence/backups.

They are NOT production candidates by default.

Never delete blindly.

Before cleanup:
- classify
- verify whether tracked
- verify whether referenced
- preserve useful recovery snapshots
- then remove only confirmed obsolete artifacts

## 18. SINGLE SOURCE OF TRUTH

For every production UI:
1. one canonical router
2. one canonical template
3. one canonical layout
4. one canonical static asset set
5. one role/access rule

Do not maintain multiple competing production versions.

## 19. DEVELOPMENT PROTOCOL

Before every significant change:

CHECK:
- current branch
- current commit
- git status
- relevant router
- relevant dependency
- relevant template
- relevant layout
- authentication flow

THEN:
- backup
- modify
- compile/import test
- route test
- UI test
- commit
- push
- verify deployment

## 20. CURRENT PRIORITY

Priority order:

1. Preserve working production authentication.
2. Unify Buyer / Merchant / Agent workspace architecture.
3. Restore intended interactive UI.
4. Ensure user-specific data is separated from UI structure.
5. Fix i18n without destroying interaction.
6. Remove confirmed obsolete artifacts only after verification.
7. Keep GitHub and Render branches synchronized intentionally.

## 21. SESSION RULE

When the phrase:

SMH-CONTEXT

is mentioned, treat this file as the project reference.

But:
REAL CODE > SMH-CONTEXT
GITHUB STATE > SMH-CONTEXT
RENDER STATE > SMH-CONTEXT
NEON STATE > SMH-CONTEXT

If they conflict, investigate and update this document.

