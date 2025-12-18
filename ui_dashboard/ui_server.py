from flask import Flask, render_template, jsonify, request
import requests

# Initialize Flask to serve the UI
# We tell it where the templates folder is relative to this script
app = Flask(__name__, template_folder='templates', static_folder='static')

# --- CONFIG: Where are the Docker containers running on localhost? ---
NRF_URL = "http://127.0.0.1:5001"
AMF_URL = "http://127.0.0.1:5003"
UPF_URL = "http://127.0.0.1:5006"

# --- ROUTE 1: Serve the main dashboard HTML page ---
@app.route('/')
def index():
    return render_template('index.html')

# --- ROUTE 2: API to get Network Status (Browser calls this) ---
@app.route('/api/network-status')
def get_network_status():
    try:
        # Ask NRF who is alive
        response = requests.get(f"{NRF_URL}/nfs", timeout=2)
        # Add NRF itself to the list for visualization
        nfs = response.json()
        nfs["NRF"] = {"status": "active", "port": 5001}
        return jsonify(nfs)
    except Exception as e:
        # If NRF is down, return empty
        return jsonify({"error": "Network Down", "details": str(e)}), 503

# --- ROUTE 3: API to trigger Connection (Phone Connect Button) ---
@app.route('/api/phone-connect', methods=['POST'])
def phone_connect():
    imsi = request.json.get('imsi')
    try:
        print(f"UI requesting connection for {imsi}...")
        # Call the AMF container
        response = requests.post(f"{AMF_URL}/attach", json={"imsi": imsi}, timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to contact AMF: {e}"}), 500

# --- ROUTE 4: API to trigger Data Browse (Phone Browse Button) ---
@app.route('/api/phone-browse', methods=['GET'])
def phone_browse():
    try:
        print("UI requesting data browse...")
        # Call the UPF container
        response = requests.get(f"{UPF_URL}/forward-data", timeout=5)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": f"Failed to contact UPF: {e}"}), 500

if __name__ == '__main__':
    # Run this UI server on port 8000 to avoid conflicting with NFs
    print("--- 5G UI Dashboard starting on http://localhost:8000 ---")
    app.run(host='0.0.0.0', port=8000, debug=True)