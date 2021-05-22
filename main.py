from fhirpy import SyncFHIRClient
from datetime import datetime as dt


HAPI_BASE_URL = "http://localhost:8080/baseR4"


class Patient:
    def __init__(self, patient):
        self.name = patient["name"][0].given[0]
        self.surname = patient["name"][0].family
        self.gender = patient["gender"]
        self.birth_date = patient["birthDate"]
        self.identifier =  patient["identifier"][0].value
        self.id = patient["id"]

        self.observations = []
        self.medications = []

    def prepare_observations(self):

        if len(self.observations) == 0:
            client = SyncFHIRClient(HAPI_BASE_URL)
            resources = client.resources('Observation')
            resources = resources.search(subject=self.id).limit(10000).sort('date')
            observations = resources.fetch()

            for observation in observations:
                observation_dict = {
                    "category": observation["category"][0].coding[0].display,
                    "name": observation["code"].coding[0].display,
                    "date": observation["effectiveDateTime"]
                }
                if "component" in observation.keys():
                    values = []
                    units = []
                    specific_names = []
                    for x in observation["component"]:
                        specific_names.append(x.code.coding[0].display)
                        values.append(x.valueQuantity.value)
                        units.append(x.valueQuantity.unit)
                    observation_dict["value"] = values
                    observation_dict["unit"] = units
                    observation_dict["specific_name"] = specific_names
                    observation_dict["type"] = 'values'  # wiele wartości
                elif "valueQuantity" in observation.keys():
                    observation_dict["value"] = observation["valueQuantity"].value
                    observation_dict["unit"] = observation["valueQuantity"].unit
                    observation_dict["type"] = 'value'  # jedna wartość
                else:
                    observation_dict["type"] = 'text'  # brak wartości

                self.observations.append(observation_dict)

    def prepare_medications(self):
        if len(self.medications) == 0:
            client = SyncFHIRClient(HAPI_BASE_URL)
            resources = client.resources('MedicationRequest')
            resources = resources.search(subject=self.id).limit(10000)
            medication_requests = resources.fetch()

            for medication_request in medication_requests:
                medication_dict = {
                    "name": medication_request["medicationCodeableConcept"].coding[0].display,
                    "date": medication_request["authoredOn"],
                    "type": 'medication'  #aby sprawdzac typ podczas przechodzenia po zmieszanej liscie
                }
                self.medications.append(medication_dict)

    def get_history_in_range(self, start_date, end_date):

        history = []

        start_date = dt.strptime(start_date,"%Y-%m-%d")
        end_date = dt.strptime(end_date,"%Y-%m-%d")

        counter = 0
        for obs in self.observations:

            obs_date =  dt.strptime(obs['date'][:16], "%Y-%m-%dT%H:%M")
            if(obs_date<start_date):
                continue
            elif(obs_date>end_date):
                break

            while counter<len(self.medications) and dt.strptime(self.medications[counter]['date'][:16],"%Y-%m-%dT%H:%M")< obs_date:
                if dt.strptime(self.medications[counter]['date'][:16],"%Y-%m-%dT%H:%M")<start_date:
                    counter+=1
                    continue
                elif dt.strptime(self.medications[counter]['date'][:16],"%Y-%m-%dT%H:%M")>end_date:
                    break
                else:
                    history.append(self.medications[counter])
                counter += 1

            history.append(obs)

        for i in range(counter,len(self.medications)):
            med_date = dt.strptime(self.medications[i]['date'][:16],"%Y-%m-%dT%H:%M")
            if(med_date<start_date):
                continue
            elif(med_date>end_date):
                break
            else:
                history.append(self.medications[i])

        print("(get_history) found ",len(history)," notes between ",start_date," and ",end_date)

        return  history

def main():
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('Patient')
    resources = resources.search().limit(10000)
    patients = resources.fetch()
    patient_list = []
    for patient in patients:
        patient_list.append(Patient(patient))

    print("(main) loaded",len(patient_list), "patients")

    # DO TESTOW DATY I LADOWANIA
    patient_list[0].prepare_medications()
    patient_list[0].prepare_observations()


    history = patient_list[0].get_history_in_range('2007-05-08','2008-01-02')  # yyyy-mm-dd
    for x in history:
        print("DATE: ", x['date']," | NAME: ",x['name'] )
    # KONIEC TESTOW  DATY I LADOWANIA

if __name__ == "__main__":
    main()












# ------------------------------------------------- UNUSED OLD FUNCTIONS

def get_patient_info(patient):
    print(patient["name"][0].given[0])  #imie
    print(patient["name"][0].family)    #naziwsko
    print(patient["gender"])    #plec
    print(patient["birthDate"]) #data urodzenia
    print(patient["identifier"][0].value) #identyfikator


def get_patient_observation(patient):

    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('Observation')
    resources = resources.search(subject=patient["id"]).sort('-date')
    observations = resources.fetch()
    observation = observations.pop()
    print(observation["category"][0].coding[0].display) # coding (display) Rodzaj obserwacji np parametry życiowe
    print(observation["code"].coding[0].display) # coding (display) Nazwa oberwacji np. masa ciala
    print(observation["valueQuantity"].value) # wartosc obserwacji
    print(observation["valueQuantity"].unit)  # jednostka miary

    print(observation["effectiveDateTime"])

def get_patient_medication_request(patient):
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('MedicationRequest')
    resources = resources.search(subject=patient["id"])
    medication_requests = resources.fetch()
    medication_request = medication_requests.pop()
    print(medication_request["medicationCodeableConcept"].coding[0].display)


def get_observations(patient):
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('Observation')
    resources = resources.search(subject=patient["id"]).limit(10000).sort('-date')
    observations = resources.fetch()

    observations_list = []

    for observation in observations:
        observation_dict = {
            "category": observation["category"][0].coding[0].display,
            "name": observation["code"].coding[0].display,
            "date": observation["effectiveDateTime"]
        }
        if "component" in observation.keys():
            values = []
            units = []
            specific_names = []
            for x in observation["component"]:
                specific_names.append(x.code.coding[0].display)
                values.append(x.valueQuantity.value)
                units.append(x.valueQuantity.unit)
            observation_dict["value"] = values
            observation_dict["unit"] = units
            observation_dict["specific_name"] = specific_names
            observation_dict["type"] = 'values'  # wiele wartości
        elif "valueQuantity" in observation.keys():
            observation_dict["value"] = observation["valueQuantity"].value
            observation_dict["unit"] = observation["valueQuantity"].unit
            observation_dict["type"] = 'value'  #jedna wartość
        else:
            observation_dict["type"] = 'text'  #brak wartości

        observations_list.append(observation_dict)


    return observations_list


def get_medication_requests(patient):
    client = SyncFHIRClient(HAPI_BASE_URL)
    resources = client.resources('MedicationRequest')
    resources = resources.search(subject=patient["id"]).limit(10000)
    medication_requests = resources.fetch()

    medication_requests_list = []


    for medication_request in medication_requests:
        medication_dict = {

            "name":medication_request["medicationCodeableConcept"].coding[0].display ,
            "date":medication_request["authoredOn"]
        }
        medication_requests_list.append(medication_dict)

    return medication_requests_list