import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# --- CONFIG ---
NF_NAME = "UDM"
NF_IP = os.environ.get('NF_IP', '0.0.0.0')
NF_PORT = int(os.environ.get('NF_PORT', 5000))
NRF_URL = os.environ.get('NRF_URL', 'http://host.docker.internal:5001/register') 
# Note: 'host.docker.internal' lets a container talk to the host machine's localhost on Windows/Mac. 
# On Linux, we might need a different network setup, but we'll fix that in the Docker Compose step.

# --- SIM CARD DATABASE (Hardcoded for now) ---
SUBSCRIBER_DB = {
    "imsi-123456789": {
        "k": "secret-key-A",
        "amf_key": "8000",
        "allowed_slices": ["slice-1", "slice-2"]
    },
    "imsi-999999999": {
        "k": "secret-key-B",
        "amf_key": "9000",
        "allowed_slices": ["slice-1"]
    }
}

@app.route('/')
def home():
    return f"I am the {NF_NAME}. I hold subscriber data."

# --- NEW: Retrieve Subscriber Data ---
@app.route('/subscriber/<imsi>', methods=['GET'])
def get_subscriber(imsi):
    user = SUBSCRIBER_DB.get(imsi)
    if user:
        print(f"--> Found profile for {imsi}")
        return jsonify(user), 200
    else:
        print(f"--> User {imsi} not found!")
        return jsonify({"error": "User not found"}), 404

# --- REGISTRATION ---
def register_with_nrf():
    # In a real Docker network, we can't use 0.0.0.0 to tell others where we are.
    # We will fix the IPs perfectly in the Docker Compose step (Step 7).
    # For now, this is just to prove it runs.
    try:
        data = {"nf_name": NF_NAME, "ip": NF_IP, "port": NF_PORT}
        requests.post(NRF_URL, json=data, timeout=2)
        print("SUCCESS: Registered with NRF")
    except:
        print("WARNING: Could not connect to NRF (Normal if NRF is not running yet)")

if __name__ == '__main__':
    register_with_nrf()
    app.run(host='0.0.0.0', port=NF_PORT)