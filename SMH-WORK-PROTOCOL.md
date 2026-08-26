# SMH-WORK-PROTOCOL
## Sudan Mining Hub — Permanent Development & Recovery Protocol

> هذا الملف هو بروتوكول العمل الدائم للمشروع.
> يجب الرجوع إليه في بداية كل جلسة عمل جديدة قبل إجراء فحوصات أو تغييرات كبيرة.

---

## 1. تعريف المراجع

### SMH-REF
SMH-REF = Sudan Mining Hub Restructure.

SMH-REF هو:
- مرجع معلوماتي للمشروع.
- يحتوي على المعلومات الرئيسية، التاريخ، الأخطاء السابقة، القرارات، والبنية المعروفة.
- يستخدم لاستعادة سياق المشروع ومنع تكرار الفحوصات.
- ليس فرع تشغيل.
- ليس نسخة نبني عليها مباشرة.
- لا يتم تحويله إلى production لمجرد أنه مرجع.

### Production
بيئة الإنتاج الحالية هي Render + Neon.

Render:
- Service: Sudan-mining-hub-3
- Public URL: https://sudan-mining-hub-3.onrender.com

Repository:
- aymenmhmd3sul/Sudan-mining-hub

---

## 2. الهدف النهائي

بناء نسخة Production بسيطة ومستقرة وقابلة للتوسع من Sudan Mining Hub، مع:

1. واجهة بصرية احترافية محفوظة الهوية العامة للمشروع.
2. Backend واضح ومستقر.
3. قاعدة بيانات Neon كمصدر تخزين Production.
4. وحدات مستقلة قابلة للإضافة والربط.
5. Single Source of Truth.
6. نظام أدوار وصلاحيات واضح.
7. إمكانية تفعيل أو تعطيل الوحدات دون إعادة بناء المشروع.
8. عدم الاعتماد على حلول مؤقتة أو ترقيعات متراكمة.
9. إمكانية إضافة أقسام جديدة دون إعادة بناء النظام من الصفر.

---

## 3. قاعدة العمل الأساسية

لا نبدأ بالبرمجة قبل فهم المشكلة.

التسلسل الإلزامي:

REFERENCE
→ ISOLATE
→ HYPOTHESIS
→ MINIMAL CHANGE
→ TEST
→ BROWSER VISUAL CHECK
→ PRODUCTION CHECK
→ COMMIT
→ DOCUMENT

---

## 4. ممنوع تكرار الفحوصات المحسومة

إذا كان SMH-REF أو سجل الجلسات السابقة يحتوي على نتيجة فحص مؤكدة:

- لا نعيد الفحص تلقائياً.
- نستخدم النتيجة السابقة.
- نعيد الفحص فقط إذا:
  - تغير الكود المرتبط بها.
  - تغيرت البيئة.
  - ظهرت نتيجة متناقضة.
  - أصبح الفحص ضرورياً لإثبات فرضية جديدة.

الهدف:
تقليل الوقت الضائع في إعادة نفس التشخيص.

---

## 5. قاعدة المتصفح

لا يعتبر أي تغيير في الواجهة ناجحاً بمجرد:

- نجاح syntax.
- نجاح grep.
- نجاح curl.
- نجاح HTTP 200.
- نجاح JavaScript بدون أخطاء.

النجاح النهائي للواجهة يحتاج:

1. تشغيل النسخة.
2. فتحها في المتصفح.
3. رؤية النتيجة بصرياً.
4. تجربة التفاعل الحقيقي.
5. التأكد أن التصميم والسلوك هما المطلوبان.

لا يتم تثبيت أو اعتماد تغيير بصري قبل هذه المرحلة.

---

## 6. قاعدة Production

Render هو المرجع التشغيلي للإنتاج.

Neon هو مخزن بيانات Production.

لا نخلط بين:
- local development
- GitHub reference
- preview branches
- Render production

أي تغيير Production يجب أن يكون مقصوداً وقابلاً للتراجع.

---

## 7. قاعدة Git

قبل أي تغيير كبير:

1. معرفة branch الحالي.
2. معرفة commit الحالي.
3. حفظ نقطة رجوع.
4. تنفيذ تغيير محدود.
5. اختبار.
6. commit واضح.

لا تستخدم:
- force push
- reset خطير
- حذف branch
- استبدال ملفات رئيسية
إلا بعد التأكد من إمكانية rollback.

