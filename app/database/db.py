import sqlite3
from pathlib import Path
from datetime import datetime

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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            file_name TEXT,
            file_path TEXT,
            category TEXT,
            upload_date TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            title TEXT NOT NULL,
            due_date TEXT,
            status TEXT DEFAULT 'Bekliyor',
            notes TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
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


def update_client(client_id, name, tax_no, tax_office, phone, email, contact_person, notes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE clients
        SET name=?, tax_no=?, tax_office=?, phone=?, email=?, contact_person=?, notes=?
        WHERE id=?
    """, (name, tax_no, tax_office, phone, email, contact_person, notes, client_id))
    conn.commit()
    conn.close()


def delete_client(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
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


def get_client(client_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, tax_no, tax_office, phone, email, contact_person, notes
        FROM clients
        WHERE id=?
    """, (client_id,))
    row = cur.fetchone()
    conn.close()
    return row


def add_document(client_id, file_name, file_path, category):
    conn = get_connection()
    cur = conn.cursor()
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO documents
        (client_id, file_name, file_path, category, upload_date)
        VALUES (?, ?, ?, ?, ?)
    """, (client_id, file_name, file_path, category, upload_date))
    conn.commit()
    conn.close()


def list_documents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT documents.id, clients.name, documents.file_name,
               documents.category, documents.upload_date, documents.file_path
        FROM documents
        LEFT JOIN clients ON clients.id = documents.client_id
        ORDER BY documents.upload_date DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_document(document_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM documents WHERE id=?", (document_id,))
    conn.commit()
    conn.close()


def count_clients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM clients")
    count = cur.fetchone()[0]
    conn.close()
    return count


def count_documents():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM documents")
    count = cur.fetchone()[0]
    conn.close()
    return count


def count_reminders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reminders")
    count = cur.fetchone()[0]
    conn.close()
    return count
def add_reminder(client_id, title, due_date, status, notes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reminders
        (client_id, title, due_date, status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (client_id, title, due_date, status, notes))
    conn.commit()
    conn.close()


def list_reminders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT reminders.id, clients.name, reminders.title,
               reminders.due_date, reminders.status, reminders.notes
        FROM reminders
        LEFT JOIN clients ON clients.id = reminders.client_id
        ORDER BY reminders.due_date ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_reminder(reminder_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
    conn.commit()
    conn.close()