import { useNavigate } from "react-router-dom";
import { useState,useEffect } from "react";
import { apiFetch } from "./api";
import NavBar from "./navBar";

function PlanesPage(){
    const [planes,setPlanes] = useState([])
    const Navigate = useNavigate()
    const [page,setPage] = useState(1)
    const [perPage,setPerpage] = useState(3)
    const [model,setModel] = useState("")
    const [totalPage,setTotalPage] = useState(1)
    const [sort,setSort] = useState("")
    const isAdmin = localStorage.getItem("isAdmin") == "true"

    const fetch = async() => {
        const params = new URLSearchParams()
        params.set("page",page)
        params.set("per_page",perPage)
        model && params.set("model",model)
        sort && params.set("sort",sort)

        const response = await apiFetch(`/planes?${params.toString()}`)
        if(response.ok){
            const data = await response.json()
            setPlanes(data.data)
            console.log("got planes yo")
            setTotalPage(data.total_pages)
        }
        if(response.status == 401){
            Navigate("/")
        }
    }

    const GoToCreatePlanePage = () => {
        Navigate("/create-plane")
    }

    const GoToUpdatePlanePage = (plane_id) => {
        localStorage.setItem("plane_id",plane_id)
        Navigate("/update-plane")
    }

    const DeletePlane = async(plane_id) => {
        const response = await apiFetch(`/delete_plane/${plane_id}`,{
            method: "DELETE"})
        if(response.ok){
            alert(`plane ${plane_id} deleted!`)
            fetch()
        }else{
            alert("Plane could not be deleted!")
        }
    }

    useEffect(() => {
        fetch()
    },[sort,model,page])

 

    return (
        <div>
            <NavBar />
            <h1>Planes</h1>
            <div>
                <input placeholder="Filter by model" value={model} onChange={(e) => {setPage(1);setModel(e.target.value)}}/>
            </div>
            <div>
                <select value={sort} onChange={(e) =>{setPage(1);setSort(e.target.value)}}>
                    <option value="capacity">Capacity(ascending)</option>
                    <option value="-capacity">Capacity(descending)</option>
                    <option value="">No Sort</option>
                </select>
            </div>
            <ul>
            {planes.map((plane) => (
                <li>Plane number: {plane.id} - Plane model: {plane.model} - Plane capacity: {plane.capacity}
                { isAdmin && <button onClick={() => {GoToUpdatePlanePage(plane.id)}}>Update</button>}
                {isAdmin && <button onClick={() => {DeletePlane(plane.id)}}>Delete</button>}</li>
            ))}
            </ul>
            {isAdmin && <button onClick={() => {GoToCreatePlanePage()}}>Create Plane</button>}
            <div>
                <button disabled = {page <= 1} onClick={() => {setPage(page-1)}} >Previous</button>
                <span>page {page} of {totalPage}</span>
                <button disabled = {page >= totalPage} onClick={() => {setPage(page+1)}}>Next</button>
            </div>
        </div>
    )
}
export default PlanesPage;