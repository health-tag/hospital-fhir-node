from fhir_transformer.utilities.holder import BundleResult, EntryResult
import jsonpickle
import requests

from fhir_transformer.FHIR.Bundle import Bundle
from fhir_transformer.fhir_transformer_config import base_fhir_url
from fhir_transformer.fhir_transformer_config import headers

actual_header = {
    **headers,
    "Content-Type": "application/json"
}


def send_bundle(bundle: Bundle) -> BundleResult:
    payload = jsonpickle.encode(bundle, unpicklable=False)
    try:
        res = requests.post(base_fhir_url, data=payload, headers=actual_header)
        fhir_response = res.json()
        results = [EntryResult(entry.resource.resourceType, entry.fullUrl) for entry in bundle.entry]
        for i, entry in enumerate(fhir_response["entry"]):
            results[i].status = entry["response"]["status"]
            results[i].location = entry["response"]["location"] if "location" in entry["response"] else None
        return BundleResult(res.status_code, results)
    except Exception as e:
        print(e)
        return BundleResult(1000,
                            [EntryResult(entry.resource.resourceType, entry.fullUrl, "Unable to send") for entry in
                             bundle.entry])
