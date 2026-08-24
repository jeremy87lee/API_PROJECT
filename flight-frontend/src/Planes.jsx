import { useNavigate } from "react-router-dom";
import { useState,useEffect } from "react";
import { apiFetch } from "./api";
import NavBar from "./navBar";

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
        if(response.status == 401){
            Navigate("/")
        }
    }

    useEffect(() => {
        fetch()
    },[])

 

    return (
        <div>
            <NavBar />
            <h1>Planes</h1>
            <ul>
            {planes.map((plane) => (
                <li>Plane number: {plane.id} - Plane model: {plane.model} - Plane capacity: {plane.capacity}</li>
            ))}
            </ul>
        </div>
    )
}
export default PlanesPage;