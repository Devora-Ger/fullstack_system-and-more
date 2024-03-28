import React from "react";

class AddPatient extends React.Component {
    state = {
        patient_id:"", 
        name:"", 
        address: "", 
        date_of_birth: "",
        telephon: "", 
        mobailphone: ""
    };

    add = (e) => {
        e.preventDefault();
        if(this.state.patient_id === "" || this.state.name === ""
        || this.state.bate_of_birth === "") {
            alert("All the fields are mandatory!")
            return;
        }
        this.props.addPatientHandler(this.state);
        this.setState({patient_id:"", name:"", address:"", date_of_birth:"", telephone:"", mobailphone:""});
        // this.props.history.push("/");
    };
    render() {
        return(
           <div className="ui main">
            <h2>Add Patient</h2>
            <form className="ui form" onSubmit={this.add}>
                <div className="field">
                    <label>Patient ID</label>
                    <input 
                    type="text" 
                    name="patient_id" 
                    placeholder="patient_id"
                    value={this.state.patient_id} 
                    onChange={(e)=>this.setState({patient_id: e.target.value})}> 
                    </input>
                </div>

                <div className="field">
                    <label>Name</label>
                    <input 
                    type="text" 
                    name="name" 
                    placeholder="name"
                    value={this.state.name} 
                    onChange={(e)=>this.setState({name: e.target.value})}>
                    </input>
                </div>

                <div className="field">
                    <label>Address</label>
                    <input 
                    type="text" 
                    name="address" 
                    placeholder="address"
                    value={this.state.address} 
                    onChange={(e)=>this.setState({address: e.target.value})}> 
                    </input>
                </div>

                <div className="field">
                    <label>Date Of Birth</label>
                    <input 
                    type="text" 
                    name="date_of_birth" 
                    placeholder="date_of_birth"
                    value={this.state.date_of_birth} 
                    onChange={(e)=>this.setState({date_of_birth: e.target.value})}> 
                    </input>
                </div>

                <div className="field">
                    <label>Telephone</label>
                    <input 
                    type="text" 
                    name="telephone" 
                    placeholder="telephone"
                    value={this.state.telephone} 
                    onChange={(e)=>this.setState({telephone: e.target.value})}>
                    </input>
                </div>

                <div className="field">
                    <label>Mobailphone</label>
                    <input 
                    type="text" 
                    name="mobailphone" 
                    placeholder="mobailphone"
                    value={this.state.mobailphone} 
                    onChange={(e)=>this.setState({mobailphone: e.target.value})}>      
                    </input>
                </div>

                <button className="ui button blue">Add</button>
            </form>
           </div> 
        );
    }
}

export default AddPatient;