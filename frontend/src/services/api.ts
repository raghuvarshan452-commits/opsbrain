import axios from "axios";
 
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});
export const uploadDocument = (file: File) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

 
export const checkHealth = () => api.get("/health");
export const checkDbHealth = () => api.get("/db-health");
export const listDocuments = () => api.get("/documents");
 
export default api;
