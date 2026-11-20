"""
File: network_heuristic_scanner_v0.1.py
Phase: 2 - Architecture & Threat Modeling
Project: Normal Users Bridge-Switch (NUBS)
Description: Simulates a local heuristic scan of network interfaces and 
             file activity to demonstrate the AI monitoring concept safely.
"""

import time
import random
import sys

class NUBSHeuristicScanner:
    def __init__(self):
        self.is_scanning = False
        self.threat_level = "LOW"

    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] NUBS SCAN: {message}")

    def check_network_interfaces(self):
        """Simulates checking active network adapters."""
        self._log("Querying local network interfaces...")
        time.sleep(0.5)
        interfaces = ["Wi-Fi (Active)", "Ethernet (Disconnected)", "Bluetooth (Active)"]
        self._log(f"Found {len(interfaces)} interfaces. Primary: Wi-Fi")
        return True

    def run_heuristic_scan(self):
        """Simulates an on-device AI checking for anomalous behavior."""
        self._log("Starting local heuristic behavior analysis...")
        self.is_scanning = True
        time.sleep(1.5) # Simulate processing time
        
        # Simulate a random minor anomaly for demonstration purposes
        anomaly_detected = random.choice([False, False, False, True]) 
        
        if anomaly_detected:
            self._log("⚠️  ANOMALY DETECTED: Unusual outbound data pattern on port 443.")
            self._log("ACTION: Flagging for user review. Threat Level raised to MEDIUM.")
            self.threat_level = "MEDIUM"
        else:
            self._log("✅ Heuristic scan complete. No anomalous behavior detected.")
            self.threat_level = "LOW"
            
        self.is_scanning = False
        return self.threat_level

    def get_status_report(self):
        """Returns a quick summary of the system state."""
        status = "SCANNING" if self.is_scanning else "IDLE"
        print(f"\n--- NUBS SYSTEM REPORT ---")
        print(f"Scanner Status : {status}")
        print(f"Threat Level   : {self.threat_level}")
        print(f"--------------------------\n")

def main():
    scanner = NUBSHeuristicScanner()
    print("\n=== NUBS HEURISTIC SCANNER v0.1 ===")
    print("Commands: [r]un scan, [s]tatus, [q]uit")
    
    while True:
        cmd = input("\nEnter command: ").strip().lower()
        
        if cmd == 'r':
            scanner.check_network_interfaces()
            scanner.run_heuristic_scan()
        elif cmd == 's':
            scanner.get_status_report()
        elif cmd == 'q':
            print("\nNUBS Scanner shutting down. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid command. Please use r, s, or q.")

if __name__ == "__main__":
    main()