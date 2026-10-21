import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "fitradar.db")
BGN_TO_EUR = 1 / 1.95583

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        base_url TEXT NOT NULL,
        free_shipping_threshold REAL DEFAULT 70.0,
        standard_shipping_bgn REAL DEFAULT 5.99,
        free_shipping_threshold_eur REAL DEFAULT 35.79,
        standard_shipping_eur REAL DEFAULT 3.06,
        badge_color TEXT DEFAULT '#4F46E5'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_code TEXT NOT NULL,
        external_id TEXT,
        raw_title TEXT NOT NULL,
        clean_title TEXT NOT NULL,
        brand TEXT NOT NULL,
        category TEXT NOT NULL,
        form TEXT DEFAULT 'powder',
        flavor TEXT,
        weight_g REAL,
        servings INTEGER,
        protein_pct REAL,
        price_bgn REAL NOT NULL,
        old_price_bgn REAL,
        price_eur REAL NOT NULL,
        old_price_eur REAL,
        discount_pct INTEGER DEFAULT 0,
        price_per_100g REAL,
        price_per_100g_eur REAL,
        price_per_100g_protein REAL,
        price_per_serving REAL,
        price_per_serving_eur REAL,
        in_stock BOOLEAN DEFAULT 1,
        product_url TEXT,
        image_url TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (store_code) REFERENCES stores (code)
    );
    """)

    cursor.executescript("""
    CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
    CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_code);
    CREATE INDEX IF NOT EXISTS idx_products_brand ON products(brand);
    CREATE INDEX IF NOT EXISTS idx_products_price_100g_eur ON products(price_per_100g_eur);
    """)

    conn.commit()
    conn.close()

def upsert_store(code: str, name: str, base_url: str, free_shipping_threshold: float, standard_shipping_bgn: float, badge_color: str):
    conn = get_connection()
    cursor = conn.cursor()
    free_shipping_eur = round(free_shipping_threshold * BGN_TO_EUR, 2)
    standard_shipping_eur = round(standard_shipping_bgn * BGN_TO_EUR, 2)

    cursor.execute("""
        INSERT INTO stores (
            code, name, base_url, free_shipping_threshold, standard_shipping_bgn,
            free_shipping_threshold_eur, standard_shipping_eur, badge_color
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(code) DO UPDATE SET
            name=excluded.name,
            base_url=excluded.base_url,
            free_shipping_threshold=excluded.free_shipping_threshold,
            standard_shipping_bgn=excluded.standard_shipping_bgn,
            free_shipping_threshold_eur=excluded.free_shipping_threshold_eur,
            standard_shipping_eur=excluded.standard_shipping_eur,
            badge_color=excluded.badge_color;
    """, (code, name, base_url, free_shipping_threshold, standard_shipping_bgn, free_shipping_eur, standard_shipping_eur, badge_color))
    conn.commit()
    conn.close()

def upsert_product(prod: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (
            store_code, external_id, raw_title, clean_title, brand, category,
            form, flavor, weight_g, servings, protein_pct, price_bgn,
            old_price_bgn, price_eur, old_price_eur, discount_pct,
            price_per_100g, price_per_100g_eur, price_per_100g_protein,
            price_per_serving, price_per_serving_eur, in_stock, product_url, image_url
        ) VALUES (
            :store_code, :external_id, :raw_title, :clean_title, :brand, :category,
            :form, :flavor, :weight_g, :servings, :protein_pct, :price_bgn,
            :old_price_bgn, :price_eur, :old_price_eur, :discount_pct,
            :price_per_100g, :price_per_100g_eur, :price_per_100g_protein,
            :price_per_serving, :price_per_serving_eur, :in_stock, :product_url, :image_url
        )
    """, prod)
    conn.commit()
    conn.close()

def search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    store_code: Optional[str] = None,
    brand: Optional[str] = None,
    sort_by: str = "price_per_100g_asc"
) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        SELECT p.*, s.name as store_name, s.free_shipping_threshold, s.standard_shipping_bgn,
               s.free_shipping_threshold_eur, s.standard_shipping_eur, s.badge_color
        FROM products p
        JOIN stores s ON p.store_code = s.code
        WHERE 1=1
    """
    params = []

    if query:
        q_clean = f"%{query.strip().lower()}%"
        sql += " AND (LOWER(p.clean_title) LIKE ? OR LOWER(p.brand) LIKE ? OR LOWER(p.category) LIKE ?)"
        params.extend([q_clean, q_clean, q_clean])

    if category and category != "all":
        sql += " AND p.category = ?"
        params.append(category)

    if store_code and store_code != "all":
        sql += " AND p.store_code = ?"
        params.append(store_code)

    if brand and brand != "all":
        sql += " AND p.brand = ?"
        params.append(brand)

    # Sorting options (EUR primary)
    if sort_by in ("price_asc", "price_eur_asc"):
        sql += " ORDER BY p.price_eur ASC"
    elif sort_by in ("price_desc", "price_eur_desc"):
        sql += " ORDER BY p.price_eur DESC"
    elif sort_by in ("price_per_100g_asc", "price_per_100g_eur_asc"):
        sql += " ORDER BY CASE WHEN p.price_per_100g_eur IS NULL OR p.price_per_100g_eur <= 0 THEN 9999 ELSE p.price_per_100g_eur END ASC"
    elif sort_by in ("price_per_serving_asc", "price_per_serving_eur_asc"):
        sql += " ORDER BY CASE WHEN p.price_per_serving_eur IS NULL OR p.price_per_serving_eur <= 0 THEN 9999 ELSE p.price_per_serving_eur END ASC"
    elif sort_by == "discount_desc":
        sql += " ORDER BY p.discount_pct DESC"
    elif sort_by == "protein_desc":
        sql += " ORDER BY p.protein_pct DESC"
    else:
        sql += " ORDER BY p.price_eur ASC"

    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_stores() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stores ORDER BY name ASC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_categories_and_brands() -> Dict[str, List[str]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL ORDER BY category ASC")
    categories = [r[0] for r in cursor.fetchall()]
    cursor.execute("SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL ORDER BY brand ASC")
    brands = [r[0] for r in cursor.fetchall()]
    conn.close()
    return {"categories": categories, "brands": brands}
