import datetime

class UserInteractionTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.interactions = []

    def track_page_view(self, page_url):
        timestamp = datetime.datetime.now()
        self.interactions.append({"type": "page_view", "timestamp": timestamp, "page_url": page_url})

    def track_button_click(self, button_id):
        timestamp = datetime.datetime.now()
        self.interactions.append({"type": "button_click", "timestamp": timestamp, "button_id": button_id})

    def track_form_submission(self, form_id, form_data):
        timestamp = datetime.datetime.now()
        self.interactions.append({"type": "form_submission", "timestamp": timestamp, "form_id": form_id, "form_data": form_data})

    def get_interactions(self):
        return self.interactions