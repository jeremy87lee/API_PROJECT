import { useEffect, useState } from "react";
import { apiFetch } from "./api";
import { useNavigate } from "react-router-dom";
import NavBar from "./navBar"

function PilotsPage(){
    const navigate = useNavigate()
    const [pilots,setPilots] = useState([])
    const [page,setPage] = useState(1)
    const [perPage,setPerPage] = useState(3)
    const [totalPages,setTotalPages] = useState(1)
    const [sort,setSort] = useState("")
    const isAdmin = localStorage.getItem("isAdmin") == "true"

    const fetch = async() => {
        const params = new URLSearchParams()
        params.set("page",page)
        params.set("per_page",perPage)
        sort && params.set("sort",sort)
        const response = await apiFetch(`/pilots?${params.toString()}`)
        if(response.ok){
            const data = await response.json()
            setPilots(data.data);
            console.log("good fetch")
            setTotalPages(data.total_pages)
        }
        if(response.status == 401){
            navigate("/")
        }
    }

    useEffect(() => {
        fetch();
    },[sort,page])

    const GoToCreatePilot = () => {
        navigate("/create-pilot")
    }

    const GoToUpdatePilotPage = (pilot_id) => {
        localStorage.setItem("pilotId",pilot_id)
        navigate("/update-pilot")
    }

    const DeletePilot = async(pilot_id) => {
        const response = await apiFetch(`/delete_pilot/${pilot_id}`,{
            method: "DELETE"
        })
        if(response.ok){
            fetch()
            alert("Pilot "+pilot_id+" deleted!")
        }else{
            alert("Pilot "+pilot_id+" could not be deleted!")    
        }
    }

    return (
        <div>
            <NavBar />
            <h1>Pilots</h1>
            <div>
                <select value={sort} onChange={(e) => {setPage(1);setSort(e.target.value)}}>
                    <option value="">No Sort</option>
                    <option value="name">Name (ascending)</option>
                    <option value="-name">Name (descending)</option>
                </select>
            </div>
            <ul>
            {pilots.map((pilot) => (
              <li>{pilot.id} - {pilot.name} 
              {isAdmin && <button onClick={() => {GoToUpdatePilotPage(pilot.id)}}>Update</button>}
              {isAdmin && <button onClick={() => {DeletePilot(pilot.id)}}>Delete</button>}
              </li>  
            ))}
            </ul>
            <div>
                {isAdmin && <button onClick={() => {GoToCreatePilot()}}>Create Pilot</button>}
            </div>
            <div>
                <button disabled={page <= 1} onClick={() => {setPage(page-1)}}>Previous</button>
                <span>page {page} of {totalPages}</span>
                <button disabled= {page >= totalPages} onClick={() => {setPage(page+1)}}>Next</button>
            </div>
        </div>

    )
}
export default PilotsPage;