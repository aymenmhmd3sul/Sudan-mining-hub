-- 1. جدول التصنيفات
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- 2. جدول الأصول الرئيسي
CREATE TABLE mining_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    seller_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'DRAFT',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

-- 3. الفهارس
CREATE INDEX idx_mining_assets_seller_id ON mining_assets(seller_id);
CREATE INDEX idx_mining_assets_category_id ON mining_assets(category_id);
CREATE INDEX idx_mining_assets_status ON mining_assets(status);
