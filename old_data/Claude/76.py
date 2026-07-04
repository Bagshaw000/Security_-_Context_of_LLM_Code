import datetime
import sqlite3


conn = sqlite3.connect('user_interactions.db')
c = conn.cursor()


c.execute()

def track_user_interaction(user_id, page_url, interaction_type):
    
    c.execute("INSERT INTO user_interactions (user_id, page_url, interaction_type, timestamp) VALUES (?, ?, ?, ?)", 
              (user_id, page_url, interaction_type, datetime.datetime.now()))
    conn.commit()


track_user_interaction('user123', 'https://example.com/homepage', 'pageview')
track_user_interaction('user123', 'https://example.com/product', 'click')
track_user_interaction('user456', 'https://example.com/signup', 'form_submit')