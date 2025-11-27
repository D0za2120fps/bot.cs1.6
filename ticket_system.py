import sqlite3
from datetime import datetime

class TicketSystem:
    def __init__(self):
        self.conn = sqlite3.connect("users.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nick TEXT,
                privilege TEXT,
                duration TEXT,
                password TEXT,
                status TEXT,
                created_at TEXT,
                screenshot TEXT
            )
        """)
        self.conn.commit()

    def create_ticket(self, user_id, data):
        self.cursor.execute("""
            INSERT INTO tickets (user_id, nick, privilege, duration, password, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, data['nick'], data['privilege'], data['duration'], data['password'],
            "Ожидает оплаты", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()

    def attach_screenshot(self, ticket_id, file_id):
        self.cursor.execute("UPDATE tickets SET screenshot=? WHERE id=?", (file_id, ticket_id))
        self.conn.commit()

    def find_ticket_by_user(self, user_id):
        self.cursor.execute("SELECT id FROM tickets WHERE user_id=? AND status='Ожидает оплаты'", (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_all_tickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        return self.cursor.fetchall()

    def confirm_ticket(self, ticket_id):
        self.cursor.execute("UPDATE tickets SET status='Оплата подтверждена' WHERE id=?", (ticket_id,))
        self.conn.commit()
