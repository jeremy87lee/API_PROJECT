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

        const dateTimePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]) ([01]\d|2[0-3]):[0-5]\d:[0-5]\d$/;
        if (!dateTimePattern.test(departureTime) || !dateTimePattern.test(arrivalTime)){
            setMsg("Please enter a date and time in the format 2026-12-12 10:00:00")
            return None;
        }

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
            if(resp.message == "Missing flight data! Could not be created!"){
                setMsg(resp.message)
            }else{
                setMsg(resp.message + " There might be a time clash or incorrect ID input!")
            }
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