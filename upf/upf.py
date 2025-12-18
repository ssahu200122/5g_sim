import os
import requests
import time 
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- CONFIG ---
NF_NAME = os.environ.get('NF_NAME', 'UPF')
NF_IP = os.environ.get('NF_IP', '0.0.0.0')
NF_PORT = int(os.environ.get('NF_PORT', 5000))
NRF_URL = os.environ.get('NRF_URL', 'http://host.docker.internal:5001')

# The UPF needs to know where the Internet is.
# In Docker Compose, we will name the DN container 'dn'.
DN_URL = "http://dn:5000"

@app.route('/')
def home():
    return f"I am {NF_NAME}. I route traffic."

# --- DATA PLANE (Simulates routing packets) ---
@app.route('/forward-data', methods=['GET'])
def forward_data():
    print(f"--> UPF received data packet from User. Forwarding to DN...")

    cable_delay = random.uniform(0.2, 0.6) 
    time.sleep(cable_delay)
    
    try:
        response = requests.get(f"{DN_URL}/content")
        
        data = response.json()
        # Add our own delay to the total
        total_latency = data.get('latency_ms', 0) + int(cable_delay * 1000)

        return jsonify({
            "status": "Success",
            "hop": "Via UPF (Fiber Optic Link)",
            "internet_response": data,
            "total_latency_ms": total_latency
        })
    except Exception as e:
        return jsonify({"error": f"Connection to Internet failed: {e}"}), 500

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