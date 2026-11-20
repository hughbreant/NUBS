## NUBS: Normal Users Bridge-Switch
\*\*AI Personal Kill Switch – Monitor, Bridge, and Safely Terminate AI Processes\*\*
\[!\[Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview
NUBS (Normal Users Bridge-Switch) is a lightweight, Python-based system designed to give normal users absolute control over AI processes. It provides a "bridge" to safely interact with AI systems while maintaining a "kill switch" that can instantly isolate or terminate processes in response to resource spikes, security breaches, or manual overrides.

## Key Features
\- \*\*Three-State Safety Model\*\*: ACTIVE (🟢), ISOLATED (🟡), TERMINATED (🔴)
\- \*\*Automatic Triggers\*\*: CPU monitoring and unauthorized access detection
\- \*\*Manual Overrides\*\*: Admin dashboard for real-time control
\- \*\*One-Way Termination\*\*: Once killed, the system requires a full restart (security guarantee)
\- \*\*Lightweight\*\*: No heavy dependencies, runs on standard Python

## Architecture
┌───────────────────────────────────────────────────┐
│ NUBS Dashboard (UI) │
│ src/ui/dashboard\_app\_v0\_1.py │
└────────────────────┬──────────────────────────────┘
│
▼
┌───────────────────────────────────────────────────┐
│ Kill Switch Engine (State Machine) │
│ src/core/kill\_switch\_engine\_v0\_2.py │
│ - Manages state transitions (ACTIVE ↔ ISOLATED ↔ TERMINATED)│
│ - Evaluates triggers (CPU, unauthorized access) │
│ - Enforces security locks │
└────────────────────┬──────────────────────────────┘
│
▼
┌───────────────────────────────────────────────────┐
│ Bridge Manager (Execution Layer) │
│ src/core/bridge\_manager\_v0\_1.py │
│ - Manages process registry │
│ - Executes isolation (suspend, revoke network) │
│ - Executes termination (kill, wipe memory) │
└───────────────────────────────────────────────────┘
\---

## Project Structure
NUBS/
├── src/
│ ├── core/
│ │ ├── kill\_switch\_engine\_v0\_2.py # State machine \& trigger logic
│ │ └── bridge\_manager\_v0\_1.py # Process execution layer
│ └── ui/
│ └── dashboard\_app\_v0\_1.py # Streamlit dashboard
├── tests/
│ ├── test\_core\_v0\_1.py # Unit tests (9 tests)
│ └── test\_e2e\_v0\_1.py # End-to-end workflow test
├── docs/
│ ├── phase\_2\_core/ # Core logic documentation
│ ├── phase\_3\_ui/ # UI documentation
│ └── phase\_4\_testing/ # Testing \& security docs
├── scripts/ # Deployment scripts (Phase 5)
├── HANDOFF\_v0\_8.md # Project handoff tracker
└── README.md # This file
\---

## Quick Start

## Prerequisites
\- Python 3.8 or higher
\- pip (Python package manager)

## Installation
1\. \*\*Clone the repository\*\*:
&#x20;  ```bash
&#x20;  git clone https://github.com/hughbreant/NUBS.git
&#x20;  cd NUBS
2\. Install dependencies:
&#x20;  pip install streamlit
Running the Dashboard
Launch the NUBS dashboard:
streamlit run src/ui/dashboard\_app\_v0\_1.py
The dashboard will open in your browser at http://localhost:8501

## Usage Guide
Understanding the States
State      | Indicator |  Description                                               | User Action
ACTIVE     |    🟢    |   Normal operation. Bridge is open, all processes running. | Monitor system
ISOLATED   |    🟡    |   Sandboxed. Network revoked, processes suspended.         | Review logs, perform admin recovery
TERMINATED |    🔴    |   Hard kill. Processes terminated, memory wiped.           | Restart application

## Dashboard Controls
The dashboard provides three manual control buttons:
*Simulate CPU Spike (>90%): Triggers automatic isolation (useful for testing).
*Simulate Security Breach: Triggers immediate termination (useful for testing).
*Manual Admin Recovery: Restores the system from ISOLATED to ACTIVE (only available when isolated).
Note: All controls are disabled when the system is TERMINATED.

## Testing
Run Unit Tests
python tests/test_core_v0_1.py
Expected output: 9 tests passing
Run End-to-End Test
python tests/test_e2e_v0_1.py
Expected output: 1 comprehensive workflow test passing

## Security Considerations
Current Security Guarantees
*One-Way Termination: Once TERMINATED, the system cannot be recovered without a full restart.
*rocess Isolation: All managed processes are immediately suspended or killed on state transition.
*Trigger Safety: No triggers can affect a terminated system.

## Future Security Enhancements
*Add user authentication to the dashboard
*Implement persistent audit logging
*Add post-termination registration locks
*Implement rate limiting on trigger evaluations
For detailed security analysis, see docs/phase\_4\_testing/security\_review\_v0\_1.md.

## Documentation
Core Logic: docs/phase\_2\_core/core\_logic\_spec\_v0\_1.md
Bridge Manager: docs/phase\_2\_core/bridge\_manager\_spec\_v0\_1.md
Dashboard UI: docs/phase\_3\_ui/dashboard\_spec\_v0\_1.md
Testing: docs/phase\_4\_testing/e2e\_testing\_spec\_v0\_1.md
Security: docs/phase\_4\_testing/security\_review\_v0\_1.md

## Contributing
This project follows a strict session-based workflow. See HANDOFF\_v0\_8.md for the current project status and next steps.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Built for normal users who want control over their AI systems.
Current Version: v0.8 (Phase 4 Complete)
Last Updated: November 20, 2026















