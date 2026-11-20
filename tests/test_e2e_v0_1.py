import sys
import os
import unittest

# Add src/core to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.abspath(os.path.join(current_dir, '..', 'src', 'core'))
sys.path.insert(0, core_dir)

from kill_switch_engine_v0_2 import KillSwitchEngine, NubsState
from bridge_manager_v0_1 import BridgeManager

class TestE2EWorkflow(unittest.TestCase):
    def setUp(self):
        """Initialize a fresh NUBS environment for each E2E test."""
        self.bridge = BridgeManager()
        self.bridge.register_process(5001, "e2e_main_ai_agent")
        self.bridge.register_process(5002, "e2e_data_pipeline")
        self.engine = KillSwitchEngine(bridge_manager=self.bridge)

    def test_full_lifecycle_workflow(self):
        """Simulate a complete user workflow: Active -> Isolated -> Active -> Terminated -> Locked."""
        
        # 1. Initial State: System starts ACTIVE
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)
        self.assertTrue(self.bridge.network_bridge_active)
        self.assertTrue(self.bridge.managed_processes[0].is_running)

        # 2. Trigger Isolation: Simulate a resource spike
        self.engine.evaluate_triggers(cpu_usage=95.0, unauthorized_access=False)
        self.assertEqual(self.engine.get_state(), NubsState.ISOLATED)
        self.assertFalse(self.bridge.network_bridge_active, "Network should be revoked in ISOLATED state")
        self.assertFalse(self.bridge.managed_processes[0].is_running, "Processes should be suspended in ISOLATED state")

        # 3. Manual Recovery: Admin reviews and clears the system
        recovery_success = self.engine.transition_to(NubsState.ACTIVE, "Admin cleared resource spike")
        self.assertTrue(recovery_success)
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)
        self.assertTrue(self.bridge.network_bridge_active, "Network should be restored after recovery")
        self.assertTrue(self.bridge.managed_processes[0].is_running, "Processes should resume after recovery")

        # 4. Trigger Termination: Simulate a critical security breach
        self.engine.evaluate_triggers(cpu_usage=20.0, unauthorized_access=True)
        self.assertEqual(self.engine.get_state(), NubsState.TERMINATED)
        self.assertFalse(self.bridge.managed_processes[0].is_running, "Processes must be killed in TERMINATED state")
        self.assertTrue(self.bridge.memory_wiped, "Memory must be wiped in TERMINATED state")

        # 5. Security Lock Verification: Attempt malicious recovery
        malicious_recovery = self.engine.transition_to(NubsState.ACTIVE, "Hacker attempting restart")
        self.assertFalse(malicious_recovery, "Recovery from TERMINATED must be rejected")
        self.assertEqual(self.engine.get_state(), NubsState.TERMINATED, "State must remain TERMINATED")
        
        # Verify bridge remains locked
        self.assertTrue(self.bridge.memory_wiped, "Memory wipe state must persist")

if __name__ == '__main__':
    # Suppress logging output during tests for clean CI/CD results
    import logging
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)