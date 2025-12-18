import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIG ---
NF_NAME = "AUSF"
NF_IP = os.environ.get('NF_IP', '0.0.0.0')
NF_PORT = int(os.environ.get('NF_PORT', 5000))
NRF_URL = os.environ.get('NRF_URL', 'http://host.docker.internal:5001')

# --- HELPER ---
def get_service_url(target_nf):
    try:
        response = requests.get(f"{NRF_URL}/nfs")
        nfs = response.json()
        if target_nf in nfs:
            target = nfs[target_nf]
            return f"http://{target['ip']}:{target['port']}"
    except:
        return None
    return None

@app.route('/')
def home():
    return f"I am {NF_NAME}. I handle security."

# --- AUTHENTICATION ENDPOINT (Called by AMF) ---
@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    imsi = data.get('imsi')
    
    print(f"--> Authenticating {imsi}...")
    
    # 1. Find UDM
    udm_url = get_service_url("UDM")
    if not udm_url:
        return jsonify({"error": "UDM not found"}), 500
        
    # 2. Verify with UDM
    try:
        # We ask UDM for the user profile
        response = requests.get(f"{udm_url}/subscriber/{imsi}")
        
        if response.status_code == 200:
            print(f"--> User {imsi} Authentication SUCCESS")
            return jsonify({"result": "success", "key": "secure-key-123"}), 200
        else:
            print(f"--> User {imsi} Authentication FAILED")
            return jsonify({"result": "failure"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- REGISTRATION ---
def register_with_nrf():
    try:
        requests.post(f"{NRF_URL}/register", json={"nf_name": NF_NAME, "ip": NF_IP, "port": NF_PORT})
        print("SUCCESS: Registered with NRF")
    except:
        pass

if __name__ == '__main__':
    register_with_nrf()
    app.run(host='0.0.0.0', port=NF_PORT)