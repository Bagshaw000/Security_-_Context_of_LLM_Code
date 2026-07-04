import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class UserInteractionTracker:
    def __init__(self, session_timeout: int = 1800):
        self.user_interactions: Dict[str, List[Tuple[float, str]]] = {}
        self.session_timeout = session_timeout
        self.logger = logging.getLogger(__name__)

    def track_user_interaction(self, user_id: str, interaction_type: str):
        if user_id not in self.user_interactions:
            self.user_interactions[user_id] = []
        self.user_interactions[user_id].append((time.time(), interaction_type))
        self.logger.info(f"Tracked user {user_id} interaction: {interaction_type}")

    def get_user_session_activity(self, user_id: str) -> List[Tuple[float, str]]:
        if user_id not in self.user_interactions:
            return []
        now = time.time()
        session_activities = [
            (timestamp, interaction_type)
            for timestamp, interaction_type in self.user_interactions[user_id]
            if now - timestamp <= self.session_timeout
        ]
        return session_activities

    def get_active_user_ids(self) -> List[str]:
        now = time.time()
        active_user_ids = [
            user_id
            for user_id, interactions in self.user_interactions.items()
            if now - interactions[-1][0] <= self.session_timeout
        ]
        return active_user_ids

    def clear_expired_user_sessions(self):
        now = time.time()
        self.user_interactions = {
            user_id: [
                (timestamp, interaction_type)
                for timestamp, interaction_type in interactions
                if now - timestamp <= self.session_timeout
            ]
            for user_id, interactions in self.user_interactions.items()
        }