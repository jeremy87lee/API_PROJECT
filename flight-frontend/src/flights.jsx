import { useState } from "react";
import { apiFetch } from "./api";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import NavBar from "./navBar";


function FlightsPage() {
    const [flights,setFlights] = useState([])
    const [error,setError] = useState("")
    const navigate = useNavigate()
    const isAdmin = localStorage.getItem("isAdmin") == "true";

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


    return (
        <div>
        <div>
        <NavBar />
        <h1>Flights</h1>
        {isAdmin && <h2>Welcome Admin!</h2>}
        {!isAdmin && <h2>Welcome User!</h2>}
            <ul>
                {flights.map((flight) => (
                    <li key={flight.id}>{flight.pilot}- {flight.plane} - 
                    {flight.departure_time}- {flight.arrival_time} - 
                    {flight.departure_destination}- {flight.destination}
                    {isAdmin && <button>Hi</button>}
                    </li>
                ))}                
            </ul>
        </div>
        {isAdmin && <button onClick={() => {navigate("/create-flight")}}>Create Flight</button>}
        <div>
            <button onClick={() => {
                Logout()
            }}>Logout</button>
            <p>{error}</p>
            
        </div>
        </div>
    );
}

export default FlightsPage;
