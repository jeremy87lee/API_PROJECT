import { useEffect, useState } from "react";
import { apiFetch } from "./api";
import { useNavigate } from "react-router-dom";

function PilotsPage(){
    const navigate = useNavigate()
    const [pilots,setPilots] = useState([])

    const fetch = async() => {
        const response = await apiFetch("/pilots")
        if(response.ok){
            const data = await response.json()
            setPilots(data.data);
            console.log("good fetch")
        }
    }

    useEffect(() => {
        fetch();
    },[])

    const goBackToFlightsPage = () => {
        navigate("/flights")
    }

    return (
        <div>
            <h1>Pilots</h1>
            <ul>
            {pilots.map((pilot) => (
              <li>{pilot.id} - {pilot.name}</li>  
            ))}
            </ul>
            <button onClick={() => {
                goBackToFlightsPage()
            }}>Go Back To Flights Page</button>
        </div>

    )
}
export default PilotsPage;