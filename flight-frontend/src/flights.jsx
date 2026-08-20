import { useState } from "react";
import { apiFetch } from "./api";
import { useEffect } from "react";

function FlightsPage() {
    const [flights,setFlights] = useState([])

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

    return (
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
    );
}

export default FlightsPage;
