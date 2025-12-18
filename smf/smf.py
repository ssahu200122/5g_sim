import os
import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIG ---
NF_NAME = "SMF"
NF_IP = os.environ.get('NF_IP', '0.0.0.0')
NF_PORT = int(os.environ.get('NF_PORT', 5000))
NRF_URL = os.environ.get('NRF_URL', 'http://host.docker.internal:5001')

@app.route('/')
def home():
    return f"I am {NF_NAME}. I manage data sessions."

# --- SESSION CREATION (Called by AMF) ---
@app.route('/create-session', methods=['POST'])
def create_session():
    data = request.json
    imsi = data.get('imsi')
    
    print(f"--> Allocating IP address for {imsi}...")
    
    # Simulate assigning an IP address to the phone
    fake_ip = f"10.0.0.{random.randint(2, 254)}"
    
    print(f"--> Session Established. User IP: {fake_ip}")
    
    return jsonify({
        "status": "Session Created",
        "ue_ip": fake_ip,
        "dn_access": "internet"
    })

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