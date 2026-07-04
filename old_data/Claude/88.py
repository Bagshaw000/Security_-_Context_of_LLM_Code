import datetime
import uuid

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = {}

    def track_user_interaction(self, user_id, page_url, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        interaction_id = str(uuid.uuid4())
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []
        self.user_interactions[user_id].append({
            'interaction_id': interaction_id,
            'page_url': page_url,
            'timestamp': timestamp
        })

    def get_user_interactions(self, user_id):
        return self.user_interactions.get(user_id, [])

    def get_all_user_interactions(self):
        return self.user_interactions