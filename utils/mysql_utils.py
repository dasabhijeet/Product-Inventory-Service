import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "inventory.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sku TEXT UNIQUE,
        price REAL,
        quantity INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS inventory_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        type TEXT,
        quantity INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Products

def create_product(payload):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO products (name, sku, price, quantity)
            VALUES (?, ?, ?, ?)
        """, (
            payload["name"],
            payload["sku"],
            payload["price"],
            payload["quantity"]
        ))
        conn.commit()
        return {"id": cur.lastrowid}

    finally:
        conn.close()

def get_products(limit, offset, search):
    conn = get_connection()
    cur = conn.cursor()

    if search:
        cur.execute("""
            SELECT * FROM products
            WHERE name LIKE ? OR sku LIKE ?
            LIMIT ? OFFSET ?
        """, (f"%{search}%", f"%{search}%", limit, offset))
    else:
        cur.execute("""
            SELECT * FROM products
            LIMIT ? OFFSET ?
        """, (limit, offset))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def get_product(pid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products WHERE id=?", (pid,))
    row = cur.fetchone()

    conn.close()
    return dict(row) if row else None

def update_product(pid, payload):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE products
        SET name=?, sku=?, price=?
        WHERE id=?
    """, (
        payload["name"],
        payload["sku"],
        payload["price"],
        pid
    ))

    conn.commit()
    conn.close()
    return {"updated": True}

def delete_product(pid):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()

    return {"deleted": True}

# Inventory

def add_stock(payload):
    conn = get_connection()
    cur = conn.cursor()

    try:
        conn.execute("BEGIN")

        cur.execute("SELECT quantity FROM products WHERE id=?", (payload["product_id"],))
        row = cur.fetchone()

        if not row:
            raise Exception("Product not found")

        new_qty = row["quantity"] + payload["quantity"]

        cur.execute("""
            UPDATE products SET quantity=? WHERE id=?
        """, (new_qty, payload["product_id"]))

        cur.execute("""
            INSERT INTO inventory_logs (product_id, type, quantity)
            VALUES (?, 'ADD', ?)
        """, (payload["product_id"], payload["quantity"]))

        conn.commit()
        return {"quantity": new_qty}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def remove_stock(payload):
    conn = get_connection()
    cur = conn.cursor()

    try:
        conn.execute("BEGIN")

        cur.execute("SELECT quantity FROM products WHERE id=?", (payload["product_id"],))
        row = cur.fetchone()

        if not row:
            raise Exception("Product not found")

        if row["quantity"] < payload["quantity"]:
            raise Exception("Insufficient stock")

        new_qty = row["quantity"] - payload["quantity"]

        cur.execute("""
            UPDATE products SET quantity=? WHERE id=?
        """, (new_qty, payload["product_id"]))

        cur.execute("""
            INSERT INTO inventory_logs (product_id, type, quantity)
            VALUES (?, 'REMOVE', ?)
        """, (payload["product_id"], payload["quantity"]))

        conn.commit()
        return {"quantity": new_qty}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()
