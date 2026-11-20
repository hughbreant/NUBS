# End-to-End (E2E) Testing Specification v0.1 - NUBS

## 1. Overview
While unit tests (`test_core_v0_1.py`) validate individual components in isolation, the E2E test (`test_e2e_v0_1.py`) validates the **entire system lifecycle** as a cohesive unit. It simulates a realistic operational timeline from system startup to catastrophic failure and subsequent security lockdown.

## 2. Test Scenario: Full Lifecycle Workflow
The `test_full_lifecycle_workflow` test executes the following sequential assertions:

1. **Initialization**: Verifies the system boots into `ACTIVE` state with network enabled and processes running.
2. **Isolation Trigger**: Simulates a CPU spike (>90%). Asserts state transitions to `ISOLATED`, network is revoked, and processes are suspended.
3. **Admin Recovery**: Simulates an admin override. Asserts state returns to `ACTIVE`, network is restored, and processes resume.
4. **Termination Trigger**: Simulates an unauthorized access breach. Asserts state transitions to `TERMINATED`, processes are force-killed, and `memory_wiped` is set to `True`.
5. **Security Lock Verification**: Attempts a malicious transition back to `ACTIVE`. Asserts the transition is rejected (`False`), the state remains `TERMINATED`, and the memory wipe persists.

## 3. Execution
To run the E2E test suite:
```bash
python tests/test_e2e_v0_1.py