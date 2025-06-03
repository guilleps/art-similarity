import axios from "axios";
import PaintingData from "@/types/painting";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function fetchSimilarityData(): Promise<PaintingData> {
  const random = await axios.get(`${API_BASE}/random-session/`);
  const comparisonId = random.data.comparison_id;

  const response = await axios.get(`${API_BASE}/get-similarity/${comparisonId}/`);
  return response.data;
}
