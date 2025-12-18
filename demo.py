import requests


try:
    dataj = {"nf_name":'nrf', "ip": "127.0.0.1", "port": 5000 }
    res = requests.post('http//localhost:5001/register,json=dataj')

    print(res.json)
except:
    print("error")


