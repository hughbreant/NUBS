# Core Logic Specification v0.1 - NUBS Kill Switch Engine

## 1. Overview
The `KillSwitchEngine` is the central state machine responsible for monitoring AI process health and enforcing safety boundaries. It ensures that normal users can safely bridge to AI systems while retaining absolute control to isolate or terminate processes.

## 2. State Machine Definition
The engine operates on three mutually exclusive states (`NubsState` Enum):

| State | Indicator | Description | Allowed Transitions |
| :--- | :---: | :--- | :--- |
| **ACTIVE** | 🟢 | Normal operation. Monitoring is active, bridge is open, full permissions granted. | → ISOLATED, → TERMINATED |
| **ISOLATED** | 🟡 | Sandboxed mode. Network access revoked, non-essential threads suspended. Awaiting admin review. | → ACTIVE, → TERMINATED |
| **TERMINATED** | 🔴 | Hard kill. Processes forcefully stopped, volatile memory wiped, bridge locked. | → TERMINATED (Locked) |

## 3. Trigger Conditions
The `evaluate_triggers()` method continuously monitors for:
1. **Resource Threshold Exceeded**: CPU usage > 90% (configurable). Triggers transition to `ISOLATED`.
2. **Unauthorized Access**: Detected anomalous permission requests or external injection attempts. Triggers immediate transition to `TERMINATED`.

## 4. Security Guarantees
- **One-Way Termination**: Once the state is `TERMINATED`, the engine explicitly rejects any `transition_to()` calls except to `TERMINATED`. Recovery requires a full system/module restart (manual hard reset).
- **Audit Logging**: All state transitions and execution sequences are logged with timestamps and triggering reasons.

## 5. File Structure
- `src/core/kill_switch_engine_v0_1.py`: Core state machine and trigger logic.
- `src/core/nubs_simulator_v0_2.py`: Integration test and demonstration script.