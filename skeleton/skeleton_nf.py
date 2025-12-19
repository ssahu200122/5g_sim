import os
import sys
import requests # <--- New Import
from flask import Flask, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
NF_NAME = os.environ.get('NF_NAME', 'Generic-NF')
NF_IP = os.environ.get('NF_IP', '127.0.0.1') 
NF_PORT = int(os.environ.get('NF_PORT', 5000))

# The address of the NRF (The Phonebook)
# If running locally, NRF is at localhost:5001
NRF_URL = os.environ.get('NRF_URL', 'http://127.0.0.1:5001/register')

# --- ROUTES ---
@app.route('/')
def home():
    return f"Hello! I am {NF_NAME} running on {NF_IP}:{NF_PORT}"

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "nf_name": NF_NAME,
        "status": "active",
        "ip": NF_IP,
        "port": NF_PORT
    })

# --- REGISTRATION LOGIC ---
def register_with_nrf():
    print(f"--- Attempting to register {NF_NAME} with NRF at {NRF_URL} ---")
    data = {
        "nf_name": NF_NAME,
        "ip": NF_IP,
        "port": NF_PORT
    }
    try:
        # Send a POST request to the NRF
        response = requests.post(NRF_URL, json=data)
        if response.status_code == 200:
            print(f"SUCCESS: Registered with NRF!")
        else:
            print(f"WARNING: NRF returned error: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Could not connect to NRF. Is it running? Details: {e}")

# --- MAIN ---
if __name__ == '__main__':
    # 1. Try to register first
    register_with_nrf()
    
    # 2. Then start the server
    print(f"--- Starting {NF_NAME} on port {NF_PORT} ---")
    app.run(host='0.0.0.0', port=NF_PORT, debug=True)