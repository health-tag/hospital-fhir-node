import jsonpickle
import requests

from csop.dataclasses.Bundle import Bundle

# CONFIG SHOULD MOVE OUT OF THIS FILE
base_fhir_url = 'http://localhost:8080/fhir'
headers = {
    'apikey': ''
}


def send_bundle(bundle: Bundle):
    res = requests.post(base_fhir_url, json=jsonpickle.encode(bundle, unpicklable=False), headers=headers)
    print(res.status_code)
    print(res.content)

