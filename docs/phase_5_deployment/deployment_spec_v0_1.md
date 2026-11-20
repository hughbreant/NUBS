# Deployment Specification v0.1 - NUBS

## 1. Overview
This document outlines the deployment strategy for the NUBS application, ensuring a consistent, isolated, and reproducible setup for end-users on Windows environments (with cross-platform compatibility via standard Python tools).

## 2. Prerequisites
- **Operating System**: Windows 10/11 (macOS/Linux compatible with minor script adjustments)
- **Python**: Version 3.8 or higher installed and added to the system `PATH`.
- **Permissions**: Ability to execute PowerShell scripts (may require `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`).

## 3. Automated Deployment Workflow

The project includes a unified deployment script (`scripts/run_nubs_v0_1.ps1`) that handles the entire setup process:

1. **Validation**: Checks for a valid Python installation.
2. **Isolation**: Creates a Python virtual environment (`.venv`) to prevent dependency conflicts with the host system.
3. **Activation**: Activates the virtual environment for the current session.
4. **Installation**: Installs or updates dependencies listed in `requirements.txt`.
5. **Execution**: Launches the Streamlit dashboard on `http://localhost:8501`.

## 4. Manual Execution (Alternative)
For advanced users or non-Windows environments, the application can be run manually:
```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run src/ui/dashboard_app_v0_1.py