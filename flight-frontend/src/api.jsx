const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8080/api";
export async function apiFetch(endpoint,options={}){
    const token = localStorage.getItem("token");
    const headers = {
        "Content-Type": "application/json",
        ...(token && {Authorization: `Bearer ${token}`}),
        ...options.headers,
    };
    const response = await fetch(`${API_BASE}${endpoint}`,{
        ...options,
        headers,
    });
    return response
}