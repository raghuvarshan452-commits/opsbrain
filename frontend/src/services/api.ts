import axios from "axios";
 
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});
 
export const checkHealth = () => api.get("/health");
export const checkDbHealth = () => api.get("/db-health");
 
export default api;
