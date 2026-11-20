import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kill_switch_engine_v0_1 import KillSwitchEngine, NubsState

def main():
    print("="*60)
    print("Initializing NUBS (Normal Users Bridge-Switch) Simulator v0.2")
    print("="*60)
    
    engine = KillSwitchEngine()
    print(f"\n[INIT] Initial State: {engine.get_state().value}")
    
    # Scenario 1: Normal operation
    print("\n--- Scenario 1: Normal Operation ---")
    engine.evaluate_triggers(cpu_usage=45.0, unauthorized_access=False)
    print(f"[STATUS] Current State: {engine.get_state().value}")
    
    # Scenario 2: Resource spike
    print("\n--- Scenario 2: Resource Spike Detected ---")
    engine.evaluate_triggers(cpu_usage=95.0, unauthorized_access=False)
    print(f"[STATUS] Current State: {engine.get_state().value}")
    
    # Scenario 3: Manual recovery
    print("\n--- Scenario 3: Manual Admin Recovery ---")
    engine.transition_to(NubsState.ACTIVE, "Manual admin override after resource check")
    print(f"[STATUS] Current State: {engine.get_state().value}")
    
    # Scenario 4: Security breach
    print("\n--- Scenario 4: Critical Security Breach ---")
    engine.evaluate_triggers(cpu_usage=30.0, unauthorized_access=True)
    print(f"[STATUS] Current State: {engine.get_state().value}")
    
    # Scenario 5: Attempt to recover from TERMINATED (should fail)
    print("\n--- Scenario 5: Attempting Unauthorized Recovery ---")
    engine.transition_to(NubsState.ACTIVE, "Malicious recovery attempt")
    print(f"[STATUS] Current State: {engine.get_state().value}")
    
    print("\n" + "="*60)
    print("NUBS Simulator v0.2 execution completed successfully.")
    print("="*60)

if __name__ == "__main__":
    main()