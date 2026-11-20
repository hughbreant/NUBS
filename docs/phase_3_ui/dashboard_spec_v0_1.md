# Dashboard Specification v0.1 - NUBS UI

## 1. Overview
The NUBS Dashboard provides a real-time, reactive visual interface for monitoring the state of the AI Kill Switch and executing manual administrative overrides. It is built using **Streamlit** for rapid, lightweight Python-based UI rendering.

## 2. Core Features

### System Status Panel
- Displays the current `NubsState` (ACTIVE, ISOLATED, TERMINATED) with color-coded indicators (Green, Orange, Red).
- Provides contextual messaging explaining the current system posture.

### Managed Processes Registry
- Lists all processes registered with the `BridgeManager` (PID, Name, Running Status).
- Displays global bridge metrics: Network Bridge status and Memory Wipe status.
- *Security Note:* Registry details are locked/masked if the system is in the `TERMINATED` state.

### Manual Controls
Provides three primary action buttons for testing and administration:
1. **Simulate CPU Spike**: Triggers the `evaluate_triggers` method with `cpu_usage=95.0`, forcing an `ISOLATED` state.
2. **Simulate Security Breach**: Triggers the `evaluate_triggers` method with `unauthorized_access=True`, forcing a `TERMINATED` state.
3. **Manual Admin Recovery**: Calls `transition_to(ACTIVE)` to restore the system from an `ISOLATED` state.
*Note: All buttons are automatically disabled if the system is already `TERMINATED` to prevent UI-level exploitation.*

## 3. State Persistence
Streamlit reruns the script on every user interaction. To maintain the state of the `KillSwitchEngine` and `BridgeManager` across clicks, the application utilizes `st.session_state`. The engine is initialized only once per session.

## 4. Execution
To run the dashboard locally:
```bash
pip install streamlit
streamlit run src/ui/dashboard_app_v0_1.py