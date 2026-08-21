import { useNavigate } from "react-router-dom";
import { useState,useEffect } from "react";
import { apiFetch } from "./api";

function PlanesPage(){
    const [planes,setPlanes] = useState([])
    const Navigate = useNavigate()

    const fetch = async() => {
        const response = await apiFetch("/planes")
        if(response.ok){
            const data = await response.json()
            setPlanes(data.data)
            console.log("got planes yo")
        }
    }

    useEffect(() => {
        fetch()
    },[])

    const goBackToFlightsPage = () => {
        Navigate("/flights")
    }

    return (
        <div>
            <h1>Planes</h1>
            <ul>
            {planes.map((plane) => (
                <li>Plane number: {plane.id} - Plane model: {plane.model} - Plane capacity: {plane.capacity}</li>
            ))}
            </ul>
            <button onClick={() => {
                goBackToFlightsPage()
            }}>
                Back to Flights Page
            </button>
        </div>
    )
}
export default PlanesPage;