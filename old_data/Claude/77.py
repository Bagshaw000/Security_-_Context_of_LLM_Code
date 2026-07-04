import time

user_interactions = []

def track_user_interaction(page, action, timestamp=None):
    if not timestamp:
        timestamp = time.time()
    user_interactions.append({
        "page": page,
        "action": action,
        "timestamp": timestamp
    })

track_user_interaction("home", "page_load")
track_user_interaction("about", "click")
track_user_interaction("contact", "form_submit", timestamp=1618304400)