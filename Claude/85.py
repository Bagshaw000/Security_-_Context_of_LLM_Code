import datetime
import uuid

class UserInteractionTracker:
    def __init__(self):
        self.user_interactions = []

    def track_user_interaction(self, user_id, page_url, interaction_type, timestamp=None):
        if not timestamp:
            timestamp = datetime.datetime.now()
        interaction = {
            "user_id": user_id,
            "page_url": page_url,
            "interaction_type": interaction_type,
            "timestamp": timestamp
        }
        self.user_interactions.append(interaction)

    def get_user_interactions(self, user_id=None, page_url=None):
        if user_id and page_url:
            return [i for i in self.user_interactions if i["user_id"] == user_id and i["page_url"] == page_url]
        elif user_id:
            return [i for i in self.user_interactions if i["user_id"] == user_id]
        elif page_url:
            return [i for i in self.user_interactions if i["page_url"] == page_url]
        else:
            return self.user_interactions


tracker = UserInteractionTracker()
tracker.track_user_interaction(user_id=str(uuid.uuid4()), page_url="/homepage", interaction_type="page_view")
tracker.track_user_interaction(user_id=str(uuid.uuid4()), page_url="/about", interaction_type="click")
tracker.track_user_interaction(user_id=str(uuid.uuid4()), page_url="/homepage", interaction_type="page_view")

print(tracker.get_user_interactions())
print(tracker.get_user_interactions(user_id=tracker.user_interactions[0]["user_id"]))
print(tracker.get_user_interactions(page_url="/homepage"))