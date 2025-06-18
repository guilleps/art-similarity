import { SimilarityRaw } from "@/pages/resultados/GeneralResult";
import axios, { AxiosResponse } from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const getAllSimilarities = async (page = 1, limit = 10) => {
    const response = await axios.get(`${API_BASE}/get-all-similarities/`, {
        params: { page, limit }
    });
    return response;
};

export const getAllSimilaritiesRaw = async (): Promise<AxiosResponse<SimilarityRaw[]>> => {
   return axios.get(`${API_BASE}/get-all-similarities/raw/`);
};

export const getSimilaritiesByTransform = async (transform: string) => {
    const response = await axios.get(`${API_BASE}/get-similarity-by-transform/`, {
        params: { transform }
    });
    return response.data;
};

export const getSimilaritiesById = async (comparison_id: string) => {
    const response = await axios.get(`${API_BASE}/get-similarity/${comparison_id}/`);
    return response.data;
};