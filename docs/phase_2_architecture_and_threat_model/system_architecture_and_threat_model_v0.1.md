# System Architecture & Threat Model v0.1

## 1. High-Level System Architecture
NUBS is designed with a "Local-First, Privacy-Preserving" architecture. No personal data leaves the device.

```mermaid
graph TD
    A[User / Non-Technical Consumer] -->|Interacts with| B(NUBS Dashboard UI)
    B -->|Commands| C{NUBS Core Engine}
    C -->|1. Monitor| D[Local Heuristic AI Scanner]
    C -->|2. Act| E[OS Network/Process Controller]
    D -->|Flags Anomaly| C
    E -->|Severs/Restores| F[(Device Network Interfaces)]
    E -->|Suspends| G[(Suspicious Local Processes)]
    
    style C fill:#2ecc71,stroke:#333,stroke-width:2px
    style E fill:#e74c3c,stroke:#333,stroke-width:2px