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

    const [destination,setDestination] = useState("")
    const [page,setPage] = useState(1)
    const [perPage,setPerPage] = useState(3)
    const [sort,setSort] = useState("")
    const [totalPages,setTotalPages] = useState(1)

    const displayFlights = async ()=>{
        const params = new URLSearchParams();
        params.set("page",page);
        params.set("per_page",perPage)
        destination && params.set("destination",destination)
        sort && params.set("sort",sort)
        const response = await apiFetch(`/flights?${params.toString()}`);
        if(response.ok){
            const data = await response.json()
            setFlights(data.data);
            setTotalPages(data.total_pages)
        }
        if(response.status == 401){
            navigate("/")
        }
    }

    useEffect(() => {
        displayFlights();
    },[sort,destination,page]);

    const Logout = async() => {
            const response = await apiFetch("/logout")
            if(response.ok){
                localStorage.removeItem("token")
                navigate("/")
            }else{
                setError("Could not logout!")
            }
    }

    const GoToUpdateFlightPage = (flight_id) => {
        localStorage.setItem("flight_id",flight_id)
        navigate("/update-flight")
    }

    const DeleteFlight = async(flight_id) => {
        const baseURL = "delete_flight"
        const response = await apiFetch(`/${baseURL}/${flight_id}`,{
            method: "DELETE"
        })
        if(response.ok){
            displayFlights()
        }else{
            setError("Could not delete!")
        }
    }

    return (
        <div>
        <div>
        <NavBar />
        <h1>Flights</h1>
        {isAdmin && <h2>Welcome Admin!</h2>}
        {!isAdmin && <h2>Welcome User!</h2>}

        <div>
            <input placeholder="Filter by Destination" value={destination} onChange={(e) => {setPage(1); setDestination(e.target.value)}}/>
        </div>
        <div>
            <select value={sort} onChange={(e) => {setPage(1); setSort(e.target.value)}}>
                <option value="">No Sort</option>
                <option value="departure_time">Departure time(earliest)</option>
                <option value="-departure_time">Departure time(latest)</option>
            </select>
        </div>

            <ul>
                {flights.map((flight) => (
                    <li key={flight.id}>{flight.pilot}- {flight.plane} - 
                    {flight.departure_time}- {flight.arrival_time} - 
                    {flight.departure_destination}- {flight.destination}
                    {isAdmin && <button onClick={() => {GoToUpdateFlightPage(flight.id)}}>Update Flight</button>}
                    {isAdmin && <button onClick={() => {DeleteFlight(flight.id)}}>Delete Flight</button>}
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
        
        <div>
            <button disabled={page <= 1} onClick={() => {setPage(page-1)}}>Previous</button>
            <span>Page {page} of {totalPages}</span>
            <button disabled={page >= totalPages} onClick={() => {setPage(page+1)}}>Next</button>
        </div>
        </div>
    );
}

export default FlightsPage;
