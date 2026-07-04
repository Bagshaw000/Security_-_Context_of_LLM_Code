import time
import uuid

class WebsiteTracker:
    def __init__(self):
        self.user_interactions = {}

    def track_user_interaction(self, user_id, page_url, interaction_time):
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []

        interaction = {
            "page_url": page_url,
            "interaction_time": interaction_time
        }
        self.user_interactions[user_id].append(interaction)

    def get_user_interactions(self, user_id):
        return self.user_interactions.get(user_id, [])


tracker = WebsiteTracker()

user_id_1 = str(uuid.uuid4())
tracker.track_user_interaction(user_id_1, "/home", time.time())
tracker.track_user_interaction(user_id_1, "/about", time.time() + 60)
tracker.track_user_interaction(user_id_1, "/contact", time.time() + 120)

user_id_2 = str(uuid.uuid4())
tracker.track_user_interaction(user_id_2, "/products", time.time())
tracker.track_user_interaction(user_id_2, "/pricing", time.time() + 30)

print(tracker.get_user_interactions(user_id_1))
print(tracker.get_user_interactions(user_id_2))