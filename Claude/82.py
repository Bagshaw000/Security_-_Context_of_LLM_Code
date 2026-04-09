import datetime

class UserInteractionTracker:
    def __init__(self):
        self.interactions = []

    def track_interaction(self, user_id, page_url, timestamp=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        self.interactions.append({
            'user_id': user_id,
            'page_url': page_url,
            'timestamp': timestamp
        })

    def get_user_interactions(self, user_id):
        return [i for i in self.interactions if i['user_id'] == user_id]

    def get_all_interactions(self):
        return self.interactions