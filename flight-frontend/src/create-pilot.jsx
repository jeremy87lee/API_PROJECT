import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import NavBar from "./navBar";

function CreatePilot(){
    const [name,setName] = useState("")
    const [msg,setMsg] = useState("")
    const navigate = useNavigate()

    const fetch = async(e) => {
        e.preventDefault()
        const response = await apiFetch("/create_pilot",{
            method: "POST",
            body: JSON.stringify({
                "name": name
            })
        })
        if(response.ok){
            navigate("/pilots")
        }
        const resp = await response.json()
        setMsg(resp.message)
    }

    return (
        <div>
            <NavBar />
            <div>
                <form onSubmit={fetch}>
                    <label>Name</label>
                    <input value={name} onChange={(e) => {setName(e.target.value)}}/>
                    <button type="submit">Submit</button>
                </form>
            </div>
            {msg && <p>{msg}</p>}
        </div>
    )
}
export default CreatePilot;