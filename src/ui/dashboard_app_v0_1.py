import sys
import os
import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Add src/core to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.abspath(os.path.join(current_dir, '..', 'core'))
sys.path.insert(0, core_dir)

from kill_switch_engine_v0_2 import KillSwitchEngine, NubsState
from bridge_manager_v0_2_real import RealBridgeManager

# Page Configuration
st.set_page_config(page_title="NUBS Dashboard", page_icon="🛡️", layout="centered")

st.title("🛡️ NUBS: Normal Users Bridge-Switch")
st.markdown("AI Personal Kill Switch – Monitor, Isolate, or Terminate AI Processes.")
st.markdown("---")

# Initialize Session State for Persistence
if "engine" not in st.session_state:
    bridge = RealBridgeManager(target_process_name="Hermes")
    bridge.discover_and_register_processes()
    st.session_state.engine = KillSwitchEngine(bridge_manager=bridge)

engine = st.session_state.engine
bridge = engine.bridge_manager
current_state = engine.get_state()

# Auto-refresh every 5 seconds to detect process changes
# This will trigger a rerun every 5 seconds
count = st_autorefresh(interval=5000, key="datarefresh")

# Re-discover processes on each auto-refresh (only if not TERMINATED)
if current_state != NubsState.TERMINATED:
    bridge.discover_and_register_processes()

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
    if len(bridge.managed_processes) == 0:
        st.warning("No target processes detected. Waiting for Hermes to start...")
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

# NEW: Reset System button (only appears when TERMINATED)
if current_state == NubsState.TERMINATED:
    st.markdown("---")
    st.warning("⚠️ **System Locked:** Kill switch engaged. To re-arm the system, click Reset below.")
    
    if st.button("🔄 Reset System & Re-Scan for Processes"):
        engine.reset_system("Manual reset via Dashboard - re-arming kill switch")
        st.success("✅ System reset complete. Re-scanning for target processes...")
        st.rerun()