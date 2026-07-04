class ATMController:
    def __init__(self, atm_network):
        self.atm_network = atm_network
        self.registered_atms = {}
        self.registered_users = {}

    def register_atm(self, atm_id, location, status):
        self.registered_atms[atm_id] = {'location': location, 'status': status}

    def unregister_atm(self, atm_id):
        if atm_id in self.registered_atms:
            del self.registered_atms[atm_id]

    def register_user(self, user_id, account_info):
        self.registered_users[user_id] = account_info

    def authenticate_user(self, user_id, password):
        if user_id in self.registered_users:
            if self.registered_users[user_id]['password'] == password:
                return True
        return False

    def get_atm_status(self, atm_id):
        if atm_id in self.registered_atms:
            return self.registered_atms[atm_id]['status']
        return None

    def update_atm_status(self, atm_id, new_status):
        if atm_id in self.registered_atms:
            self.registered_atms[atm_id]['status'] = new_status

    def process_transaction(self, user_id, atm_id, transaction_type, amount):
        if user_id in self.registered_users and atm_id in self.registered_atms:
            if self.registered_atms[atm_id]['status'] == 'active':
                if transaction_type == 'withdrawal':
                    if self.registered_users[user_id]['balance'] >= amount:
                        self.registered_users[user_id]['balance'] -= amount
                        return True
                elif transaction_type == 'deposit':
                    self.registered_users[user_id]['balance'] += amount
                    return True
        return False