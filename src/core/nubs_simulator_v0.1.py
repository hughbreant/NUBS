"""
File: nubs_simulator_v0.1.py
Phase: 1 - Setup & Discovery
Project: Normal Users Bridge-Switch (NUBS)
Description: A simple CLI state machine to verify the core logic 
             of the 'Bridge' (Active) and 'Kill Switch' (Isolated) states.
"""

import time
import sys

class NUBSSimulator:
    def __init__(self):
        # True = Bridge Active (Connected), False = Switch Killed (Isolated)
        self.is_bridge_active = True 
        self.log = []

    def _log_event(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] NUBS: {message}"
        self.log.append(log_entry)
        print(log_entry)

    def blow_bridge(self):
        """Severs the network connection (The Kill Switch)."""
        if not self.is_bridge_active:
            self._log_event("WARNING: Switch is already killed. Network is already isolated.")
            return
        
        self._log_event("ACTION: User triggered KILL SWITCH.")
        self._log_event("STATUS: Severing all inbound/outbound network traffic...")
        time.sleep(1) # Simulate execution time
        self.is_bridge_active = False
        self._log_event("STATUS: 🛑 NETWORK ISOLATED. Device is in safe mode.")

    def rebuild_bridge(self):
        """Restores the network connection after verification."""
        if self.is_bridge_active:
            self._log_event("INFO: Bridge is already active. Network is connected.")
            return
            
        self._log_event("ACTION: User triggered RECOVERY.")
        self._log_event("STATUS: Running local threat verification...")
        time.sleep(1) # Simulate AI scan
        self._log_event("STATUS: Verification passed. Rebuilding bridge...")
        self.is_bridge_active = True
        self._log_event("STATUS: 🟢 BRIDGE ACTIVE. Network restored.")

    def show_status(self):
        status = "🟢 BRIDGE ACTIVE (Connected)" if self.is_bridge_active else "🛑 SWITCH KILLED (Isolated)"
        print(f"\n--- NUBS CURRENT STATUS: {status} ---\n")

def main():
    simulator = NUBSSimulator()
    simulator._log_event("System initialized. Awaiting user command.")
    
    print("\n=== NUBS (Normal Users Bridge-Switch) SIMULATOR v0.1 ===")
    print("Commands: [s]tatus, [k]ill switch, [r]ebuild bridge, [q]uit")
    
    while True:
        cmd = input("\nEnter command: ").strip().lower()
        
        if cmd == 's':
            simulator.show_status()
        elif cmd == 'k':
            simulator.blow_bridge()
        elif cmd == 'r':
            simulator.rebuild_bridge()
        elif cmd == 'q':
            simulator._log_event("System shutting down.")
            sys.exit(0)
        else:
            print("Invalid command. Please use s, k, r, or q.")

if __name__ == "__main__":
    main()