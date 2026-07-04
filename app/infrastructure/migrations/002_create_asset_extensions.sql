-- ====================================================================
-- 1. جدول المواقع الجغرافية للأصول (asset_locations)
-- ====================================================================
CREATE TABLE asset_locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    state TEXT NOT NULL,                     -- الولاية (مثال: نهر النيل، البحر الأحمر)
    region TEXT NOT NULL,                    -- المنطقة / المحلية (مثال: أبوحمد، المرابيع)
    latitude REAL,                           -- الإحداثيات الجغرافية (اختياري للخرائط لاحقاً)
    longitude REAL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 2. جدول المواصفات الديناميكية (asset_specs) - نمط Key-Value
-- ====================================================================
CREATE TABLE asset_specs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    spec_key TEXT NOT NULL,                  -- مفتاح المواصفة (مثال: القوة الحصانية، درجة النقاء)
    spec_value TEXT NOT NULL,                -- قيمة المواصفة (مثال: 500 HP، 92%)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE,
    UNIQUE(asset_id, spec_key)               -- منع تكرار نفس المفتاح لنفس الأصل
);

-- ====================================================================
-- 3. جدول صور الأصول (asset_images)
-- ====================================================================
CREATE TABLE asset_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,                 -- رابط الصورة على السيرفر أو التخزين السحابي
    is_main INTEGER DEFAULT 0,               -- هل هي الصورة الرئيسية للمعرض؟ (1 = نعم، 0 = لا)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 4. جدول المستندات والشهادات القانونية (asset_documents)
-- ====================================================================
CREATE TABLE asset_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    document_name TEXT NOT NULL,             -- اسم المستند (مثال: رخصة التنقيب، شهادة السلامة)
    document_url TEXT NOT NULL,              -- رابط الملف (PDF غالباً)
    is_verified INTEGER DEFAULT 0,           -- التحقق من المستند (0=معلق، 1=معتمد، 2=مرفوض)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES mining_assets(id) ON DELETE CASCADE
);

-- ====================================================================
-- 5. الفهارس (Indexes) لتسريع عمليات الربط والبحث
-- ====================================================================
CREATE INDEX idx_asset_locations_asset_id ON asset_locations(asset_id);
CREATE INDEX idx_asset_specs_asset_id ON asset_specs(asset_id);
CREATE INDEX idx_asset_images_asset_id ON asset_images(asset_id);
CREATE INDEX idx_asset_documents_asset_id ON asset_documents(asset_id);
