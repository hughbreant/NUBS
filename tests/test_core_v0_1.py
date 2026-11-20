import sys
import os
import unittest

# Add src/core to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.abspath(os.path.join(current_dir, '..', 'src', 'core'))
sys.path.insert(0, core_dir)

from kill_switch_engine_v0_2 import KillSwitchEngine, NubsState
from bridge_manager_v0_1 import BridgeManager, ManagedProcess

class TestBridgeManager(unittest.TestCase):
    def setUp(self):
        self.bridge = BridgeManager()
        self.bridge.register_process(1001, "test_ai_process")

    def test_process_registration(self):
        self.assertEqual(len(self.bridge.managed_processes), 1)
        self.assertEqual(self.bridge.managed_processes[0].name, "test_ai_process")
        self.assertTrue(self.bridge.network_bridge_active)

    def test_isolation_sequence(self):
        self.bridge.execute_isolation()
        self.assertFalse(self.bridge.network_bridge_active)
        self.assertFalse(self.bridge.managed_processes[0].is_running)

    def test_termination_sequence(self):
        self.bridge.execute_termination()
        self.assertFalse(self.bridge.managed_processes[0].is_running)
        self.assertTrue(self.bridge.memory_wiped)

    def test_recovery_sequence(self):
        self.bridge.execute_isolation()
        self.bridge.execute_recovery()
        self.assertTrue(self.bridge.network_bridge_active)
        self.assertTrue(self.bridge.managed_processes[0].is_running)
        self.assertFalse(self.bridge.memory_wiped)


class TestKillSwitchEngine(unittest.TestCase):
    def setUp(self):
        self.bridge = BridgeManager()
        self.bridge.register_process(2001, "engine_test_process")
        self.engine = KillSwitchEngine(bridge_manager=self.bridge)

    def test_initial_state(self):
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)
        self.assertTrue(self.engine.is_running)

    def test_cpu_trigger_isolation(self):
        self.engine.evaluate_triggers(cpu_usage=95.0, unauthorized_access=False)
        self.assertEqual(self.engine.get_state(), NubsState.ISOLATED)
        self.assertFalse(self.bridge.network_bridge_active)

    def test_unauthorized_access_termination(self):
        self.engine.evaluate_triggers(cpu_usage=30.0, unauthorized_access=True)
        self.assertEqual(self.engine.get_state(), NubsState.TERMINATED)
        self.assertTrue(self.bridge.memory_wiped)

    def test_termination_security_lock(self):
        # Force to terminated
        self.engine.transition_to(NubsState.TERMINATED, "Test termination")
        # Attempt recovery
        result = self.engine.transition_to(NubsState.ACTIVE, "Malicious recovery")
        self.assertFalse(result)
        self.assertEqual(self.engine.get_state(), NubsState.TERMINATED)

    def test_manual_recovery_from_isolation(self):
        self.engine.evaluate_triggers(cpu_usage=95.0, unauthorized_access=False)
        self.assertEqual(self.engine.get_state(), NubsState.ISOLATED)
        
        result = self.engine.transition_to(NubsState.ACTIVE, "Admin override")
        self.assertTrue(result)
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)
        self.assertTrue(self.bridge.network_bridge_active)


if __name__ == '__main__':
    # Suppress logging output during tests for cleaner results
    import logging
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)