import { useState } from "react";
import NavBar from "./navBar";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import { useEffect } from "react";

function createFlight(){
    const [pilotID,setPilot] = useState("")
    const [planeID,setPlane] = useState("")
    const [departureTime,setDepTime] = useState("")
    const [arrivalTime,setArrTime] = useState("")
    const [departureDestination,setDep] = useState("")
    const [destination,setDest] = useState("")
    const [msg,setMsg] = useState("")
    const navigate = useNavigate()

    const fetch = async (e) => {
        e.preventDefault()
        const response = await apiFetch("/create_flight",{
            method: "POST",
            body: JSON.stringify({
                departure_time: departureTime,
                arrival_time: arrivalTime,
                plane_id: planeID,
                pilot_id: pilotID,
                departure_destination: departureDestination,
                arrival_destination: destination
            })
        })
        if(response.ok){
            setMsg("Flight created!")
            console.log("good")
            navigate("/flights")
        }else{
            const resp = await response.json()
            setMsg(resp.message)
            console.log("bad")
        }
    }

    

    return (
        <div>
            <NavBar />
            <form onSubmit={fetch}>
                <label>Pilot ID</label>
                <input value={pilotID} onChange={(e) => setPilot(e.target.value)}/>
                <label>Plane ID</label>
                <input value={planeID} onChange={(e) => setPlane(e.target.value)}/>
                <label>Departure Time</label>
                <input value={departureTime} onChange={(e) => setDepTime(e.target.value)}/>
                <label>Arrival Time</label>
                <input value={arrivalTime} onChange={(e) => setArrTime(e.target.value)}/>
                <label>Departure Destination</label>
                <input value={departureDestination} onChange={(e) => setDep(e.target.value)}/>
                <label>Destination</label>
                <input value={destination} onChange={(e) => setDest(e.target.value)}/>

                <button type="submit">Submit</button>
            </form>
            {msg && <p>{msg}</p>}
        </div>
    )
}
export default createFlight;