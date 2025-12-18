import requests

# The AMF is running on port 5003
AMF_URL = "http://127.0.0.1:5003/attach"

# Our SIM Card ID
payload = {
    "imsi": "imsi-123456789"
}

print(f"--- Sending Attach Request to AMF at {AMF_URL} ---")

try:
    response = requests.post(AMF_URL, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print("Response from 5G Core:")
    print(response.json())

except Exception as e:
    print(f"Error: {e}")
    