---

## 8. الوحدات المستقلة

كل Module يجب أن يكون قابلاً لـ:

- التطوير منفرداً.
- الاختبار منفرداً.
- الربط بالمشروع.
- التعطيل.
- التفعيل.
- التوسع.

إضافة Module جديد لا يجب أن تتطلب إعادة بناء المشروع كله.

يجب فصل:

UI
API
Service
Data Model
Authorization
Configuration

قدر الإمكان.

---

## 9. Single Source of Truth

لا يجوز أن تكون نفس المعلومة موزعة في أماكن متناقضة.

خصوصاً:

- Role
- User status
- Permissions
- Authentication state
- Language
- Feature state
- Module state

يجب تحديد مصدر الحقيقة لكل واحدة.

لا نعالج التعارض بإضافة قيمة ثانية في مكان آخر.

---

## 10. الأدوار

الأدوار الأساسية الحالية:

- Visitor
- Buyer
- Merchant
- Agent
- Admin / Supervisor حسب نظام الصلاحيات المعتمد.

يجب أن يكون تحديد الدور موحداً.

لا يجوز أن:

- يسجل المستخدم كـ Agent
- ثم يتم إنشاء الحساب كـ Merchant
- أو يتم تحويله إلى Merchant بسبب default غير مقصود
- أو يحدد الدور من الواجهة فقط دون مصدر موثوق في قاعدة البيانات.

---

## 11. مشكلة Agent / Merchant

المشكلة المعروفة:

اختبار تسجيل Agent كان ينجح،
لكن بعد التسجيل كان المستخدم يدخل باعتباره Merchant.

يجب تشخيص السلسلة كاملة:

Registration
→ Submitted Role
→ Database Role
→ User Status
→ Login
→ Session / Token
→ Role Resolver
→ Authorization
→ Redirect
→ Dashboard

لا نعالج redirect فقط إذا كان أصل المشكلة في registration أو database.

يجب تحديد مكان فقدان الدور الحقيقي.

---

## 12. Authentication

المصادقة يجب أن تكون موحدة.

يجب ألا توجد عدة مصادر متضاربة لتحديد:

- من هو المستخدم.
- ما دوره.
- هل هو مصادق.
- هل حسابه pending/rejected/approved.
- إلى أين يتم توجيهه.

أي إصلاح في Authentication يجب اختبار:

- Buyer
- Merchant
- Agent
- Admin

بشكل منفصل.

---

## 13. Legacy Code

لا يتم إحياء الكود القديم لمجرد أنه موجود.

خصوصاً:

- legacy negotiation routers
- old authentication routes
- duplicate frontend routers
- obsolete templates

يجب تحديد:

ACTIVE
أو
LEGACY
أو
DISABLED

قبل الاعتماد عليه.

---

## 14. Gateway

Gateway هو واجهة رئيسية تفاعلية.

الوظائف الأساسية المستهدفة:

- البحث.
- الفلاتر.
- الحالات.
- الفئات.
- عرض العناصر.
- التفاصيل.
- Login.
- Register.
- Authentication gates.
- Language switching.
- Navigation.

يجب الحفاظ على السلوك التفاعلي وعدم اختزاله إلى صفحة ثابتة.

---

## 15. i18n

الترجمة يجب أن تستخدم مصدر ترجمة موحد.

لا نعتمد على خلط:

- hard-coded Arabic
- hard-coded English
- translation keys
- JavaScript strings

بدون سبب.

أي إصلاح للغة يجب التأكد منه على الأقل في:

Arabic
English

وفي Gateway والمناطق الأساسية.

---

## 16. قاعدة "لا ترقيع"

إذا ظهرت مشكلة:

لا نضيف workaround مباشرة.

نسأل:

1. أين المصدر الحقيقي؟
2. لماذا حدث؟
3. هل يوجد duplicate؟
4. هل يوجد route آخر؟
5. هل يوجد default role؟
6. هل يوجد middleware يغير القيمة؟
7. هل توجد session قديمة؟
8. هل يوجد template أو JS يتجاوز المصدر الصحيح؟

ثم نعالج المصدر.

---

## 17. قاعدة أقل تغيير ممكن

عند معرفة السبب:

نفذ أصغر تغيير صحيح يعالج السبب.

