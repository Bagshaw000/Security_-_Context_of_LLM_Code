import sqlite3
from datetime import datetime


conn = sqlite3.connect('user_interactions.db')
c = conn.cursor()


c.execute()

def log_interaction(username, interaction_type):
    
    c.execute('INSERT INTO user_interactions (username, interaction_type, timestamp)
              VALUES (?, ?, ?)', (username, interaction_type, datetime.now()))
    
    
    conn.commit()


log_interaction('harold', 'logged in')
log_interaction('harold', 'started writing')