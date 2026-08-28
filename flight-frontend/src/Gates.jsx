import { useState } from "react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";
import NavBar from "./navBar";

function GatesPage(){
    const navigate = useNavigate()
    const [gates,setGates] = useState([])
    const [page,setPage] = useState(1)
    const [perPage,setPerPage] = useState(3)
    const [totalPages,setTotalPages] = useState(1)
    const [sort,setSort] = useState("")
    const isAdmin = localStorage.getItem("isAdmin") == "true"

    const fetch = async() => {
        const params = new URLSearchParams()
        params.set("page",page)
        params.set("per_page",perPage)
        params.set("Sort",sort) && sort
        const response = await apiFetch(`/gates?${params.toString()}`)
        if(response.ok){
            const data = await response.json()
            setGates(data.data)
            setTotalPages(data.total_pages)
            console.log("good fetch")
        }
        if(response.status == 401){
            navigate("/")
        }
    }

    useEffect(() => {
        fetch()
    },[page,sort]);



    return(
        <div>
            <NavBar />
            <div>
                <select value={sort} onChange={(e) => {setPage(1);setSort(e.target.value)}}>
                    <option value="">No Sort</option>
                    <option value="terminal">Terminal (ascending)</option>
                    <option value="-terminal">Terminal (descending)</option>
                </select>
            </div>
            <ul>
                {gates.map((gate) => (
                    <li>Gate number {gate.id} - Gate terminal {gate.terminal} - Gate flight {gate.flight} </li>
                ))}
            </ul>
            <div>
                {isAdmin && <button onClick={() => {navigate("/create-gate")}}>Create Gate</button>}
            </div>
            <div>
                <button disabled={page <= 1} onClick={() => {setPage(page-1)}}>Previous</button>
                <spam>page {page} of {totalPages}</spam>
                <button disabled={page >= totalPages} onClick={() => {setPage(page+1)}}>Next</button>
            </div>
        </div>
    );
}
export default GatesPage;