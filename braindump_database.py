import sqlite3


class BraindumpDatabase:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                body TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sent INTEGER DEFAULT 0
            )
        """
        )
        self.conn.commit()

    def add_note(self, body, timestamp):
        self.cursor.execute(
            "INSERT INTO notes (body, timestamp) VALUES (?, ?)", (body, timestamp)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_unsent_notes(self):
        self.cursor.execute(
            "SELECT id, body, timestamp FROM notes WHERE sent = 0")
        return self.cursor.fetchall()

    def mark_notes_as_sent(self, note_ids):
        self.cursor.execute(
            "UPDATE notes SET sent = 1 WHERE id IN ({})".format(
                ",".join("?" for _ in note_ids)
            ),
            note_ids,
        )
        self.conn.commit()
