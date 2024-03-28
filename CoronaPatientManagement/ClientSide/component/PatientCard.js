import React from "react"
import { Link } from "react-router-dom"
import user from './user.png';

const PatientCard = (props) => {
    const {patient_id, name, address, bate_of_birth, telephone, mobailphone} = props.patient;
    return(
        <div className="item">
            <img className="ui avatar image" src={user} alt="user" />
            <div className="patient">
                <Link to={{pathname: `/patient/${patient_id}`, state: {patient: props.patient}} }>
                    <div className="header">{patient_id}</div>
                    <div>{name}</div>
                </Link>
            </div>
            <i
                className="trash alternate outline icon"
                style={{ color: "red", marginTop: "7px", marginLeft: "10px" }}
                onClick={() => props.clickHandler(patient_id)}>
            </i>
            <Link to={{ pathname: "/update", state: { patient: props.patient } }}>
            <i
            className="edit alternate outline icon"
            style={{ color: "blue", marginTop: "7px" }}>
            </i>
            </Link>

        </div>
    );
}

export default PatientCard;