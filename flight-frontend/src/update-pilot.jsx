import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import NavBar from "./navBar";

function UpdatePilot(){
    const [name,setName] = useState("")
    const pilotId = localStorage.getItem("pilotId")
    const navigate = useNavigate()
    const [msg,setMsg] = useState("")

    const fetch = async(e) => {
        e.preventDefault()
        const response = await apiFetch(`/update_pilot/${pilotId}`,{
            method: "PUT",
            body: JSON.stringify({
                "name": name
            })
        })
        if(response.ok){
            navigate("/pilots")
            alert("Pilot updated!")
        }
        const js = response.json()
        setMsg(js.message)
    }

    return(
        <div>
            <NavBar />
            <div>
                <form onSubmit={fetch}>
                    <label>Name</label>
                    <input value={name} onChange={(e) => {setName(e.target.value)}}/>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    )
}
export default UpdatePilot;