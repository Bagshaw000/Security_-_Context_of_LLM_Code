import random
import threading
import time

class ATMController:
    def __init__(self, num_atms):
        self.num_atms = num_atms
        self.atm_states = [0] * num_atms
        self.lock = threading.Lock()

    def monitor_atms(self):
        while True:
            with self.lock:
                for i in range(self.num_atms):
                    if self.atm_states[i] == 0:
                        self.atm_states[i] = 1
                        print(f"ATM {i} is now active.")
                    elif self.atm_states[i] == 1:
                        if random.random() < 0.1:
                            self.atm_states[i] = 2
                            print(f"ATM {i} has encountered an error.")
                    elif self.atm_states[i] == 2:
                        if random.random() < 0.5:
                            self.atm_states[i] = 1
                            print(f"ATM {i} has been repaired.")
            time.sleep(5)

    def start(self):
        monitor_thread = threading.Thread(target=self.monitor_atms)
        monitor_thread.start()

controller = ATMController(10)
controller.start()