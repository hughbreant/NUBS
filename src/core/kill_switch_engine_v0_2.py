import logging
from enum import Enum
from bridge_manager_v0_1 import BridgeManager

class NubsState(Enum):
    ACTIVE = "🟢 BRIDGE ACTIVE"
    ISOLATED = "🟡 BRIDGE ISOLATED"
    TERMINATED = "🔴 KILL SWITCH ENGAGED"

class KillSwitchEngine:
    def __init__(self, bridge_manager: BridgeManager = None):
        self.current_state = NubsState.ACTIVE
        self.resource_threshold_cpu = 90.0
        self.is_running = True
        self.bridge_manager = bridge_manager or BridgeManager()

    def get_state(self):
        return self.current_state

    def transition_to(self, new_state: NubsState, reason: str) -> bool:
        if self.current_state == NubsState.TERMINATED and new_state != NubsState.TERMINATED:
            logging.warning("SECURITY: Cannot transition out of TERMINATED state without manual system reset.")
            return False
        
        logging.info(f"STATE TRANSITION: {self.current_state.value} -> {new_state.value} | Reason: {reason}")
        self.current_state = new_state
        
        if new_state == NubsState.TERMINATED:
            self.bridge_manager.execute_termination()
        elif new_state == NubsState.ISOLATED:
            self.bridge_manager.execute_isolation()
        elif new_state == NubsState.ACTIVE:
            self.bridge_manager.execute_recovery()
            
        return True

    def evaluate_triggers(self, cpu_usage: float, unauthorized_access: bool):
        if self.current_state == NubsState.TERMINATED:
            return

        if unauthorized_access:
            self.transition_to(NubsState.TERMINATED, "Unauthorized access detected")
        elif cpu_usage > self.resource_threshold_cpu:
            self.transition_to(NubsState.ISOLATED, f"Resource threshold exceeded (CPU: {cpu_usage}%)")