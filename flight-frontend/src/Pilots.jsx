import { useEffect, useState } from "react";
import { apiFetch } from "./api";
import { useNavigate } from "react-router-dom";
import NavBar from "./navBar"

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

  

    return (
        <div>
            <NavBar />
            <h1>Pilots</h1>
            <ul>
            {pilots.map((pilot) => (
              <li>{pilot.id} - {pilot.name}</li>  
            ))}
            </ul>
        </div>

    )
}
export default PilotsPage;