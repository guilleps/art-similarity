import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const fetchSimilarityData = async (currentId?: string) => {
  const url = currentId
    ? `/get-session/?current_id=${currentId}`
    : `/get-session/`;

  const sessionRes = await axios.get(`${API_BASE}${url}`);
  const { comparison_id } = await sessionRes.data;
  
  const dataRes = await axios.get(`${API_BASE}/get-similarity/${comparison_id}/`);
  return dataRes.data;
};