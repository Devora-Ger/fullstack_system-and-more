import React, { useRef } from 'react';
import {Link } from "react-router-dom"
import PatientCard from './PatientCard';


const PatientList = (props) => {
    console.log(props);

    const inputEl = useRef("");
    const deletePatientHandler = (patient_id)=>{
        props.getPatientId(patient_id);
    };
    
    const renderPatientList = props.patients.map((patient) => {
        return(
            <PatientCard patient={patient} clickHandler ={deletePatientHandler} key={patient.patient_id}></PatientCard>
        );
    });

    const getSearchTerm = () => {
        props.searchKeeyword(inputEl.current.value);
    };

    return(
        <div className="main">
        <h2>
        Ptient List
            <Link to="/add"> 
                <button className="ui button blue right">Add Patient</button>
            </Link>
        </h2>
        <div className="ui search">
            <div className="ui icon input">
                <input 
                    ref={inputEl}
                    type="text" 
                    placeholder="Search Patient" 
                    className="prompt" 
                    value={props.term} 
                    onChange={getSearchTerm}
                />
                <i className="search icon" />
            </div>
        </div>
    <div className="ui celled list">
            {renderPatientList.length > 0 
            ? renderPatientList 
            : "No Patients available"}
        </div>
    </div>
    );
};

export default PatientList;