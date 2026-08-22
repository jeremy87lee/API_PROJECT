import { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";

function GatesPage(){
    const navigate = useNavigate()
    const [gates,setGates] = useState([])

    const fetch = async() => {
        const response = await apiFetch("/gates")
        if(response.ok){
            const data = await response.json()
            setGates(data.data)
            console.log("good fetch")
        }
    }

    useEffect(() => {
        fetch()
    },[]);

    const GoBackToFlightsPage = () => {
        navigate("/flights")
    }

    return(
        <div>
            <ul>
                {gates.map((gate) => (
                    <li>Gate number {gate.id} - Gate terminal {gate.terminal} - Gate flight {gate.flight} </li>
                ))}
            </ul>
            <button onClick={() => {
                GoBackToFlightsPage()
            }}>Go Back To Flights Page</button>
        </div>
    );
}
export default GatesPage;