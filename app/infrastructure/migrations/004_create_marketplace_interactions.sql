-- ====================================================================
-- 1. جدول المفاوضات والعروض المالية (asset_negotiations)
-- ====================================================================
CREATE TABLE asset_negotiations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,               -- معرف المشتري
    current_offer_price REAL NOT NULL,       -- قيمة العرض الحالي المالي
    status TEXT NOT NULL DEFAULT 'OPEN',     -- حالة التفاوض (OPEN, ACCEPTED, REJECTED, CLOSED)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 2. جدول البلاغات والرقابة (asset_reports)
-- ====================================================================
CREATE TABLE asset_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    reporter_id INTEGER NOT NULL,            -- من قام بالتبليغ
    reason TEXT NOT NULL,                    -- سبب التبليغ
    status TEXT NOT NULL DEFAULT 'PENDING',  -- حالة البلاغ (PENDING, RESOLVED, IGNORED)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 3. جدول المفضلة (asset_favorites)
-- ====================================================================
CREATE TABLE asset_favorites (
    user_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, asset_id),
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 4. جدول المشاهدات والزيارات (asset_views)
-- ====================================================================
CREATE TABLE asset_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    viewer_id INTEGER,                       -- يمكن أن يكون NULL إذا كان الزائر غير مسجل (Guest)
    ip_address TEXT,                         -- لمنع تكرار العدادات العشوائية
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 5. الفهارس (Indexes)
-- ====================================================================
CREATE INDEX idx_asset_negotiations_asset_id ON asset_negotiations(asset_id);
CREATE INDEX idx_asset_reports_asset_id ON asset_reports(asset_id);
CREATE INDEX idx_asset_views_asset_id ON asset_views(asset_id);
