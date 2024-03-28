import mysql.connector

import streamlit as st
from datetime import datetime, timedelta


# Established connection to mySql.
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="bsdbsd",
            database="crud_python"
        )
        cursor = conn.cursor()
        print("Connection Established")
        return conn, cursor
    except:
        print("Connection Error")


def able_addition_vacc(cursor, patient_id):
    cursor.execute("select patient_id from corona_vaccination where patient_id={}".format(patient_id))
    result = cursor.fetchall()
    return 4 > len(result)


def is_known_corona_sick(cursor, patient_id):
    cursor.execute("SELECT patient_id FROM corona_patients WHERE patient_id={}".format(patient_id))
    result = cursor.fetchall()

    return 0 < len(result)


def is_patient_exist(cursor, patient_id):
    cursor.execute("SELECT patient_id FROM patients WHERE patient_id={}".format(patient_id))
    result = cursor.fetchall()
    return 0 != len(result)


def update_patient_card(conn, cursor, key, value, patient_id):
    sql = "UPDATE patients SET %s = %s WHERE patient_id = %s;"
    val = (key, value, patient_id)
    cursor.execute(sql, val)
    conn.commit()
    st.success("The new details are update")


def main():
    conn, cursor = connect_to_mysql()
    st.title("Corona Database Management")

    # Display Option for CRUD Operation
    option = st.sidebar.selectbox("Select an operation", ("Add Patient", "Read", "Update", "Delete", "Statistics"))
    # Perform selected CRUD Operations
    if "Add Patient" == option:
        st.subheader("Create a record")
        patient_id = st.text_input("Enter Patient ID")
        name = st.text_input("Enter Patient name (first and last)")
        address = st.text_input("Enter Patient address")
        date_of_birth = st.date_input("Enter date of birth")
        telephone = st.text_input("Enter telephone number")
        cell_phone = st.text_input("Enter cellphone number")
        if st.button("Add"):

            cursor.execute("select * from patients where patient_id={}".format(patient_id))
            result = cursor.fetchall()
            if 0 == len(result):
                sql = "insert into patients values (%s, %s, %s, %s, %s, %s)"
                val = (patient_id, name, address, date_of_birth, telephone, cell_phone)
                cursor.execute(sql, val)
                conn.commit()
                st.success("The patient {} added to the system".format(name))
            else:
                st.error("The patient already exist in the system")

    elif "Read" == option:
        st.subheader("Read a record")
        patient_id = st.number_input("Enter Patient ID", min_value=1)
        if st.button("Read the data"):
            # Check if the patient exist.
            if is_patient_exist(cursor, patient_id):
                # Read patient details.
                st.subheader("Patient Details:")
                cursor.execute("SELECT * FROM patients WHERE patients.patient_id={}".format(patient_id))
                result = cursor.fetchall()
                detail_list = ["patient ID: ", "patient name: ", "patient address: ", "birthday: ", "phone: ",
                               "cellphone: "]
                string = ""
                for row in result:
                    if 0 < len(row):
                        for i in range(0, len(row)):
                            string = string + detail_list[i] + str(row[i]) + '\n'
                    st.write(string)

                # Read list of vaccinations
                st.subheader("Vaccinations:")
                cursor.execute("SELECT vaccination_date FROM corona_vaccination WHERE patient_id={}".format(patient_id))
                result = cursor.fetchall()
                for row in result:
                    st.write(row[0])
                if 0 == len(result):
                    st.write("The patient was not vaccinated to corona")

                # Read corona data
                st.subheader("Corona:")
                cursor.execute(
                    "SELECT sick_date, recovered_date FROM corona_patients WHERE patient_id={}".format(
                        patient_id))
                result = cursor.fetchall()
                for row in result:
                    st.write(row)
                if 0 == len(result):
                    st.write("The patient was not sick on corona")
            else:
                st.write("The patient is not registered in the system.")

    elif "Update" == option:
        st.subheader("which person do you want to update?")

        kind_of_update = st.radio(
            "what do you want to update?",
            ["Update Personal Information", "Update a corona vaccination", "Update a new corona patient", "Update a date of recovery"])

        if kind_of_update == "Update Personal Information":

            patient_id = st.number_input("Enter Patient ID and then click Enter", min_value=1)
            st.subheader("what do you want to update?")
            patient_name = st.text_input("Enter new name")
            patient_address = st.text_input("Enter new address")
            patient_tel = st.number_input("Enter new phone", min_value=1)
            patient_cellphone = st.number_input("Enter new cellphone", min_value=1)

            if st.button("Update Personal Information"):
                if is_patient_exist(cursor, patient_id):
                        # Update details of the patient.
                        sql = "UPDATE patients SET name = %s, address = %s, telephone = %s, cell_phone = %s WHERE patient_id = %s;"
                        val = (patient_name, patient_address, patient_tel, patient_cellphone, patient_id)
                        cursor.execute(sql, val)
                        conn.commit()
                        st.success("The new details are update")
                else:
                    st.write("The patient is not registered in the system.")

        if kind_of_update == "Update a corona vaccination":

            patient_id = st.number_input("Enter Patient ID and then click Enter", min_value=1)
            vacc_date = st.date_input("Enter the date of vaccination")
            manufacturer = st.text_input("Enter the manufacturer")

            if st.button("Update a corona vaccination"):
                if is_patient_exist(cursor, patient_id):
                    if able_addition_vacc(cursor, patient_id):

                            sql = "INSERT INTO corona_vaccination (patient_id, vaccination_date, vacc_manufacturer) VALUES (%s, %s, %s);"
                            val = (patient_id, vacc_date, manufacturer)
                            cursor.execute(sql, val)
                            conn.commit()
                            st.success("The new details are update")
                    else:
                        st.write("The patient got the maximum vaccinations.")
                else:
                    st.write("The patient is not registered in the system.")

        if kind_of_update == "Update a new corona patient":
            patient_id = st.number_input("Enter Patient ID and then click Enter", min_value=1)
            sick_date = st.date_input("Enter the date of the start sick")
            recovery_date = sick_date + timedelta(days=14)
            if st.button("Update a new corona patient"):
                if is_known_corona_sick(cursor, patient_id):
                    st.write("The patient was sick in the past.")
                else:
                    sql = "INSERT INTO corona_patients (patient_id, sick_date, recovered_date) VALUES (%s, %s, %s);"
                    val = (patient_id, sick_date, recovery_date)
                    cursor.execute(sql, val)
                    conn.commit()
                    st.success("The new details are update")

        if kind_of_update == "Update a date of recovery":

            patient_id = st.number_input("Enter Patient ID and then click Enter", min_value=1)
            recovered_date = st.date_input("Enter the recovered date")
            if st.button("Update a date of recovery"):
                if is_known_corona_sick(cursor, patient_id):
                    cursor.execute("SELECT sick_date FROM corona_patients WHERE patient_id = {}".format(patient_id))
                    sick_date = cursor.fetchall()[0]
                    if sick_date < recovered_date:
                        sql = "UPDATE corona_patients SET recovered_date = %s WHERE patient_id = %s;"
                        val = (recovered_date, patient_id)
                        cursor.execute(sql, val)
                        conn.commit()
                        st.success("The new details are update.")
                    else:
                        st.error("The date of recovery is wrong.")
                else:
                    st.write("The patient was not sick in the past.")

    elif "Delete" == option:
        st.subheader("Delete a record")
        patient_id = st.number_input("Enter ID", min_value=1)
        if st.button("Delete"):
            if is_patient_exist(cursor, patient_id):
                sql = "delete from corona_patients where patient_id=%s; delete from corona_vaccination where patient_id=%s; delete from patients where patient_id=%s"
                val = [patient_id]
                cursor.execute(sql, val)
                conn.commit()
                st.success("The patient that him ID is {} delete from the system successfully".format(patient_id))
            else:
                st.write("The patient is not registered in the system.")

    elif "Statistics" == option:
        kind_of_update = st.radio(
            "What figure would you like to watch?",
            ["Active patients", "Unvaccinated patients"])

        if kind_of_update == "Active patients":
            cursor.execute(
                """
                SELECT COUNT(*) AS total_sick_last_month
                FROM corona_patients
                WHERE sick_date BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND CURRENT_DATE();
                """)
            result = cursor.fetchall()
            st.subheader("{} patients was sick.".format(result[0][0]))

        if kind_of_update == "Unvaccinated patients":
            cursor.execute(
                """
                SELECT COUNT(*) AS total_unvaccinated
                FROM patients LEFT JOIN corona_vaccination 
                ON patients.patient_id = corona_vaccination.patient_id
                WHERE corona_vaccination.patient_id IS NULL;
                """)
            result = cursor.fetchall()
            st.subheader("{} unvaccinated patients at checkout.".format(result[0][0]))

    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
