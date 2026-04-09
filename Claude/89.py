import datetime
import json
from collections import defaultdict

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = defaultdict(list)

    def track_user_interaction(self, user_id, page_url, timestamp=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        self.user_interactions[user_id].append({
            'page_url': page_url,
            'timestamp': timestamp.isoformat()
        })

    def get_user_interactions(self, user_id):
        return self.user_interactions[user_id]

    def save_interactions_to_file(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.user_interactions, f, indent=4)

    def load_interactions_from_file(self, file_path):
        with open(file_path, 'r') as f:
            self.user_interactions = json.load(f)