import jsonpickle
import requests

from csop.FHIR.Bundle import Bundle

# CONFIG SHOULD MOVE OUT OF THIS FILE
base_fhir_url = 'http://localhost:8080/fhir'
headers = {
    'apikey': '',
    "Content-Type": "application/json"
}


def send_bundle(bundle: Bundle):
    payload = jsonpickle.encode(bundle, unpicklable=False)
    print(payload)
    #res = requests.post(base_fhir_url, data=payload, headers=headers)
    #print(res.status_code)
    #print(res.content)
