import sqlite3


class BraindumpDatabase:
    def __init__(self, db_file):
        self.db_file = db_file

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY,
                    body TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    sent INTEGER DEFAULT 0
                )
            """
            )
            conn.commit()

    def add_note(self, body, timestamp):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notes (body, timestamp) VALUES (?, ?)", (body, timestamp)
            )
            conn.commit()
            return cursor.lastrowid

    def get_unsent_notes(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, body, timestamp FROM notes WHERE sent = 0"
            )
            return cursor.fetchall()

    def mark_notes_as_sent(self, note_ids):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE notes SET sent = 1 WHERE id IN ({})".format(
                    ",".join("?" for _ in note_ids)
                ),
                note_ids,
            )
            conn.commit()
