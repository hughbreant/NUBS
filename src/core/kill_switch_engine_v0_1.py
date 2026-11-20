import logging
from enum import Enum

# Configure logging for the engine
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NubsState(Enum):
    ACTIVE = "🟢 BRIDGE ACTIVE"
    ISOLATED = "🟡 BRIDGE ISOLATED"
    TERMINATED = "🔴 KILL SWITCH ENGAGED"

class KillSwitchEngine:
    def __init__(self):
        self.current_state = NubsState.ACTIVE
        self.resource_threshold_cpu = 90.0
        self.is_running = True

    def get_state(self):
        return self.current_state

    def transition_to(self, new_state: NubsState, reason: str) -> bool:
        # Security Lock: Prevent transition out of TERMINATED without hard reset
        if self.current_state == NubsState.TERMINATED and new_state != NubsState.TERMINATED:
            logging.warning("SECURITY: Cannot transition out of TERMINATED state without manual system reset.")
            return False
        
        logging.info(f"STATE TRANSITION: {self.current_state.value} -> {new_state.value} | Reason: {reason}")
        self.current_state = new_state
        
        if new_state == NubsState.TERMINATED:
            self._execute_termination_sequence()
        elif new_state == NubsState.ISOLATED:
            self._execute_isolation_sequence()
            
        return True

    def _execute_isolation_sequence(self):
        logging.info("ACTION: Revoking network access, suspending non-essential threads, sandboxing environment.")

    def _execute_termination_sequence(self):
        logging.info("ACTION: Force killing AI processes, wiping volatile temp memory, locking system bridge.")
        self.is_running = False

    def evaluate_triggers(self, cpu_usage: float, unauthorized_access: bool):
        if self.current_state == NubsState.TERMINATED:
            return

        if unauthorized_access:
            self.transition_to(NubsState.TERMINATED, "Unauthorized access detected")
        elif cpu_usage > self.resource_threshold_cpu:
            self.transition_to(NubsState.ISOLATED, f"Resource threshold exceeded (CPU: {cpu_usage}%)")