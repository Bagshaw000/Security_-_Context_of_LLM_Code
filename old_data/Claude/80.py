import os
import datetime
import json

class WebsiteTracker:
    def __init__(self, log_directory):
        self.log_directory = log_directory
        self.user_interactions = {}

    def track_user_interaction(self, user_id, page_url, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()

        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []

        self.user_interactions[user_id].append({
            'page_url': page_url,
            'timestamp': timestamp
        })

        self.save_log()

    def save_log(self):
        log_file = os.path.join(self.log_directory, 'user_interactions.json')
        with open(log_file, 'w') as f:
            json.dump(self.user_interactions, f, indent=4)

    def load_log(self):
        log_file = os.path.join(self.log_directory, 'user_interactions.json')
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                self.user_interactions = json.load(f)