# Network Isolation Logic & Safety Failsafe v0.1

## 1. Isolation Mechanism (Windows MVP)
Instead of disabling network adapters (which risks permanent lockout), NUBS utilizes the Windows Advanced Firewall (`netsh advfirewall`) to inject a high-priority, temporary blocking rule.

- **Rule Name:** `NUBS_Emergency_Block_All`
- **Action:** Block
- **Direction:** Outbound (prevents data exfiltration and C2 communication)
- **Profile:** Any (Public, Private, Domain)

## 2. The Safety Failsafe (Auto-Rollback)
To adhere to the "Do No Harm" principle for non-technical users, the isolation mechanism includes a mandatory auto-rollback:
1. When the Kill Switch is triggered, a background daemon thread starts a 30-second countdown.
2. If the user does not manually trigger "Rebuild Bridge" within 30 seconds, the script automatically executes the removal of the firewall rule.
3. This guarantees that even in the event of a Python crash or system freeze, the user's internet access will restore itself shortly after.

## 3. Privilege Requirements
Modifying Windows Firewall rules requires **Administrator Privileges**. 
- The MVP script will check for admin rights on startup.
- If not running as admin, it will gracefully degrade to "Simulation Mode" (logging what it *would* do without executing it).

## 4. Future Enhancements (Post-MVP)
- Cross-platform support (Linux `iptables` / macOS `pf`).
- Process-level suspension (using `psutil` to pause suspicious PIDs, not just network blocking).