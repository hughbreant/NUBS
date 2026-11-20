# Integration & Testing Protocol v0.1

## 1. System Integration
The NUBS MVP is now fully integrated. The architecture separates concerns cleanly:
- `src/core/network_isolator_v0.1.py`: Handles OS-level firewall rules and the 30-second safety failsafe.
- `src/main_v0.1.py`: The unified entry point that initializes the `NUBSIsolator` and passes it to the `NUBSDashboard` UI.

## 2. Safe Testing Protocol (Do No Harm)
To verify the application works without risking your primary machine's internet connection, follow this protocol:

### Level 1: Simulation Mode (Default)
1. Open standard PowerShell (Not as Administrator).
2. Run: `python src/main_v0.1.py`
3. Click "ISOLATE DEVICE". 
4. **Expected Result:** The UI turns red, logs state "SIMULATION MODE", and the 30-second timer runs. No actual firewall rules are changed.

### Level 2: Live Isolation Test (Requires Admin)
1. Open PowerShell **as Administrator**.
2. Run: `python src/main_v0.1.py`
3. Click "ISOLATE DEVICE".
4. **Expected Result:** UI turns red. Open a browser and try to load a webpage (e.g., google.com). It should fail to load.
5. Click "RESTORE CONNECTION" (or wait 30 seconds).
6. **Expected Result:** UI turns green. Browser immediately regains internet access.

## 3. Future Roadmap (Post-MVP)
- **AI Heuristics:** Integrate a lightweight local ML model (e.g., ONNX runtime) to monitor file I/O and auto-trigger the kill switch.
- **Physical Button:** Map the `blow_bridge()` function to a USB macro pad (e.g., Stream Deck or Raspberry Pi Pico) for a true "Panic Button" experience.
- **Packaging:** Use `PyInstaller` to compile the Python script into a standalone `.exe` file for easy distribution to non-technical users.