import time
import datetime

class UserInteractionTracker:
    def __init__(self):
        self.interaction_data = []

    def track_page_view(self, user_id, page_url, timestamp=None):
        if not timestamp:
            timestamp = time.time()
        self.interaction_data.append({
            'user_id': user_id,
            'action': 'page_view',
            'page_url': page_url,
            'timestamp': timestamp
        })

    def track_button_click(self, user_id, button_label, page_url, timestamp=None):
        if not timestamp:
            timestamp = time.time()
        self.interaction_data.append({
            'user_id': user_id,
            'action': 'button_click',
            'button_label': button_label,
            'page_url': page_url,
            'timestamp': timestamp
        })

    def track_form_submission(self, user_id, form_data, page_url, timestamp=None):
        if not timestamp:
            timestamp = time.time()
        self.interaction_data.append({
            'user_id': user_id,
            'action': 'form_submission',
            'form_data': form_data,
            'page_url': page_url,
            'timestamp': timestamp
        })

    def get_interaction_data(self):
        return self.interaction_data

    def export_to_csv(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['user_id', 'action', 'page_url', 'button_label', 'form_data', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for interaction in self.interaction_data:
                row = {
                    'user_id': interaction['user_id'],
                    'action': interaction['action'],
                    'page_url': interaction['page_url'],
                    'button_label': interaction.get('button_label', ''),
                    'form_data': interaction.get('form_data', ''),
                    'timestamp': datetime.datetime.fromtimestamp(interaction['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                }
                writer.writerow(row)