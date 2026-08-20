import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "./api";

function LoginPage(){
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        const response = await apiFetch("/login",{
            method: "POST",
            body: JSON.stringify({username,password}),
        });

        if(response.ok){
            const data = await response.json();
            localStorage.setItem("token",data.access_token);
            navigate("/flights");
        }else{
            setError("Invalid username or password");
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>Username</label>
                <input value={username} onChange={(e) => setUsername(e.target.value)}/>

                <label>Password</label>
                <input value={password} onChange={(e) => setPassword(e.target.value)}/>

                {error && <p style={{color:"red"}}>{error}</p>}
                <button type="submit">Login</button>
            </form>
        </div>
    )

}
export default LoginPage;
