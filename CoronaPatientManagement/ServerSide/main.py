import collections
from datetime import datetime


import mysql.connector
from fastapi import FastAPI, Body
import json

from starlette.middleware.cors import CORSMiddleware
from models import Person, Vaccination, CoronaSick


def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="bsdbsd",
            database="crud_python"
        )

        print("Connection Established")
        return conn
    except:
        print("Connection Error")


connection = connect_to_mysql()
cursor = connection.cursor()


def was_sick(patient_id):
    cursor.execute(
        "SELECT * FROM corona_patients WHERE patient_id={}".format(
            patient_id))
    result = cursor.fetchall()
    return 0 < len(result)


def is_the_patient_vaccines(patient_id):
    cursor.execute(
        "SELECT vaccination_date FROM corona_vaccination WHERE patient_id={}".format(
            patient_id))
    result = cursor.fetchall()
    return 0 < len(result)


def convert_patients_table_data_to_json(rows):
    user_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['patient_id'] = row[0]
        d['name'] = row[1]
        d['address'] = row[2]
        d['date_of_birth'] = row[3]
        d['tel'] = row[4]
        d['cell'] = row[5]
        user_list.append(dict(d))

    return json.dumps(user_list, indent=4, sort_keys=True, default=str)


def convert_corona_vaccination_table_data_to_json(rows, json_patient):
    user_list = []
    for row in rows:
        d = collections.OrderedDict()
        d['vaccination_date'] = row[1]
        d['manufacturer'] = row[2]
        user_list.append(dict(d))

    data = json.loads(json_patient)
    data["vaccination_date"] = {}

    for i, d in enumerate(user_list):
        data["vaccination_date"][i] = d

    return json.dumps(data, indent=4, sort_keys=True, default=str)


def convert_corona_patients_table_data_to_json(row, json_patient):
    d = {'sick_date': row[0][1], 'recovered_date': row[0][2]}
    data = json.loads(json_patient)
    data["corona sick"] = d

    return json.dumps(data, indent=4, sort_keys=True, default=str)


def is_patient_exist(patient_id):
    cursor.execute("SELECT * FROM patients WHERE patient_id={}".format(patient_id))
    result = cursor.fetchall()
    return 0 < len(result)


# Create a DataBase.
def create_database(database_name="crud_python"):
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
    connection.commit()
    print("DataBase created")


def able_addition_vacc(patient_id):
    cursor.execute("SELECT patient_id FROM corona_vaccination WHERE patient_id={}".format(patient_id))
    result = cursor.fetchall()
    return 4 > len(result)


def is_known_corona_sick(patient_id):
    cursor.execute("SELECT patient_id FROM corona_patients WHERE patient_id={}".format(patient_id))
    result = cursor.fetchall()

    return 0 < len(result)


