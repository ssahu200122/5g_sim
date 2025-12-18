# 5G Core Network Simulation (SBA Architecture)

A full-stack, cloud-native simulation of a 5G Core Network based on the 3GPP Service-Based Architecture (SBA). This project demonstrates the interaction between various Network Functions (NFs), the separation of Control and User planes, and realistic network behavior through simulated physics.

##  Overview

This project simulates the logic and signaling of a 5G Standalone (SA) Core. Unlike traditional monolithic simulations, this implementation uses a microservices approach where each Network Function is isolated in a Docker container and communicates via REST APIs.

### Key Features

- **Service-Based Architecture (SBA):** Dynamic service discovery using a Network Repository Function (NRF).
- 
- **Control Plane & User Plane Separation (CUPS):** Distinct paths for signaling (AMF/AUSF/UDM) and data traffic (UPF/DN).
    
- **Simulated Physics:** Injected latency and jitter to mimic real-world fiber optic and processing delays.
    
- **NOC Dashboard:** A real-time web-based monitoring interface to visualize network health and subscriber status.
    
- **UE Simulator:** A simulated smartphone interface to trigger attachments and data sessions.
    

##  Architecture & Network Functions

The simulation implements the following 3GPP-standard functions:

|Function|Full Name|Role|
|---|---|---|
|**NRF**|Network Repository Function|The "Phonebook" that handles service registration and discovery.|
|**AMF**|Access & Mobility Management|The entry point for the UE; manages authentication and sessions.|
|**AUSF**|Authentication Server|Handles security verification logic between AMF and UDM.|
|**UDM**|Unified Data Management|The subscriber database containing IMSI profiles and keys.|
|**SMF**|Session Management|Allocates IP addresses and manages PDU session context.|
|**UPF**|User Plane Function|The high-speed router that forwards user data to the internet.|
|**DN**|Data Network|Represents the external internet/content servers (e.g., Video Server).|

##  Tech Stack

- **Backend:** Python 3.9, Flask (REST APIs)
    
- **Containerization:** Docker, Docker Compose
    
- **Frontend:** HTML5, CSS3 (Tailwind-style), Vanilla JavaScript
    
- **Communication:** HTTP/1.1 (Simulating HTTP/2 Service Based Interfaces)
    

##  Folder Structure

```
5g_sim/
├── docker-compose.yml          # Main orchestration file
├── test_ue.py                  # CLI-based User Equipment simulator
├── amf/, ausf/, smf/...        # Individual NF directories (Dockerfile + Code)
└── ui_dashboard/
    ├── ui_server.py            # Backend for the monitoring dashboard
    └── templates/
        └── index.html          # Frontend Dashboard & Phone UI
```

##  Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/ "null") installed and running.
    
- Python 3.x installed (for running the UI and test scripts).
    

### Installation & Setup

1. **Clone the repository:**
    
    ```
    git clone <your-repo-link>
    cd 5g_sim
    ```
    
2. **Start the 5G Core:** Use Docker Compose to build and launch all 7 Network Functions:
    
    ```
    docker-compose up --build
    ```
    
    _Note: Wait until you see "Registered with NRF" logs from all components._
    
3. **Launch the Dashboard:** In a new terminal, start the UI server:
    
    ```
    cd ui_dashboard
    python ui_server.py
    ```
    

##  Usage

### 1. Interactive Dashboard (Recommended)

Open your browser and navigate to: **`http://localhost:8000`**

- **Monitor:** View the "Core Network Status" panel. Active NFs will turn **Green** automatically.
    
- **Connect:** Enter an IMSI (e.g., `imsi-123456789`) in the phone simulator and click **Connect to 5G**.
    
- **Data:** Once connected, click **Browse Internet** to simulate a 4K video stream request through the UPF.
    

### 2. CLI Testing

If you prefer the command line, use the provided test script:

```
python test_ue.py
```

##  Simulation Details (The "Physics")

This project includes a simulated **Physics Engine** to make the network behavior realistic:

- **AMF Processing Delay:** 0.5s - 1.5s (Simulating decryption/logic).
    
- **Cable Propagation Delay:** 0.2s - 0.6s (Simulating fiber optic travel in the UPF).
    
- **DN Buffering:** 1.0s - 3.0s (Simulating content server response time).
    
