import requests

from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    address: str
    date_of_birth: str
    tel: int
    cell: int
    description: str = None  # Optional field


class Vaccination(BaseModel):
    patient_id: int
    vaccination_date: str
    vacc_manufacturer: str


class CoronaSick(BaseModel):
    patient_id: int
    date_sick: str
    date_recovered: str


v = {
    "patient_id": 600,
    "name": "lala",
    "address": "str",
    "date_of_birth": "2021-11-11",
    "cell": 222,
    "tel": 333
}

data = {
    "patient_id": 613,
    "vaccination_date": "2022-01-09",
    "vacc_manufacturer": "str"
}

# Set the headers to specify JSON content type
headers = {"Content-Type": "application/json"}

# response = requests.post("http://localhost:8000/add_patient", json=data, headers=headers)


response = requests.get("http://localhost:8000/read/")
#response = requests.delete("http://localhost:8000/delete/{}".format(12))
#response = requests.put("http://localhost:8000/update_person/{}".format(600), json=v, headers=headers)


if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
    print("Error creating item:", response.text)
