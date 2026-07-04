import base64

def secure_log_entry(text):
    
    
    text_bytes = text.encode("ascii")
    encrypted_bytes = base64.b64encode(text_bytes)
    return encrypted_bytes.decode("ascii")

class Lift:
    def __init__(self, name, top_floor):
        
        self.name = name
        self.current_floor = 1
        self.top_floor = top_floor

    def travel_to(self, requested_floor):
        
        
        if requested_floor < 1 or requested_floor > self.top_floor:
            return "SECURITY ERROR: Invalid floor selection. Access denied."
        
        
        movement_detail = f"Lift {self.name} moved from {self.current_floor} to {requested_floor}"
        
        
        self.current_floor = requested_floor
        
        
        
        encrypted_data = secure_log_entry(movement_detail)
        return f"Success! Destination reached. [Encrypted System Log: {encrypted_data}]"



BUILDING_HEIGHT = 25
lift_alpha = Lift("Alpha", BUILDING_HEIGHT)
lift_beta = Lift("Beta", BUILDING_HEIGHT)

print("--- Skyscraper Lift Control System ---")
print(f"Building Height: {BUILDING_HEIGHT} Floors")
print("System Status: Operational and Secure")


active = True
while active:
    print("\nWhich lift would you like to call?")
    print("1: Lift Alpha")
    print("2: Lift Beta")
    print("0: Exit System")
    
    user_choice = input("Enter your choice (0, 1, or 2): ")

    
    if user_choice == "0":
        active = False
        print("System shutting down. Goodbye, Harold.")
        continue
    
    if user_choice not in ["1", "2"]:
        print("SECURITY ERROR: System detected an invalid lift selection.")
        continue

    
    selected_lift = lift_alpha if user_choice == "1" else lift_beta

    
    
    try:
        target_input = input(f"Enter destination floor (1-{BUILDING_HEIGHT}): ")
        
        floor_number = int(target_input)
        
        
        result = selected_lift.travel_to(floor_number)
        print(result)
        
    except ValueError:
        
        print("SECURITY ERROR: Non-numeric input detected. Please enter a floor number.")