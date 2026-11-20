# Dashboard UI Implementation v0.1

## 1. Technology Choice: CustomTkinter
For the MVP, we selected `customtkinter` (a modern UI library for Python) because:
- **Zero Web Stack Complexity:** No need for Node.js, Webpack, or Electron for the initial proof-of-concept.
- **Native OS Integration:** Runs as a native desktop application.
- **Modern Aesthetics:** Built-in dark mode, rounded corners, and high-contrast colors perfect for a security tool.

## 2. UI Layout & User Experience (UX) Principles
- **Jargon-Free:** Buttons say "ISOLATE DEVICE" and "RESTORE CONNECTION", not "Toggle iptables" or "Flush DNS".
- **High Contrast Status:** A large, color-coded indicator (🟢 SECURE / 🛑 ISOLATED) is always visible.
- **Live Activity Log:** A scrollable text area shows exactly what the system is doing in real-time, building user trust.
- **Safety First:** The "Restore" button becomes prominently available after isolation, and the system auto-restores after 30 seconds (inherited from Phase 3 backend logic).

## 3. MVP Scope
This UI script contains a self-contained version of the NUBS isolation logic for easy testing. In Phase 5, this will be refactored to cleanly import the `network_isolator_v0.1.py` module.