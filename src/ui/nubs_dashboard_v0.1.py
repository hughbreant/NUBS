"""
File: nubs_dashboard_v0.1.py
Phase: 4 - MVP Frontend (Dashboard UI Implementation)
Project: Normal Users Bridge-Switch (NUBS)
Description: A modern, dark-mode desktop dashboard for NUBS, featuring 
             real-time status updates, a kill switch, and an activity log.
"""

import customtkinter as ctk
import time
import threading
import ctypes

# Set appearance mode and default theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NUBSDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("NUBS - Normal Users Bridge-Switch v0.1")
        self.geometry("500x600")
        self.resizable(False, False)

        # State variables
        self.is_isolated = False
        self.is_admin = self._check_admin()
        self.rollback_timer = None

        # Build UI
        self._build_ui()
        self._log("System initialized. Ready.")
        if not self.is_admin:
            self._log("⚠️ Running in SIMULATION MODE (Not Admin).")

    def _check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def _build_ui(self):
        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=20)

        self.title_label = ctk.CTkLabel(self.header_frame, text="NUBS", font=("Roboto", 28, "bold"))
        self.title_label.pack()

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Normal Users Bridge-Switch", font=("Roboto", 14), text_color="gray")
        self.subtitle_label.pack()

        # --- Status Indicator ---
        self.status_label = ctk.CTkLabel(self, text="🟢 SYSTEM SECURE", font=("Roboto", 20, "bold"), text_color="#2ecc71")
        self.status_label.pack(pady=10)

        # --- Action Buttons ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.isolate_btn = ctk.CTkButton(self.button_frame, text="🛑 ISOLATE DEVICE", fg_color="#e74c3c", hover_color="#c0392b", 
                                         font=("Roboto", 16, "bold"), width=200, height=50, command=self._trigger_isolation)
        self.isolate_btn.pack(pady=10)

        self.restore_btn = ctk.CTkButton(self.button_frame, text="🟢 RESTORE CONNECTION", fg_color="#2ecc71", hover_color="#27ae60", 
                                         font=("Roboto", 16, "bold"), width=200, height=50, command=self._trigger_restore, state="disabled")
        self.restore_btn.pack(pady=10)

        # --- Activity Log ---
        self.log_frame = ctk.CTkFrame(self, width=460, height=200)
        self.log_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.log_label = ctk.CTkLabel(self.log_frame, text="Activity Log", font=("Roboto", 14, "bold"), anchor="w")
        self.log_label.pack(fill="x", padx=10, pady=(10, 0))

        self.log_text = ctk.CTkTextbox(self.log_frame, font=("Consolas", 12), state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # --- Footer ---
        self.footer_label = ctk.CTkLabel(self, text="v0.1 MVP | Local Processing Only", font=("Roboto", 10), text_color="gray")
        self.footer_label.pack(pady=10)

    def _log(self, message):
        """Appends a timestamped message to the UI log."""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.configure(state="normal")
        self.log_text.insert("end", log_entry)
        self.log_text.see("end") # Auto-scroll to bottom
        self.log_text.configure(state="disabled")

    def _update_status(self, is_isolated):
        """Updates the main status label and button states."""
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
        self._log("STATUS: Severing network traffic...")
        
        # Simulate work (In Phase 5, this calls the actual backend)
        self.after(500, self._complete_isolation)

    def _complete_isolation(self):
        self.is_isolated = True
        self._update_status(True)
        self._log("STATUS: 🛑 Network isolated. Device is in safe mode.")
        
        # Start 30-second auto-rollback failsafe
        self._log("⏱️ SAFETY FAILSAFE: 30-second auto-restore timer started.")
        self.rollback_timer = threading.Timer(30.0, self._auto_restore)
        self.rollback_timer.start()

    def _trigger_restore(self):
        if self.rollback_timer:
            self.rollback_timer.cancel()
            self._log("ACTION: User manually canceled auto-restore timer.")
        
        self._log("ACTION: User triggered RECOVERY.")
        self._log("STATUS: Verifying system integrity...")
        self.after(500, self._complete_restore)

    def _complete_restore(self):
        self.is_isolated = False
        self._update_status(False)
        self._log("STATUS: 🟢 Connection restored. System secure.")

    def _auto_restore(self):
        """Safety Failsafe: Called by timer if user doesn't manually restore."""
        if self.is_isolated:
            self._log("⚠️ AUTO-RESTORE TRIGGERED: 30 seconds elapsed. Restoring network.")
            self._complete_restore()

    def on_closing(self):
        """Ensure network is restored before the app closes."""
        if self.is_isolated:
            self._log("Cleanup: Restoring network before exit...")
            self._complete_restore()
        self.destroy()

if __name__ == "__main__":
    app = NUBSDashboard()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()