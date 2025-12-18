import os
import time
import random
from flask import Flask, jsonify

app = Flask(__name__)
NF_PORT = int(os.environ.get('NF_PORT', 5000))

@app.route('/')
def home():
    return "I am the Internet (Data Network)."

# This simulates a video server or web page
@app.route('/content')
def get_content():

    download_time = random.uniform(1.0, 3.0)
    print(f"--> Buffering 4K Video... (Estimated time: {download_time:.2f}s)")
    time.sleep(download_time)
    return jsonify({
        "data": "Here is the 4K Video Stream you asked for!",
        "source": "Netflix-Simulated-Server"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=NF_PORT)