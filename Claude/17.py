import datetime
import os

class UserInteractionTracker:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.interactions = []

    def track_user_interaction(self, user_id, page_url, timestamp=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        interaction = {
            'user_id': user_id,
            'page_url': page_url,
            'timestamp': timestamp
        }
        self.interactions.append(interaction)

    def save_interactions_to_file(self):
        try:
            os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
            with open(self.log_file_path, 'a') as log_file:
                for interaction in self.interactions:
                    log_file.write(f"{interaction['user_id']},{interaction['page_url']},{interaction['timestamp']}\n")
            self.interactions = []
        except Exception as e:
            print(f"Error saving interactions to file: {e}")