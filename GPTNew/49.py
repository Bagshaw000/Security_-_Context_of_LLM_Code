class Device:
    def __init__(self, device_id, owner_id):
        self.device_id = device_id
        self.owner_id = owner_id
        self.is_authenticated = False

    def authenticate(self, token):
        
        if self.validate_token(token):
            self.is_authenticated = True
            return True
        return False

    def validate_token(self, token):
        
        return token == "secure_token"

class DeviceRegistry:
    def __init__(self):
        self.devices = {}

    def register_device(self, device):
        if device.device_id in self.devices:
            raise ValueError("Device already registered.")
        self.devices[device.device_id] = device

    def authenticate_device(self, device_id, token):
        if device_id in self.devices:
            return self.devices[device_id].authenticate(token)
        raise ValueError("Device not found.")

class DeviceManager:
    def __init__(self):
        self.registry = DeviceRegistry()

    def register_new_device(self, device_id, owner_id):
        new_device = Device(device_id, owner_id)
        self.registry.register_device(new_device)

    def authenticate_device(self, device_id, token):
        return self.registry.authenticate_device(device_id, token)


if __name__ == "__main__":
    manager = DeviceManager()
    manager.register_new_device("device_123", "owner_456")
    is_authenticated = manager.authenticate_device("device_123", "secure_token")
    print(f"Device authenticated: {is_authenticated}")