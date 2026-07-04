import time
from datetime import datetime

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = []

    def track_page_view(self, user_id, page_url, timestamp=None):
        if not timestamp:
            timestamp = datetime.now()
        self.user_interactions.append({
            'user_id': user_id,
            'page_url': page_url,
            'timestamp': timestamp
        })

    def track_button_click(self, user_id, button_id, timestamp=None):
        if not timestamp:
            timestamp = datetime.now()
        self.user_interactions.append({
            'user_id': user_id,
            'button_id': button_id,
            'timestamp': timestamp
        })

    def track_form_submission(self, user_id, form_id, timestamp=None):
        if not timestamp:
            timestamp = datetime.now()
        self.user_interactions.append({
            'user_id': user_id,
            'form_id': form_id,
            'timestamp': timestamp
        })

    def get_user_interactions(self, user_id):
        return [interaction for interaction in self.user_interactions if interaction['user_id'] == user_id]

    def get_interactions_by_time_range(self, start_time, end_time):
        return [interaction for interaction in self.user_interactions if start_time <= interaction['timestamp'] <= end_time]