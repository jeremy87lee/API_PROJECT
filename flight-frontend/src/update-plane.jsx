import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import NavBar from "./navBar";

function UpdatePlane(){
    const [model,setModel] = useState("")
    const [capacity,setCapacity] = useState(1)
    const plane_id = localStorage.getItem("plane_id")
    const navigate = useNavigate()
    const [msg,setMsg] = useState("")

    const fetch = async(e) => {
        e.preventDefault()
        const response = await apiFetch(`/update_plane/${plane_id}`,{
            method: "PUT",
            body: JSON.stringify({
                "model":model,
                "capacity":capacity
            })
        })
        if(response.ok){
            alert(`Plane ${plane_id} updated!`)
            navigate("/planes")
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
                    <label>Model</label>
                    <input value={model} onChange={(e) => {setModel(e.target.value)}}/>
                    <label>Capacity</label>
                    <input value={capacity} onChange={(e) => {setCapacity(e.target.value)}}/>
                    <button type="submit">Submit</button>
                </form>
                {msg && <p>{msg}</p>}
            </div>
        </div>
    )
}
export default UpdatePlane;