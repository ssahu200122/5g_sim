import os
import requests
import time 
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIGURATION ---
NF_NAME = "AMF"
# In Docker, we listen on 0.0.0.0 to accept connections from outside the container
NF_IP = os.environ.get('NF_IP', '0.0.0.0')
NF_PORT = int(os.environ.get('NF_PORT', 5000))
# Default to localhost for testing, but Docker Compose will override this
NRF_URL = os.environ.get('NRF_URL', 'http://host.docker.internal:5001')

# --- HELPER: Find another NF via NRF ---
def get_service_url(target_nf_name):
    """
    Asks NRF for the IP/Port of a specific NF (e.g., 'AUSF', 'SMF').
    """
    try:
        # Ask NRF for the list of all NFs
        response = requests.get(f"{NRF_URL}/nfs", timeout=2)
        nfs = response.json()
        
        if target_nf_name in nfs:
            target = nfs[target_nf_name]
            # Construct the URL (e.g., http://smf:5000)
            return f"http://{target['ip']}:{target['port']}"
        else:
            print(f"ERROR: NRF does not have an entry for {target_nf_name}")
            return None
    except Exception as e:
        print(f"Error talking to NRF: {e}")
        return None

@app.route('/')
def home():
    return f"I am the {NF_NAME}. I control access."

# --- MAIN LOGIC: User Connection Request ---
@app.route('/attach', methods=['POST'])
def attach_user():
    data = request.json
    imsi = data.get('imsi')
    
    print(f"--> Received Attach Request for {imsi}")
    
    process_time = random.uniform(0.5, 1.5)
    time.sleep(process_time)
    # ---------------------------------------------------------
    # STEP 1: AUTHENTICATION (Talk to AUSF)
    # ---------------------------------------------------------
    ausf_url = get_service_url("AUSF")
    if not ausf_url:
        return jsonify({"error": "Network Error: Cannot find AUSF"}), 500
    
    print(f"--> Found AUSF at: {ausf_url}. Authenticating...")

    try:
        # Send Authentication Request to AUSF
        auth_response = requests.post(f"{ausf_url}/authenticate", json={"imsi": imsi}, timeout=2)
        
        if auth_response.status_code != 200:
            print(f"--> AUSF rejected {imsi}")
            return jsonify({"status": "Rejected", "reason": "Authentication Failed"}), 403
            
        print(f"--> AUSF confirmed {imsi} is valid.")

    except Exception as e:
        return jsonify({"error": f"AUSF Communication failed: {e}"}), 500

    # ---------------------------------------------------------
    # STEP 2: SESSION MANAGEMENT (Talk to SMF)
    # ---------------------------------------------------------
    smf_url = get_service_url("SMF")
    if not smf_url:
        return jsonify({"error": "Network Error: Cannot find SMF"}), 500

    print(f"--> Found SMF at: {smf_url}. Creating Session...")

    try:
        # Ask SMF to allocate IP and resources
        session_response = requests.post(f"{smf_url}/create-session", json={"imsi": imsi}, timeout=2)
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            user_ip = session_data.get('ue_ip')
            
            print(f"--> Session Active. User IP: {user_ip}")
            
            return jsonify({
                "status": "Connected",
                "message": f"Welcome to 5G, {imsi}",
                "ip_address": user_ip
            })
        else:
            return jsonify({"error": "SMF failed to create session"}), 500

    except Exception as e:
        return jsonify({"error": f"SMF Communication failed: {e}"}), 500

# --- REGISTRATION ---
def register_with_nrf():
    try:
        # Register ourselves so others know we exist
        requests.post(f"{NRF_URL}/register", json={"nf_name": NF_NAME, "ip": NF_IP, "port": NF_PORT}, timeout=2)
        print("SUCCESS: Registered with NRF")
    except:
        print(f"WARNING: Could not connect to NRF at {NRF_URL}")

if __name__ == '__main__':
    register_with_nrf()
    app.run(host='0.0.0.0', port=NF_PORT)