import requests


URL = "http://127.0.0.1:5001/register"


payload = {
    "nf_name": "imsi-123456789",
    "ip":"21212",
    "port":5000
}

print(f"--- Sending Attach Request to AMF at {URL} ---")

try:
    response = requests.post(URL, json=payload)
    
    print(f"Status Code: {response.status_code}")
    print("Response from 5G Core:")
    print(response.json())

except Exception as e:
    print(f"Error: {e}")
    