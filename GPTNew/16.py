class UserInteractionTracker:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def track_interaction(self, user_id, interaction_type, metadata):
        if self._is_valid_user(user_id) and self._is_valid_interaction(interaction_type):
            interaction_data = {
                'user_id': user_id,
                'interaction_type': interaction_type,
                'metadata': self._sanitize_metadata(metadata),
                'timestamp': self._get_current_timestamp()
            }
            self._store_interaction(interaction_data)

    def _is_valid_user(self, user_id):
        
        return True  

    def _is_valid_interaction(self, interaction_type):
        valid_interactions = ['click', 'view', 'purchase']
        return interaction_type in valid_interactions

    def _sanitize_metadata(self, metadata):
        
        return {key: self._escape_html(value) for key, value in metadata.items()}

    def _escape_html(self, value):
        return value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def _get_current_timestamp(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def _store_interaction(self, interaction_data):
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user_interactions (user_id, interaction_type, metadata, timestamp) VALUES (%s, %s, %s, %s)",
                (interaction_data['user_id'], interaction_data['interaction_type'], interaction_data['metadata'], interaction_data['timestamp'])
            )
        self.db_connection.commit()

class DatabaseConnection:
    def __init__(self, connection_string):
        import psycopg2
        self.connection = psycopg2.connect(connection_string)

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


db_connection = DatabaseConnection("your_connection_string")
tracker = UserInteractionTracker(db_connection)
tracker.track_interaction("user123", "click", {"page": "home", "button": "subscribe"})