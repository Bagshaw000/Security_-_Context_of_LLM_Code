class ATMController:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm_id, atm_info):
        self.atms[atm_id] = atm_info

    def remove_atm(self, atm_id):
        if atm_id in self.atms:
            del self.atms[atm_id]
        else:
            print("ATM not found")

    def update_atm(self, atm_id, atm_info):
        if atm_id in self.atms:
            self.atms[atm_id] = atm_info
        else:
            print("ATM not found")

    def get_atm(self, atm_id):
        return self.atms.get(atm_id)

class ATMNetworkController:
    def __init__(self):
        self.controller = ATMController()

    def add_network_atm(self, atm_id, atm_info):
        self.controller.add_atm(atm_id, atm_info)

    def remove_network_atm(self, atm_id):
        self.controller.remove_atm(atm_id)

    def update_network_atm(self, atm_id, atm_info):
        self.controller.update_atm(atm_id, atm_info)

    def get_network_atm(self, atm_id):
        return self.controller.get_atm(atm_id)

class ATMSystem:
    def __init__(self):
        self.network_controller = ATMNetworkController()

    def add_system_atm(self, atm_id, atm_info):
        self.network_controller.add_network_atm(atm_id, atm_info)

    def remove_system_atm(self, atm_id):
        self.network_controller.remove_network_atm(atm_id)

    def update_system_atm(self, atm_id, atm_info):
        self.network_controller.update_network_atm(atm_id, atm_info)

    def get_system_atm(self, atm_id):
        return self.network_controller.get_network_atm(atm_id)