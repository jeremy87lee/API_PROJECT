import { useState } from "react";
import NavBar from "./navBar";
import { apiFetch } from "./api";
import { useNavigate } from "react-router-dom";

function CreatePlane(){
    const [model,setModel] = useState("")
    const [capacity,setCapacity] = useState(1)
    const navigate = useNavigate()
    const [msg,setMsg] = useState("")

    const fetch = async(e) => {
        e.preventDefault()
        const response = await apiFetch("/create_plane",{
            method: "POST",
            body: JSON.stringify({
                "model": model,
                "capacity":capacity
            })
        })
        if(response.ok){
            alert("Plane created!")
            navigate("/planes")
        }else{
            const resp = await response.json()
            setMsg(resp.message)
        }
    }


    return (
        <div>
            <NavBar />
            <div>
                <form onSubmit={fetch}>

                    <label>Model</label>
                    <input value={model} onChange={(e) => {setModel(e.target.value)}}/>

                    <label>Capacity</label>
                    <input value={capacity} onChange={(e) => {setCapacity(e.target.value)}}/>

                    <button type="submit">Submit</button>
                </form>
            </div>
            {msg && <p>{msg}</p>}
        </div>
    )
}
export default CreatePlane;