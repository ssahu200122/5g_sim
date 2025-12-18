import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# CONFIG
NF_NAME = "NRF"
NF_IP = os.environ.get('NF_IP', '0.0.0.0')
NF_PORT = int(os.environ.get('NF_PORT', 5000))

# THE DATABASE (In-memory storage for registered NFs)
# Structure: { "AMF": { "ip": "...", "port": "..." }, "UDM": { ... } }
registered_nfs = {}

@app.route('/')
def home():
    return f"This is the {NF_NAME}. I hold the database of all NFs."

# 1. Registration Endpoint (Other NFs will call this)
@app.route('/register', methods=['POST'])
def register_nf():
    data = request.json
    nf_name = data.get('nf_name')
    ip = data.get('ip')
    port = data.get('port')
    
    if not nf_name or not ip:
        return jsonify({"error": "Missing data"}), 400

    # Save to our database
    registered_nfs[nf_name] = {
        "ip": ip,
        "port": port,
        "status": "active"
    }
    
    print(f"--> Registered New NF: {nf_name} at {ip}:{port}")
    return jsonify({"message": f"Registration successful for {nf_name}"}), 200

# 2. Discovery Endpoint (To see who is online)
@app.route('/nfs', methods=['GET'])
def get_all_nfs():
    return jsonify(registered_nfs)

@app.route('/status')
def status():
    return jsonify({"nf_name": NF_NAME, "status": "running", "count": len(registered_nfs)})

if __name__ == '__main__':
    print(f"--- Starting {NF_NAME} on port {NF_PORT} ---")
    app.run(host='0.0.0.0', port=NF_PORT)