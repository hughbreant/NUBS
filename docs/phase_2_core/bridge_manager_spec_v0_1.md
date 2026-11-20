# Bridge Manager Specification v0.1 - NUBS Process Execution Layer

## 1. Overview
The `BridgeManager` acts as the execution layer for the NUBS Kill Switch Engine. While the `KillSwitchEngine` handles the state machine logic and trigger evaluation, the `BridgeManager` is responsible for simulating (and eventually executing) the actual OS-level or process-level actions required to isolate or terminate AI processes.

## 2. Core Components

### `ManagedProcess` Class
Represents a single AI process being monitored and controlled by NUBS.
- **Attributes**:
  - `pid` (int): Process ID.
  - `name` (str): Process name/identifier.
  - `is_running` (bool): Current execution state (True = Running, False = Suspended/Killed).
  - `has_network` (bool): Network access status.

### `BridgeManager` Class
Manages a registry of `ManagedProcess` instances and executes state-mandated actions.
- **Methods**:
  - `register_process(pid, name)`: Adds a new process to the managed registry.
  - `execute_isolation()`: Revokes network access and suspends all managed processes.
  - `execute_termination()`: Force kills all managed processes, wipes volatile memory, and locks the bridge.
  - `execute_recovery()`: Restores network access and resumes suspended processes (used when transitioning from ISOLATED back to ACTIVE).

## 3. Integration with Kill Switch Engine
The `KillSwitchEngine` now accepts a `BridgeManager` instance via dependency injection in its constructor. 
- When the engine transitions to `ISOLATED`, it calls `bridge_manager.execute_isolation()`.
- When the engine transitions to `TERMINATED`, it calls `bridge_manager.execute_termination()`.
- When the engine transitions to `ACTIVE` (recovery), it calls `bridge_manager.execute_recovery()`.

## 4. File Structure
- `src/core/bridge_manager_v0_1.py`: Process registry and execution logic.
- `src/core/kill_switch_engine_v0_2.py`: Updated engine to utilize the BridgeManager.
- `src/core/nubs_simulator_v0_3.py`: Updated simulator demonstrating process registration and execution.