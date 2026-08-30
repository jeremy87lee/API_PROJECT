import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import NavBar from "./navBar";

function CreateGate(){
    const [terminal,setTerminal] = useState("")
    const [flightID,setFlightID] = useState()
    const navigate = useNavigate()
    const [msg,setMsg] = useState("")

    const fetch = async(e) => {
        e.preventDefault()
        const response = await apiFetch("/create_gate",{
            method:"POST",
            body: JSON.stringify({
                "terminal":terminal,
                "flight_id":flightID
            })
        })
        if(response.ok){
            alert("Gate created!")
            navigate("/gates")
        }else{
            const resp = await response.json()
            setMsg(resp.message)
        }
    }
    return(
        <div>
            <NavBar />
            <div>
                <form onSubmit={fetch}>
                    <label>Terminal</label>
                    <input value={terminal} onChange={(e) => {setTerminal(e.target.value)}}/>
                    <label>Flight ID</label>
                    <input value={flightID} onChange={(e) => {setFlightID(e.target.value)}}/>
                    <button type="submit">Submit</button>
                </form>
            </div>
            {msg && <p>{msg}</p>}
        </div>
    )
}
export default CreateGate;