# Create the tables.
def create_tables():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients(
        patient_id INTEGER PRIMARY KEY, 
        name VARCHAR(50) NOT NULL,
        address VARCHAR(50) NOT NULL,
        birth_date DATE NOT NULL,
        telephone VARCHAR(10), 
        cell_phone VARCHAR(10) NOT NULL
        );
        """)
    connection.commit()
    print("The table patients is created")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS corona_vaccination(
        patient_id INTEGER NOT NULL,
        vaccination_date DATE NOT NULL,
        vacc_manufacturer VARCHAR(20) NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        );
        """)
    connection.commit()
    print("The table corona_vaccination is created")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS corona_patients(
        patient_id INTEGER PRIMARY KEY,
        sick_date DATE,
        recovered_date DATE,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        );
        """)
    connection.commit()
    print("The table corona_patients is created")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/read")
async def read_patients_details():
    cursor.execute("SELECT * FROM patients")
    json_data = convert_patients_table_data_to_json(cursor.fetchall())
    # cursor.close()
    return json_data


@app.get("/read/{person_id}")
async def read_patient_details(person_id: int):
    if is_patient_exist(person_id):
        cursor.execute("SELECT * FROM patients WHERE patient_id={}".format(person_id))
        json_data = convert_patients_table_data_to_json(cursor.fetchall())
        if is_the_patient_vaccines(person_id):
            cursor.execute("SELECT * FROM corona_vaccination WHERE patient_id={}".format(person_id))
            json_data = convert_corona_vaccination_table_data_to_json(cursor.fetchall(), json_data)
        if was_sick(person_id):
            cursor.execute("SELECT * FROM corona_patients WHERE patient_id={}".format(person_id))
            json_data = convert_corona_patients_table_data_to_json(cursor.fetchall(), json_data)

        return json_data
    else:
        return {"message": "Person not exist in the system."}


@app.post("/add_patient")
async def create_item(person: Person = Body(...)):
    if is_patient_exist(person.id):
        return {"message": "The person already exist in the system."}
    else:
        sql = "INSERT INTO patients VALUES(%s, %s, %s, %s, %s, %s);"
        val = (person.id, person.name, person.address, person.date_of_birth, person.tel, person.cell)
        cursor.execute(sql, val)
        connection.commit()
        return {"message": "The person created successfully."}




def update_patient_details(person_id, patient: Person = Body(...)):
    if is_patient_exist(person_id):
        sql = "UPDATE patients SET name = %s, address = %s, telephone = %s, cell_phone = %s WHERE patient_id = %s;"
        val = (patient.name, patient.address, patient.tel, patient.cell, patient.id)
        cursor.execute(sql, val)
        connection.commit()
        return {"message": "Item updated successfully."}
    else:
        return {"message": "The patient doesnt exist in the system."}


def update_vaccination(person_id, vacc: Vaccination = Body(...)):
    if is_patient_exist(person_id):
        if able_addition_vacc(person_id):
            sql = "INSERT INTO corona_vaccination (patient_id, vaccination_date, vacc_manufacturer) VALUES (%s, %s, %s);"
            val = (vacc.patient_id, vacc.vaccination_date, vacc.vacc_manufacturer)
            cursor.execute(sql, val)
            connection.commit()
            return {"message": "Item updated successfully."}
        else:
            return {"massage": "The patient already received 4 vaccinations."}
    else:
        return {"message": "The patient doesnt exist in the system."}


def update_new_corona_patient(person_id, corona_patient: CoronaSick = Body(...)):
    if is_patient_exist(person_id):
        if is_known_corona_sick(person_id):
            return {"massage": "The patient was sick in the past."}
        else:
            sql = "INSERT INTO corona_patients (patient_id, sick_date, recovered_date) VALUES (%s, %s, %s);"
            val = (corona_patient.patient_id, corona_patient.date_sick, corona_patient.date_recovered)
            cursor.execute(sql, val)
            connection.commit()
            return {"message": "Item updated successfully."}
    else:
        return {"message": "The patient doesnt exist in the system."}


def update_corona_recovered(person_id, corona_patient: CoronaSick = Body(...)):
    if is_patient_exist(person_id):
        if is_known_corona_sick(cursor, person_id):
            cursor.execute("SELECT sick_date FROM corona_patients WHERE patient_id = {}".format(person_id))
            sick_date = cursor.fetchall()[0]
            if sick_date < corona_patient.date_recovered:
                sql = "UPDATE corona_patients SET recovered_date = %s WHERE patient_id = %s;"
                val = (sick_date, person_id)
                cursor.execute(sql, val)
                connection.commit()
                return {"message": "Item updated successfully."}
            else:
                return {"message": "The date is incorrect."}
        else:
            return {"message": "The patient wasn't sick in corona."}
    else:
        return {"message": "The patient doesnt exist in the system."}


@app.put("/update_person/{patient_id}")
async def update_person_details(patient_id: int, person: Person):
    return update_patient_details(patient_id, person)


@app.put("/update_vacc/{patient_id}")
async def update_vacc(patient_id: int, vacc: Vaccination):
    return update_vaccination(patient_id, vacc)


@app.put("/update_corona_patient/{patient_id}")
async def update_corona_sick(patient_id: int, corona_sick: CoronaSick):
    if was_sick(patient_id):
        return update_corona_recovered(patient_id, corona_sick)
    return update_new_corona_patient(patient_id, corona_sick)


@app.delete("/delete/{patient_id}")
async def delete_item(patient_id: int):
    if is_patient_exist(patient_id):
        cursor.execute("DELETE FROM corona_vaccination WHERE patient_id={}".format(patient_id))
        connection.commit()
        cursor.execute("DELETE FROM corona_patients WHERE patient_id={}".format(patient_id))
        connection.commit()
        cursor.execute("DELETE FROM patients WHERE patient_id={}".format(patient_id))
        connection.commit()
        return {"message": "The patient deleted successfully from the system."}
    else:
        return {"message": "This person not exist in the system."}


'''def main():
    print(read_patient_details(600))
'''

if __name__ == "__main__":
    # main()
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
