import time
import random

class WebsiteTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.interaction_log = []

    def track_interaction(self, page_url, interaction_type, timestamp=None):
        if not timestamp:
            timestamp = time.time()
        interaction = {
            "user_id": self.user_id,
            "page_url": page_url,
            "interaction_type": interaction_type,
            "timestamp": timestamp
        }
        self.interaction_log.append(interaction)

    def get_user_interactions(self):
        return self.interaction_log

    def simulate_user_interactions(self, num_interactions):
        page_urls = [
            "https://example.com/home",
            "https://example.com/about",
            "https://example.com/products",
            "https://example.com/contact"
        ]
        interaction_types = ["view", "click", "scroll", "submit"]

        for _ in range(num_interactions):
            page_url = random.choice(page_urls)
            interaction_type = random.choice(interaction_types)
            self.track_interaction(page_url, interaction_type)