لا نعيد كتابة المشروع أو الملف كاملاً دون ضرورة.

الهدف:
تقليل regression.

---

## 18. اختبار قبل وبعد

كل إصلاح مهم يحتاج:

BEFORE
- تحديد السلوك الخاطئ.

AFTER
- إثبات السلوك الصحيح.

ثم:

BROWSER
- اختبار بصري وتفاعلي.

PRODUCTION
- اختبار على Render إذا كان التغيير Production-related.

---

## 19. لا نخلط النسخ

يجب عدم خلط:

- v1
- v2
- stable
- preview
- legacy
- recovery

إلا بعد معرفة الفروق بينها.

عند اختيار نسخة مرجعية:
يجب تحديدها بوضوح.

---

## 20. قاعدة الجلسات الجديدة

في بداية كل جلسة:

1. اقرأ SMH-WORK-PROTOCOL.md.
2. استخدم SMH-REF لاستعادة المعلومات.
3. حدد آخر حالة معروفة.
4. حدد آخر مشكلة غير محلولة.
5. لا تعيد الفحوصات المحسومة.
6. ابدأ من آخر نقطة مؤكدة.

---

## 21. سجل الحالة

كل جلسة مهمة يجب أن تنتهي بسجل:

DATE
CURRENT BRANCH
CURRENT COMMIT
WHAT WAS VERIFIED
WHAT WAS FIXED
WHAT REMAINS
LAST BROWSER RESULT
LAST PRODUCTION RESULT
NEXT STEP

---

## 22. قاعدة عدم الادعاء

لا نقول:

"تم الحل"

إلا إذا كان هناك دليل.

الأدلة المقبولة حسب نوع المشكلة:

- Code inspection
- Automated test
- API test
- Database verification
- Browser verification
- Production verification

ولا نخلط بينها.

---

## 23. قاعدة عدم تثبيت التغييرات

لا يتم اعتبار التغيير نهائياً قبل عرضه بصرياً على المتصفح عندما يكون التغيير متعلقاً بالواجهة.

يمكن إنشاء commit تجريبي،
لكن لا نعتبره النسخة النهائية المتفق عليها قبل التحقق.

---

## 24. قاعدة العمل للمطورين

المطوران الفعليان للمشروع:

User + AI

لذلك يجب تقليل:

- التجارب العشوائية.
- تكرار الفحوصات.
- التعديلات الواسعة.
- التراجع غير الموثق.
- الاعتماد على ذاكرة الجلسة.

والاعتماد بدلاً من ذلك على:

Documentation
Git
SMH-REF
Tests
Browser verification
Production verification

---

## 25. معيار النجاح

المشروع ناجح عندما:

- يعمل Production.
- المصادقة صحيحة.
- الأدوار صحيحة.
- Merchant يدخل Merchant.
- Agent يدخل Agent.
- Buyer يدخل Buyer.
- Admin يدخل Admin.
- Visitor يستطيع التصفح المسموح.
- الوحدات مستقلة.
- إضافة Module جديدة لا تكسر النظام.
- Gateway تفاعلي.
- اللغة تعمل.
- قاعدة البيانات مستقرة.
- لا توجد مصادر متناقضة للحقيقة.
- كل إصلاح رئيسي يمكن تفسيره وإرجاعه.

---

## 26. قاعدة الأولوية

عند وجود عدة مشاكل:

1. Production stability
2. Authentication
3. Roles / Authorization
4. Database integrity
5. Core business flows
6. Gateway functionality
7. UI polish
8. Secondary features

لا نضحي بالاستقرار لإضافة ميزة ثانوية.

---

## 27. قاعدة القرار

إذا كان لدينا خياران:

A) حل سريع هش
B) حل بسيط صحيح وقابل للتوسع

نختار B حتى لو احتاج وقتاً إضافياً معقولاً.

لكن لا نعيد بناء أجزاء مستقرة بدون سبب.

---

## 28. قاعدة الخروج من المشكلة

عندما نفشل في مسار تشخيصي مرتين:

نتوقف.

لا نكرر نفس الفحص بصيغة مختلفة.

نعود إلى:

- المصدر.
- SMH-REF.
- Git history.
- route map.
- data flow.
- actual runtime behavior.

ثم نغير الفرضية.

---


