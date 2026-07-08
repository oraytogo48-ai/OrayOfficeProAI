import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

DB_FILE = DATA_DIR / "oray_office.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tax_no TEXT,
            tax_office TEXT,
            phone TEXT,
            email TEXT,
            contact_person TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_client(name, tax_no, tax_office, phone, email, contact_person, notes):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clients
        (name, tax_no, tax_office, phone, email, contact_person, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, tax_no, tax_office, phone, email, contact_person, notes))

    conn.commit()
    conn.close()


def list_clients():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, tax_no, tax_office, phone, email, contact_person
        FROM clients
        ORDER BY name ASC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def count_clients():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM clients")
    count = cur.fetchone()[0]

    conn.close()
    return count