import sys
import os
import unittest

# Add src/core to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.abspath(os.path.join(current_dir, '..', 'src', 'core'))
sys.path.insert(0, core_dir)

from kill_switch_engine_v0_2 import KillSwitchEngine, NubsState
from bridge_manager_v0_1 import BridgeManager

class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        """Initialize a fresh NUBS environment for each edge case test."""
        self.bridge = BridgeManager()
        self.engine = KillSwitchEngine(bridge_manager=self.bridge)

    def test_boundary_cpu_threshold(self):
        """CPU at exactly 90.0% should NOT trigger isolation. 90.1% should."""
        # Test exact boundary (should remain ACTIVE)
        self.engine.evaluate_triggers(cpu_usage=90.0, unauthorized_access=False)
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)
        
        # Test just over boundary (should trigger ISOLATED)
        self.engine.evaluate_triggers(cpu_usage=90.1, unauthorized_access=False)
        self.assertEqual(self.engine.get_state(), NubsState.ISOLATED)

    def test_empty_registry_termination(self):
        """System should handle termination gracefully even with 0 registered processes."""
        # Do not register any processes
        self.assertEqual(len(self.bridge.managed_processes), 0)
        
        # Trigger termination
        self.engine.evaluate_triggers(cpu_usage=10.0, unauthorized_access=True)
        
        # Verify state and memory wipe flag without crashing
        self.assertEqual(self.engine.get_state(), NubsState.TERMINATED)
        self.assertTrue(self.bridge.memory_wiped)

    def test_rapid_fire_conflicting_triggers(self):
        """If CPU spike and unauthorized access happen simultaneously, security breach (termination) must win."""
        self.bridge.register_process(9999, "critical_ai_agent")
        
        # Simulate simultaneous trigger evaluation
        self.engine.evaluate_triggers(cpu_usage=99.9, unauthorized_access=True)
        
        # Must be TERMINATED, not just ISOLATED
        self.assertEqual(self.engine.get_state(), NubsState.TERMINATED)
        self.assertFalse(self.bridge.managed_processes[0].is_running)
        self.assertTrue(self.bridge.memory_wiped)

    def test_multiple_recoveries_attempt(self):
        """Attempting to recover multiple times from ISOLATED state should be idempotent and safe."""
        self.bridge.register_process(8888, "recovery_test_process")
        
        # Isolate
        self.engine.evaluate_triggers(cpu_usage=95.0, unauthorized_access=False)
        self.assertEqual(self.engine.get_state(), NubsState.ISOLATED)
        
        # Recover once
        self.engine.transition_to(NubsState.ACTIVE, "Admin recovery 1")
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)
        
        # Attempt to "recover" again while already ACTIVE (should just stay ACTIVE or log, but not break)
        # Note: Current logic allows ACTIVE -> ACTIVE transition if called, let's verify it doesn't crash
        result = self.engine.transition_to(NubsState.ACTIVE, "Redundant admin recovery")
        self.assertTrue(result)
        self.assertEqual(self.engine.get_state(), NubsState.ACTIVE)

if __name__ == '__main__':
    import logging
    logging.disable(logging.CRITICAL)
    unittest.main(verbosity=2)