## 15. PRODUCTION DATABASE & ENVIRONMENT IDENTITY

هذه هي الهوية التشغيلية المعتمدة لبيئة Production، وتم تثبيتها بعد التحقق من إعدادات Render وNeon.

### Render Web Service

- Service: `Sudan-mining-hub-3`
- Service ID: `srv-d8m7vocvikkc73cgc0a0`
- Type: Web Service (Python 3)
- Plan: Starter
- Compute: 0.5 CPU / 512 MB RAM
- Region: Frankfurt (EU Central)
- Repository: `aymenmhmd3sul/Sudan-mining-hub`
- Production URL: `https://sudan-mining-hub-3.onrender.com`
- Configured deployment branch: `preview-interactive-gateway-i18n-20260817`
- Auto-Deploy: OFF

### Render Build / Start

Build command:

`pip install -r requirements.txt`

Start command:

`uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Production Database

Production database is:

**Neon PostgreSQL**

Render Web Service is the application layer and passes the production `DATABASE_URL` to the application.

The production database is NOT Render's former PostgreSQL service.

The former Render database service:

`Sudan-mining-hub-db`

is not the Production Source of Truth.

### Production Source of Truth

**Neon PostgreSQL is the single source of truth for Production data.**

Production users, authentication data, marketplace data, and other persistent application data must be read/written through the Production Neon database when the application is running in Production.

The Neon connection string and credentials MUST NOT be stored in this protocol, GitHub source files, or other documentation.

Only the variable name and architectural role may be documented.

### Local Databases

The following local databases are NOT Production:

- `local.db` — local development database.
- `sudan_mining.db` — legacy local database.

A local runtime result such as:

`DATABASE_URL = sqlite:///local.db`

proves only the database configuration of the local Termux environment.

It MUST NOT be interpreted as the Production database configuration.

### Environment Separation Rule

The project has four distinct layers:

`Termux Local`
→ `GitHub`
→ `Render Web Service`
→ `Neon Production Database`

These layers MUST NOT be conflated.

In particular:

- Local `.env` does not define Render Production.
- GitHub branch state does not by itself prove the deployed Render state.
- Render Web Service is not the Production database.
- Neon is the Production database.
- A local SQLite database must never be used as evidence about Production data.
- A disabled/removed legacy Render database must never be silently replaced by a local SQLite database.

### Production Verification Rule

Before any database, authentication, migration, or user-account investigation, identify explicitly:

1. Which environment is being tested.
2. Which Git branch/commit is being tested.
3. Which database that environment actually resolves to.
4. Whether the result represents Local, GitHub, Render, or Neon state.

If these identities are unclear, STOP before making changes.

### No Third Database Rule

Do not introduce a third database as a temporary workaround.

Do not create a new SQLite/PostgreSQL database merely to make a test pass.

If Production is unavailable, diagnose the Production path instead of silently falling back to another database.

### Authentication Database Rule

Authentication tests such as:

- `good@test.com`
- Buyer
- Merchant
- Agent
- Admin

must be executed against the intended environment and database.

A successful local authentication test does not prove that the same account exists in Neon Production.

### Render Deployment Rule

Never assume that pushing a GitHub branch changes Production.

Always verify:

- Render configured branch.
- Render deployed commit/SHA.
- Render runtime environment.
- Runtime `DATABASE_URL` destination, without exposing credentials.

### Critical Safety Rule

Before changing `app/database.py`, `app/infrastructure/database.py`, authentication, migrations, models, or database dependencies:

**IDENTIFY ENVIRONMENT → IDENTIFY DATABASE → VERIFY SOURCE OF TRUTH → THEN CHANGE.**

This rule exists to prevent testing one database while believing that another database is being tested.


## 29. البروتوكول النهائي

القاعدة الذهبية:

DO NOT GUESS.
DO NOT PATCH BLINDLY.
DO NOT REPEAT VERIFIED CHECKS.
DO NOT DECLARE SUCCESS WITHOUT EVIDENCE.
DO NOT DEPLOY UNVERIFIED UI.
DO NOT MIX REFERENCE WITH PRODUCTION.

Always:

READ
→ UNDERSTAND
→ ISOLATE
→ FIX
→ TEST
→ SEE
→ VERIFY
→ COMMIT
→ DOCUMENT

---

# END OF SMH-WORK-PROTOCOL
