import sqlite3
from datetime import datetime

class UserInteractionTracker:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute()
        self.conn.commit()

    def track_interaction(self, user_id, interaction_type):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO user_interactions VALUES (?, ?, ?)', (user_id, interaction_type, timestamp))
        self.conn.commit()


tracker = UserInteractionTracker('interactions.db')

tracker.track_interaction('user1', 'page_view')
tracker.track_interaction('user2', 'click')
tracker.track_interaction('user1', 'submit')