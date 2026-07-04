-- ====================================================================
-- 1. جدول تاريخ تحولات الحالات (asset_status_history) - حارس الـ State Machine
-- ====================================================================
CREATE TABLE asset_status_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    from_state TEXT,                         -- يمكن أن يكون NULL عند أول إنشاء للأصل
    to_state TEXT NOT NULL,                  -- الحالة المنتقل إليها
    actor TEXT NOT NULL,                     -- المنفذ (Seller, Buyer, Admin, System)
    actor_id TEXT NOT NULL,                  -- معرف المستخدم المنفذ (أو SYSTEM)
    reason TEXT,                             -- اختياري (مثل سبب الرفض أو الإيقاف)
    changed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 2. سجل الأحداث الشامل (asset_events) - نواة الـ Mining Intelligence
-- ====================================================================
CREATE TABLE asset_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    event_type TEXT NOT NULL,                -- نوع الحدث من الـ Catalog (مثل: IMAGE_UPLOADED)
    payload TEXT,                            -- بيانات الحدث بصيغة JSON (للمرونة الكاملة مستقبلاً)
    actor TEXT NOT NULL,                     -- المنفذ الفعلي للحدث
    actor_id TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 3. سجل تتبع الأسعار (price_history)
-- ====================================================================
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    price REAL NOT NULL,                     -- السعر الجديد
    currency TEXT NOT NULL DEFAULT 'SDG',    -- العملة (SDG, USD...)
    changed_by TEXT NOT NULL,                -- من قام بتعديل السعر
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 4. الفهارس (Indexes)
-- ====================================================================
CREATE INDEX idx_asset_status_history_asset_id ON asset_status_history(asset_id);
CREATE INDEX idx_asset_events_asset_id ON asset_events(asset_id);
CREATE INDEX idx_asset_events_event_type ON asset_events(event_type);
CREATE INDEX idx_price_history_asset_id ON price_history(asset_id);
