import sys
import os
import streamlit as st

# Add src/core to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.abspath(os.path.join(current_dir, '..', 'core'))
sys.path.insert(0, core_dir)

from kill_switch_engine_v0_2 import KillSwitchEngine, NubsState
from bridge_manager_v0_1 import BridgeManager

# Page Configuration
st.set_page_config(page_title="NUBS Dashboard", page_icon="🛡️", layout="centered")

st.title("🛡️ NUBS: Normal Users Bridge-Switch")
st.markdown("AI Personal Kill Switch – Monitor, Isolate, or Terminate AI Processes.")
st.markdown("---")

# Initialize Session State for Persistence
if "engine" not in st.session_state:
    bridge = BridgeManager()
    # Register some default simulated processes
    bridge.register_process(1001, "llama_inference_node_1")
    bridge.register_process(1002, "rag_retrieval_agent")
    bridge.register_process(1003, "vector_db_connector")
    
    st.session_state.engine = KillSwitchEngine(bridge_manager=bridge)

engine = st.session_state.engine
bridge = engine.bridge_manager
current_state = engine.get_state()

# --- State Display ---
st.header("System Status")

state_colors = {
    NubsState.ACTIVE: "green",
    NubsState.ISOLATED: "orange",
    NubsState.TERMINATED: "red"
}

st.markdown(f"### Current State: :{state_colors[current_state]}[{current_state.value}]")

if current_state == NubsState.ACTIVE:
    st.success("System is operating normally. Bridge is active.")
elif current_state == NubsState.ISOLATED:
    st.warning("System is isolated. Network revoked, processes suspended. Awaiting admin review.")
elif current_state == NubsState.TERMINATED:
    st.error("KILL SWITCH ENGAGED. Processes terminated, memory wiped. Manual system reset required.")

# --- Process Registry Display ---
st.header("Managed Processes")
if current_state == NubsState.TERMINATED:
    st.info("Process registry locked due to termination.")
else:
    cols = st.columns(3)
    for i, proc in enumerate(bridge.managed_processes):
        with cols[i % 3]:
            status = "🟢 Running" if proc.is_running else "🔴 Suspended/Killed"
            st.metric(label=f"PID: {proc.pid}", value=proc.name, delta=status)

st.markdown(f"**Network Bridge:** {'🟢 Active' if bridge.network_bridge_active else '🔴 Revoked'}")
st.markdown(f"**Memory Wiped:** {'Yes' if bridge.memory_wiped else 'No'}")

# --- Manual Controls ---
st.header("Manual Controls")
st.markdown("*Simulate triggers or perform admin overrides.*")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚠️ Simulate CPU Spike (>90%)", disabled=(current_state == NubsState.TERMINATED)):
        engine.evaluate_triggers(cpu_usage=95.0, unauthorized_access=False)
        st.rerun()

with col2:
    if st.button("🚨 Simulate Security Breach", disabled=(current_state == NubsState.TERMINATED)):
        engine.evaluate_triggers(cpu_usage=30.0, unauthorized_access=True)
        st.rerun()

with col3:
    if st.button("🔓 Manual Admin Recovery", disabled=(current_state == NubsState.ACTIVE or current_state == NubsState.TERMINATED)):
        engine.transition_to(NubsState.ACTIVE, "Manual admin override via Dashboard")
        st.rerun()

if current_state == NubsState.TERMINATED:
    st.markdown("---")
    st.info("⚠️ **System Locked:** To recover from a TERMINATED state, please restart the NUBS application entirely.")