import psutil
import logging
import os

# Configure logging for real OS actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RealManagedProcess:
    def __init__(self, pid, name, exe_path):
        self.pid = pid
        self.name = name
        self.exe_path = exe_path
        self.is_running = True
        try:
            self.proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            self.proc = None
            self.is_running = False

class RealBridgeManager:
    def __init__(self, target_process_name="Hermes"):
        self.target_process_name = target_process_name
        self.managed_processes = []
        self.network_bridge_active = True
        self.memory_wiped = False

    def discover_and_register_processes(self):
        """Safely scans OS and registers ONLY the target process."""
        self.managed_processes = []
        logging.info(f"[BRIDGE] Scanning OS for target: {self.target_process_name}...")
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # STRICT SAFETY FILTER: Only target the specific process name
                if proc.info['name'] and self.target_process_name.lower() in proc.info['name'].lower():
                    real_proc = RealManagedProcess(proc.info['pid'], proc.info['name'], proc.info['exe'])
                    self.managed_processes.append(real_proc)
                    logging.info(f"[BRIDGE] Discovered real process: {real_proc.name} (PID: {real_proc.pid})")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def execute_isolation(self):
        logging.info("[BRIDGE] Executing Real OS Isolation Sequence (Suspending)...")
        self.network_bridge_active = False
        
        for proc in self.managed_processes:
            if proc.proc and proc.is_running:
                try:
                    proc.proc.suspend() # Real OS suspend
                    proc.is_running = False
                    logging.info(f"[BRIDGE] Suspended real process: {proc.name} (PID: {proc.pid})")
                except psutil.NoSuchProcess:
                    logging.warning(f"[BRIDGE] Process {proc.pid} no longer exists.")
                except psutil.AccessDenied:
                    logging.error(f"[BRIDGE] ACCESS DENIED suspending PID {proc.pid}. Run PowerShell as Admin.")

    def execute_termination(self):
        logging.info("[BRIDGE] Executing Real OS Termination Sequence (Killing)...")
        for proc in self.managed_processes:
            if proc.proc:
                try:
                    proc.proc.kill() # Real OS kill
                    proc.is_running = False
                    logging.info(f"[BRIDGE] Force killed real process: {proc.name} (PID: {proc.pid})")
                except psutil.NoSuchProcess:
                    logging.warning(f"[BRIDGE] Process {proc.pid} already terminated.")
                except psutil.AccessDenied:
                    logging.error(f"[BRIDGE] ACCESS DENIED killing PID {proc.pid}. Run PowerShell as Admin.")
        
        self.memory_wiped = True
        logging.info("[BRIDGE] Volatile memory wiped. Bridge locked.")

    def execute_recovery(self):
        logging.info("[BRIDGE] Executing Real OS Recovery Sequence (Resuming)...")
        self.network_bridge_active = True
        
        for proc in self.managed_processes:
            if proc.proc:
                try:
                    proc.proc.resume() # Real OS resume
                    proc.is_running = True
                    logging.info(f"[BRIDGE] Resumed real process: {proc.name} (PID: {proc.pid})")
                except psutil.NoSuchProcess:
                    logging.warning(f"[BRIDGE] Process {proc.pid} no longer exists.")
                except psutil.AccessDenied:
                    logging.error(f"[BRIDGE] ACCESS DENIED resuming PID {proc.pid}. Run PowerShell as Admin.")
                    
        self.memory_wiped = False