import datetime

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = {}

    def track_interaction(self, user_id, page_url, interaction_type, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []
        self.user_interactions[user_id].append({
            'page_url': page_url,
            'interaction_type': interaction_type,
            'timestamp': timestamp
        })

    def get_user_interactions(self, user_id):
        return self.user_interactions.get(user_id, [])