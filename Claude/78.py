import datetime
import uuid

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = []

    def track_interaction(self, user_id, page_url, timestamp=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        interaction = {
            'user_id': user_id,
            'page_url': page_url,
            'timestamp': timestamp
        }
        self.user_interactions.append(interaction)

    def get_user_interactions(self, user_id):
        return [i for i in self.user_interactions if i['user_id'] == user_id]

    def get_all_interactions(self):
        return self.user_interactions