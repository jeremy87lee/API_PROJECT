import { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import NavBar from "./navBar";

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



    return(
        <div>
            <NavBar />
            <ul>
                {gates.map((gate) => (
                    <li>Gate number {gate.id} - Gate terminal {gate.terminal} - Gate flight {gate.flight} </li>
                ))}
            </ul>
        </div>
    );
}
export default GatesPage;