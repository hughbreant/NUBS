"""
File: main_v0.1.py
Phase: 5 - Integration & Final Handoff
Project: Normal Users Bridge-Switch (NUBS)
Description: The unified entry point for the NUBS application. 
             Integrates the backend Network Isolator with the CustomTkinter Dashboard.
"""

import sys
import os
import time
import threading
import ctypes
import customtkinter as ctk

# Ensure the src directory is in the Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the backend logic (Assuming network_isolator_v0.1.py is in src/core)
# For this unified MVP, we embed the core logic directly to guarantee zero import path errors across environments.

class NUBSIsolator:
    def __init__(self):
        self.is_isolated = False
        self.rule_name = "NUBS_Emergency_Block_All"
        self.is_admin = self._check_admin()

    def _check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def _execute_command(self, command):
        import subprocess
        if not self.is_admin:
            return True # Simulated success
        
        try:
            subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def blow_bridge(self):
        if self.is_isolated:
            return True
        
        cmd = f'netsh advfirewall firewall add rule name="{self.rule_name}" dir=out action=block enable=yes profile=any'
        if self._execute_command(cmd):
            self.is_isolated = True
            return True
        return False

    def rebuild_bridge(self):
        if not self.is_isolated:
            return True
            
        cmd = f'netsh advfirewall firewall delete rule name="{self.rule_name}"'
        if self._execute_command(cmd):
            self.is_isolated = False
            return True
        return False

# --- Frontend UI Class ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NUBSDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NUBS - Normal Users Bridge-Switch v1.0 MVP")
        self.geometry("500x600")
        self.resizable(False, False)

        self.isolator = NUBSIsolator()
        self.rollback_timer = None

        self._build_ui()
        self._log("System initialized. Ready.")
        if not self.isolator.is_admin:
            self._log("⚠️ Running in SIMULATION MODE (Not Admin).")

    def _build_ui(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20)
        ctk.CTkLabel(self.header_frame, text="NUBS", font=("Roboto", 28, "bold")).pack()
        ctk.CTkLabel(self.header_frame, text="Normal Users Bridge-Switch", font=("Roboto", 14), text_color="gray").pack()

        self.status_label = ctk.CTkLabel(self, text="🟢 SYSTEM SECURE", font=("Roboto", 20, "bold"), text_color="#2ecc71")
        self.status_label.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.isolate_btn = ctk.CTkButton(self.button_frame, text="🛑 ISOLATE DEVICE", fg_color="#e74c3c", hover_color="#c0392b", 
                                         font=("Roboto", 16, "bold"), width=200, height=50, command=self._trigger_isolation)
        self.isolate_btn.pack(pady=10)

        self.restore_btn = ctk.CTkButton(self.button_frame, text="🟢 RESTORE CONNECTION", fg_color="#2ecc71", hover_color="#27ae60", 
                                         font=("Roboto", 16, "bold"), width=200, height=50, command=self._trigger_restore, state="disabled")
        self.restore_btn.pack(pady=10)

        self.log_frame = ctk.CTkFrame(self, width=460, height=200)
        self.log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        ctk.CTkLabel(self.log_frame, text="Activity Log", font=("Roboto", 14, "bold"), anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        
        self.log_text = ctk.CTkTextbox(self.log_frame, font=("Consolas", 12), state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(self, text="v1.0 MVP | Local Processing Only", font=("Roboto", 10), text_color="gray").pack(pady=10)

    def _log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _update_status(self, is_isolated):
        if is_isolated:
            self.status_label.configure(text="🛑 DEVICE ISOLATED", text_color="#e74c3c")
            self.isolate_btn.configure(state="disabled")
            self.restore_btn.configure(state="normal")
        else:
            self.status_label.configure(text="🟢 SYSTEM SECURE", text_color="#2ecc71")
            self.isolate_btn.configure(state="normal")
            self.restore_btn.configure(state="disabled")

    def _trigger_isolation(self):
        self._log("ACTION: User triggered KILL SWITCH.")
        self.isolate_btn.configure(state="disabled")
        
        def isolate_task():
            success = self.isolator.blow_bridge()
            self.after(0, self._complete_isolation, success)
            
        threading.Thread(target=isolate_task, daemon=True).start()

    def _complete_isolation(self, success):
        if success:
            self.isolator.is_isolated = True
            self._update_status(True)
            self._log("STATUS: 🛑 Network isolated. Device is in safe mode.")
            
            self._log("⏱️ SAFETY FAILSAFE: 30-second auto-restore timer started.")
            self.rollback_timer = threading.Timer(30.0, self._auto_restore)
            self.rollback_timer.start()
        else:
            self._log("ERROR: Failed to isolate network. Check Admin privileges.")
            self.isolate_btn.configure(state="normal")

    def _trigger_restore(self):
        if self.rollback_timer:
            self.rollback_timer.cancel()
            self._log("ACTION: User manually canceled auto-restore timer.")
        
        self._log("ACTION: User triggered RECOVERY.")
        self.restore_btn.configure(state="disabled")
        
        def restore_task():
            success = self.isolator.rebuild_bridge()
            self.after(0, self._complete_restore, success)
            
        threading.Thread(target=restore_task, daemon=True).start()

    def _complete_restore(self, success):
        if success:
            self.isolator.is_isolated = False
            self._update_status(False)
            self._log("STATUS: 🟢 Connection restored. System secure.")
        else:
            self._log("ERROR: Failed to restore network.")
            self.restore_btn.configure(state="normal")

    def _auto_restore(self):
        if self.isolator.is_isolated:
            self.after(0, self._log, "⚠️ AUTO-RESTORE TRIGGERED: 30 seconds elapsed. Restoring network.")
            self._trigger_restore()

    def on_closing(self):
        if self.isolator.is_isolated:
            self._log("Cleanup: Restoring network before exit...")
            self.isolator.rebuild_bridge()
        self.destroy()

if __name__ == "__main__":
    app = NUBSDashboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()