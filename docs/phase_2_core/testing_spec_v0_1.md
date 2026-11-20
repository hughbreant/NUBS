# Testing Specification v0.1 - NUBS Core Logic

## 1. Overview
This document outlines the unit testing strategy for the NUBS core logic (`KillSwitchEngine` and `BridgeManager`). Tests are designed to validate state transitions, trigger evaluations, process management, and critical security guarantees.

## 2. Test Coverage

### `TestBridgeManager` (4 Tests)
1. **`test_process_registration`**: Verifies that processes are correctly added to the managed registry with default running/network states.
2. **`test_isolation_sequence`**: Confirms that `execute_isolation()` revokes network access and suspends all managed processes.
3. **`test_termination_sequence`**: Confirms that `execute_termination()` kills all processes and sets the `memory_wiped` flag to `True`.
4. **`test_recovery_sequence`**: Validates that `execute_recovery()` correctly restores network access and resumes suspended processes.

### `TestKillSwitchEngine` (5 Tests)
1. **`test_initial_state`**: Ensures the engine initializes in the `ACTIVE` state.
2. **`test_cpu_trigger_isolation`**: Validates that CPU usage > 90% triggers a transition to `ISOLATED` and invokes the bridge isolation sequence.
3. **`test_unauthorized_access_termination`**: Validates that an unauthorized access flag immediately triggers `TERMINATED` and invokes the bridge termination sequence.
4. **`test_termination_security_lock`**: **Critical Security Test**. Confirms that once in `TERMINATED`, any attempt to transition to `ACTIVE` or `ISOLATED` is rejected (returns `False`) and the state remains `TERMINATED`.
5. **`test_manual_recovery_from_isolation`**: Validates the happy path of recovering from an `ISOLATED` state back to `ACTIVE` via admin override.

## 3. Execution
Tests are executed via the standard Python `unittest` framework:
```bash
python tests/test_core_v0_1.py