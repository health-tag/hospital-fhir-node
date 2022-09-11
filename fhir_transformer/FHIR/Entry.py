from fhir_transformer.FHIR.Base import FHIRResource


class Entry:
    fullUrl: str
    resource: FHIRResource
    request = None

    def __init__(self, full_url: str, resource: FHIRResource, request):
        self.fullUrl = full_url
        self.resource = resource
        self.request = request
