import { useState } from "react";
import { apiFetch } from "./api";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";


function FlightsPage() {
    const [flights,setFlights] = useState([])
    const [error,setError] = useState("")
    const navigate = useNavigate()

    const displayFlights = async ()=>{
        const response = await apiFetch("/flights");
        if(response.ok){
            const data = await response.json()
            setFlights(data.data);
        }
    }

    useEffect(() => {
        displayFlights();
    },[]);

    const Logout = async() => {
            const response = await apiFetch("/logout")
            if(response.ok){
                localStorage.removeItem("token")
                navigate("/")
            }else{
                setError("Could not logout!")
            }
    }

    const GoToPilotsPage = () => {
        navigate("/pilots")
    }

    const GoToPlanesPage = () =>{
        navigate("/planes")
    }

    return (
        <div>
        <div>
        <h1>Flights</h1>
            <ul>
                {flights.map((flight) => (
                    <li key={flight.id}>{flight.pilot}- {flight.plane} - 
                    {flight.departure_time}- {flight.arrival_time} - 
                    {flight.departure_destination}- {flight.destination}
                    </li>
                ))}
                
            </ul>
        </div>

        <div>
            <button onClick={() => {
                Logout()
            }}>Logout</button>
            <p>{error}</p>
            <button onClick={() => {
                GoToPilotsPage()
            }}>Pilots Page</button>
            <button onClick={() => {
                GoToPlanesPage()
            }}>
                Planes Page
            </button>
        </div>
        </div>
    );
}

export default FlightsPage;
