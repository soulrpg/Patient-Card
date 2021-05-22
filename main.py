from fhirpy import SyncFHIRClient

HAPI_BASE_URL = "http://localhost:8080/baseR4"

def get_patient_info(patient):
    print(patient["name"][0].given[0])  #imie
    print(patient["name"][0].family)    #naziwsko
    print(patient["gender"])    #plec
    print(patient["birthDate"]) #data urodzenia
    print(patient["identifier"][0].value) #identyfikator


def get_patient_observation(patient):

    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('Observation')
    resources = resources.search(subject=patient["id"])
    observations = resources.fetch()
    observation = observations.pop()
    print(observation["category"][0].coding[0].display) # coding (display) Rodzaj obserwacji np parametry życiowe
    print(observation["code"].coding[0].display) # coding (display) Nazwa oberwacji np. masa ciala
    print(observation["valueQuantity"].value) # wartosc obserwacji
    print(observation["valueQuantity"].unit)  # jednostka miary

def get_patient_medication_request(patient):
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('MedicationRequest')
    resources = resources.search(subject=patient["id"])
    medication_requests = resources.fetch()
    medication_request = medication_requests.pop()
    print(medication_request["medicationCodeableConcept"].coding[0].display)


def main():
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('Patient')
    resources = resources.search(name='Adam').limit(10).sort('name')
    patients = resources.fetch()
    patient = patients.pop()

    print("-------------------------")
    get_patient_info(patient)
    print("-------------------------")
    get_patient_observation(patient)
    print("-------------------------")
    get_patient_medication_request(patient)
    print("-------------------------")

if __name__ == "__main__":
    main()