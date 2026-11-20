# HANDOFF.md (v0.3) - NUBS (Normal Users Bridge-Switch) Project

## Project Overview
- **Name**: Normal Users Bridge-Switch (NUBS)
- **Purpose**: AI Personal Kill Switch – A system to monitor, bridge, and safely terminate or isolate AI processes for normal users.
- **Repository**: https://github.com/hughbreant/NUBS.git
- **Current Status**: Phase 1 Completed. Core structure, v0.1 simulator, and initial documentation established.

## Project Phases Checklist

### ✅ Phase 1: Setup & Discovery (COMPLETED)
- [x] Project directory structure created (`docs/`, `src/core`, `src/ui`, `tests`, `scripts`)
- [x] Git repository initialized and pushed to GitHub (PowerShell compatible)
- [x] `nubs_simulator_v0.1.py` created and tested (Status: 🟢 BRIDGE ACTIVE)
- [x] Initial UI mockup documented (`docs/phase_1_setup_and_discovery/dashboard_ui_mockup_v0.2.md`)
- [x] Initial `HANDOFF.md` created and versioned

### 🔄 Phase 2: Core Logic & Kill Switch Implementation (NEXT)
- [ ] Define kill switch triggers and conditions (e.g., resource limits, unauthorized access, manual override)
- [ ] Implement `kill_switch_engine_v0.1.py` in `src/core/`
- [ ] Implement `bridge_manager_v0.1.py` to handle safe state transitions (Active ↔ Isolated ↔ Terminated)
- [ ] Write unit tests for core logic in `tests/test_core_v0.1.py`
- [ ] Document architecture in `docs/phase_2_core/core_logic_spec_v0.1.md`
- [ ] Update `HANDOFF.md` to v0.4 upon completion

### 📋 Phase 3: Functional UI Dashboard
- [ ] Select UI framework (Recommendation: Streamlit or Gradio for rapid Python UI)
- [ ] Implement `dashboard_app_v0.1.py` in `src/ui/`
- [ ] Connect UI to `nubs_simulator` and core kill switch logic
- [ ] Document UI components in `docs/phase_3_ui/dashboard_spec_v0.1.md`
- [ ] Update `HANDOFF.md` to v0.5 upon completion

### 🛡️ Phase 4: Testing, Security & Documentation Finalization
- [ ] End-to-end testing script: `tests/test_e2e_v0.1.py`
- [ ] Security review of kill switch execution (ensure it only targets intended NUBS processes)
- [ ] Finalize root `README.md` with setup, usage, and architecture diagrams
- [ ] Update `HANDOFF.md` to v0.6 upon completion

### 🚀 Phase 5: Deployment & Handoff
- [ ] Package application dependencies (`requirements.txt`)
- [ ] Create deployment/execution script: `scripts/run_nubs_v0.1.ps1`
- [ ] Final project review, git push, and sign-off
- [ ] Update `HANDOFF.md` to v1.0 (FINAL)

## Documentation & Naming Conventions
- **Code Files**: Always include filename, extension, and version (e.g., `kill_switch_engine_v0.1.py`).
- **Documentation**: Structured by phase/module (e.g., `docs/phase_2_core/core_logic_spec_v0.1.md`).
- **Session Workflow**: Complete one phase/module, document it, update `HANDOFF.md`, then proceed to the next session.

## Next Action
**Phase 2, Step 1**: Define kill switch triggers and draft `kill_switch_engine_v0.1.py`.