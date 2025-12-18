import requests
import time

AMF_URL = "http://127.0.0.1:5003/attach"
UPF_URL = "http://127.0.0.1:5006/forward-data"

payload = {"imsi": "imsi-123456789"}

print("--- 1. CONTROL PLANE: Connecting to 5G Core... ---")
try:
    # 1. Attach to AMF
    response = requests.post(AMF_URL, json=payload)
    data = response.json()
    
    if response.status_code == 200:
        print("SUCCESS: Connected!")
        print(f"My IP Address: {data['ip_address']}")
        
        print("\n--- 2. USER PLANE: Browsing the Internet... ---")
        time.sleep(1) # Simulating delay
        
        # 2. Send Data through UPF
        data_response = requests.get(UPF_URL)
        print("Response from UPF:")
        print(data_response.json())
        
    else:
        print("FAILED: Connection rejected.")
        print(data)

except Exception as e:
    print(f"Error: {e}")