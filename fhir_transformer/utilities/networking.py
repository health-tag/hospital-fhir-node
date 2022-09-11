import jsonpickle
import requests

from fhir_transformer.FHIR.Bundle import Bundle
from fhir_transformer.fhir_transformer_config import base_fhir_url
from fhir_transformer.fhir_transformer_config import headers

actual_header = {
    **headers,
    "Content-Type": "application/json"
}

def send_bundle(bundle: Bundle):
    payload = jsonpickle.encode(bundle, unpicklable=False)
    res = requests.post(base_fhir_url, data=payload, headers=actual_header)
    print(f"Bundle HTTP status code {res.status_code}")
    print(f"Bundle response")
    print(res.content)
