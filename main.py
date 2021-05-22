from fhirpy import SyncFHIRClient

HAPI_BASE_URL = "http://localhost:8080/baseR4"

def main():
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('Patient')
    resources = resources.search(name='Amalia').limit(10).sort('name')
    patients = resources.fetch()
    patient = patients.pop()
    print(patient["name"][0])
    print(patient["name"][0].family)

if __name__ == "__main__":
    main()