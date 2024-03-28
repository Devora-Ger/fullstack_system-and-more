import React from "react";
import { Link } from "react-router-dom";
import user from "./user.jpg";

const PatientDetail = (props) => {
  const { patient_id, name, address, date_of_birth, telephone, mobailphone } = props.location.state.patient;
  return (
    <div className="main">
      <div className="ui card centered">
        <div className="image">
          <img src={user} alt="user" />
        </div>
        <div className="patient">
          <div className="header">{patient_id} {name}</div>
          <div className="description">{address} {date_of_birth} {telephone} {mobailphone}</div>
        </div>
      </div>
      <div className="center-div">
        <Link to="/">
          <button className="ui button blue center">
            Back to Patient List
          </button>
        </Link>
      </div>
    </div>
  );
};

export default PatientDetail;