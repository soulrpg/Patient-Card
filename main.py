from fhirpy import SyncFHIRClient
from gui import *

HAPI_BASE_URL = "http://localhost:8080/baseR4"

def filter_by_surname(client, surname):
    resources = client.resources('Bundle')
    resources = resources.search(family=surname).sort('name')
    return resources.fetch()

def main():
    gui = GUI("Karta pacjenta", 600, 500, False)
    client = SyncFHIRClient(HAPI_BASE_URL)
    patients = filter_by_surname(client, "Shields502")
    print(patients)
    patient = patients.pop()
    print(patient["resourceType"])
    print(patient.keys())
    #print(patient.everything)
    #print(patient["name"][0])
    #print(patient["name"][0].family)

if __name__ == "__main__":
    main()