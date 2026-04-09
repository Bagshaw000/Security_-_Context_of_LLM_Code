import datetime
import uuid

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = {}

    def track_user_interaction(self, user_id, page_url, interaction_type, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now()
        interaction_id = str(uuid.uuid4())
        user_interaction = {
            'interaction_id': interaction_id,
            'user_id': user_id,
            'page_url': page_url,
            'interaction_type': interaction_type,
            'timestamp': timestamp
        }
        if user_id in self.user_interactions:
            self.user_interactions[user_id].append(user_interaction)
        else:
            self.user_interactions[user_id] = [user_interaction]

    def get_user_interactions(self, user_id):
        return self.user_interactions.get(user_id, [])

    def get_all_user_interactions(self):
        return sum(self.user_interactions.values(), [])