import { useNavigate } from "react-router-dom";

function navBar(){
    const navigate = useNavigate()
    
    return (
        <div class="nav">
            <button onClick={()=> {
                navigate("/flights")
            }}>Flights</button>
            <button onClick={()=> {
                navigate("/pilots")
            }}>Pilots</button>
            <button onClick={() => {
                navigate("/planes")
            }}>Planes</button>
            <button onClick={() => {navigate("/gates")}}>Gates</button>
        </div>
    )
}
export default navBar;