"""
File: network_isolator_v0.1.py
Phase: 3 - MVP Backend (Network Isolation Logic)
Project: Normal Users Bridge-Switch (NUBS)
Description: Safely isolates network traffic using Windows Firewall with a 
             mandatory 30-second auto-rollback failsafe to prevent user lockout.
"""

import subprocess
import threading
import time
import sys
import ctypes

class NUBSIsolator:
    def __init__(self):
        self.is_isolated = False
        self.rule_name = "NUBS_Emergency_Block_All"
        self.rollback_timer = None
        self.is_admin = self._check_admin()

    def _check_admin(self):
        """Checks if the script is running with Administrator privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def _log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        mode = "[LIVE]" if self.is_admin else "[SIMULATION]"
        print(f"[{timestamp}] NUBS {mode}: {message}")

    def _execute_command(self, command):
        """Safely executes a shell command, or simulates it if not admin."""
        if not self.is_admin:
            self._log(f"SIMULATED COMMAND: {command}")
            return True
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            self._log(f"ERROR executing command: {e.stderr.strip()}")
            return False

    def _auto_rollback(self):
        """Safety Failsafe: Automatically restores network after 30 seconds."""
        self._log("⏱️  SAFETY FAILSAFE: 30-second auto-rollback timer started.")
        time.sleep(30)
        if self.is_isolated:
            self._log("⚠️  AUTO-ROLLBACK TRIGGERED: No manual recovery detected. Restoring network.")
            self.rebuild_bridge()

    def blow_bridge(self):
        """Severs outbound network traffic via Windows Firewall."""
        if self.is_isolated:
            self._log("INFO: Network is already isolated.")
            return

        self._log("ACTION: Triggering KILL SWITCH.")
        
        # Windows Firewall command to block all outbound traffic
        cmd = f'netsh advfirewall firewall add rule name="{self.rule_name}" dir=out action=block enable=yes profile=any'
        
        if self._execute_command(cmd):
            self.is_isolated = True
            self._log("STATUS: 🛑 NETWORK ISOLATED. All outbound traffic blocked.")
            
            # Start the safety failsafe timer
            self.rollback_timer = threading.Thread(target=self._auto_rollback, daemon=True)
            self.rollback_timer.start()

    def rebuild_bridge(self):
        """Restores network traffic by removing the firewall rule."""
        if not self.is_isolated:
            self._log("INFO: Network is already active.")
            return

        self._log("ACTION: Triggering RECOVERY.")
        
        # Windows Firewall command to delete the block rule
        cmd = f'netsh advfirewall firewall delete rule name="{self.rule_name}"'
        
        if self._execute_command(cmd):
            self.is_isolated = False
            self._log("STATUS: 🟢 BRIDGE ACTIVE. Network restored.")

    def show_status(self):
        status = "🛑 ISOLATED (Kill Switch Active)" if self.is_isolated else "🟢 ACTIVE (Normal)"
        admin_status = "Administrator" if self.is_admin else "Standard User (Simulation Mode)"
        print(f"\n--- NUBS SYSTEM STATUS ---")
        print(f"Privilege Level: {admin_status}")
        print(f"Network State  : {status}")
        print(f"--------------------------\n")

def main():
    isolator = NUBSIsolator()
    
    if not isolator.is_admin:
        print("\n⚠️  WARNING: Not running as Administrator.")
        print("NUBS will run in SIMULATION MODE. No actual firewall rules will be changed.")
        print("To test live isolation, close this and run PowerShell as Administrator.\n")

    print("=== NUBS NETWORK ISOLATOR v0.1 ===")
    print("Commands: [s]tatus, [k]ill switch, [r]ebuild bridge, [q]uit")
    
    while True:
        cmd = input("\nEnter command: ").strip().lower()
        
        if cmd == 's':
            isolator.show_status()
        elif cmd == 'k':
            isolator.blow_bridge()
        elif cmd == 'r':
            isolator.rebuild_bridge()
        elif cmd == 'q':
            # Clean up on exit
            if isolator.is_isolated:
                isolator._log("Cleanup: Restoring network before exit.")
                isolator.rebuild_bridge()
            isolator._log("System shutting down.")
            sys.exit(0)
        else:
            print("Invalid command. Please use s, k, r, or q.")

if __name__ == "__main__":
    main()