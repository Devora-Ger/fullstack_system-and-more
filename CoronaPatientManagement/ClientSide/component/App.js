import React, {useState, useEffect} from "react";
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";
import api from "./api/patients";
import './App.css';
import Header from './Header';
import AddPatient from './AddPatient';
import PatientList from './PatientList';
import PtientDetail from "./PatientDetails";

function App() {
  const LOCAL_STORAGE_KEY = "patients"
  const [patients, setPatients] = useState([]);

  const [searchTerm, setSearchTerm] =  useState("");
  const [searchResalts, setSearchResalt] = useState([]);

  const retrivePatients = async ()=>{
    const response = await api.get("/read");
    return response.data;
  };

  const addPatientHandler = async (patient)=>{
    console.log(patient);
    const request = {
      patient_id: patient.patient_id, 
      ...patient
    }

    const response = await api.post("/add_patient", request);
    console.log(response);
    setPatients([...patients, response.data])
  };

  const updatePatientHandler = async (patient)=>{
    console.log(patient);

    const response = await api.put(`/add_patient/${patient.patient_id}`, patient);
    console.log(response.data);
    const { patient_id, name, address, dat_of_birth, telephone, mobailphne} = response.data;
    setPatients(
      patients.map((patient) => {
        return patient.patient_id === patient_id ? {...response.data} : patient;
      })
    );
  };
  const removePatientHandler = async (patient_id) => {
    await api.delete(`/delete/${patient_id}`);
    const newPatientList = patients.filter((patient)=>{
      return patient.patient_id !== patient_id;
    });

    setPatients(newPatientList);
  };

  const searchHandler = (searchTerm)=>{
    setSearchTerm(searchTerm);
    if (searchTerm !== "") {
      const newPatientList = patients.filter((patient)=>{
        return Object.values(patient)
        .join(" ")
        .toLowerCase()
        .includes(searchTerm.toLowerCase());
      });
      setSearchResalt(newPatientList);
    } else {
      setSearchResalt(patients);
    }
  };

  useEffect(()=>{
    // const retrivePatients = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    // if (retrivePatients) setPatients(retrivePatients);
    const getAllPatients = async() => {
      const allPatients = await retrivePatients();
      if (allPatients) setPatients(allPatients)
    };

    getAllPatients();
  },[]);

  useEffect(()=>{
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(patients));
  },[patients]);

  return (
    <div className="ui container">
      <Router>
        <Header />
        <Routes>
          <Route 
            path="/" 
            exact 
            render={(props)=>(
              <PatientList 
                {...props} 
                patients={searchTerm.length < 1 ? patients : searchResalts} 
                getPatientId={removePatientHandler}
                term={searchTerm}
                searchKeyword={ searchHandler}
                />
              )}
          />

          <Route 
            path="/add"
            exact 
            render={(props)=>(
              <AddPatient 
                {...props} 
                addPatientHandler={addPatientHandler}
              />
            )}
          />

          <Route 
            path="/patient/:patient_id"
            exact 
            Component={PatientDetail}
          />

          <Route 
            path="/update"
            exact 
            render={(props)=>(
              <UpdatePatient 
                {...props} 
                updatePatientHandler={updatePatientHandler}
              />
            )}
          /> 
        
        </Routes>

        
      </Router> 
      
    </div>
  )
}

export default App;
