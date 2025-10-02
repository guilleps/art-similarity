import { ExportedSimilarityData } from '@/dto/similarity-export.dto';
import { SimilarityRaw } from '@/types/similarity';
import axios, { AxiosResponse } from 'axios';
import { getAllSimilaritiesMocks } from './mocks/getAllSimilarities.mock';
import { getAllSimilaritiesRawMocks } from './mocks/getAllSimilaritiesRaw.mock';
import { getSimilaritiesByIdMocks } from './mocks/getSimilaritiesById.mock';
import {
	getSimilaritiesByTransformToneMocks,
	getSimilaritiesByTransformColorHeatMapMocks,
	getSimilaritiesByTransformSaturationMocks,
	getSimilaritiesByTransformBrightnessMocks,
	getSimilaritiesByTransformTextureMocks,
	getSimilaritiesByTransformContrastMocks,
} from './mocks/getSimilaritiesByTransform.mock';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const ENVIRONMENT = import.meta.env.VITE_ENVIRONMENT;

export const getAllSimilarities = async (page = 1, limit = 10) => {
	if (ENVIRONMENT === 'development') return getAllSimilaritiesMocks();

	const response = await axios.get(`${API_BASE}/get-all-similarities/`, {
		params: { page, limit },
	});
	return response;
};

export const getAllSimilaritiesRaw = async (): Promise<AxiosResponse<SimilarityRaw[]>> => {
	if (ENVIRONMENT === 'development') return getAllSimilaritiesRawMocks();

	return axios.get(`${API_BASE}/get-all-similarities/raw/`);
};

export const getSimilaritiesByTransform = async (transform: string) => {
	if (ENVIRONMENT === 'development') {
		const t = (transform || '').toLowerCase();
		if (t === 'tone') return getSimilaritiesByTransformToneMocks;
		if (t === 'color_heat_map' || t === 'color-heat-map') {
			return getSimilaritiesByTransformColorHeatMapMocks;
		}
		if (t === 'saturation') return getSimilaritiesByTransformSaturationMocks;
		if (t === 'brightness') return getSimilaritiesByTransformBrightnessMocks;
		if (t === 'texture') return getSimilaritiesByTransformTextureMocks;
		if (t === 'contrast') return getSimilaritiesByTransformContrastMocks;
		return [];
	}

	const response = await axios.get(`${API_BASE}/get-similarity-by-transform/`, {
		params: { transform },
	});
	return response.data;
};

export const getSimilaritiesById = async (comparison_id: string) => {
	if (ENVIRONMENT === 'development') {
		const response = await getSimilaritiesByIdMocks(comparison_id);
		return response.data;
	}
	const response = await axios.get(`${API_BASE}/get-similarity/${comparison_id}/`);
	return response.data;
};

export const getExportedSimilarityData = async (
	format: 'json' | 'csv' = 'json',
): Promise<AxiosResponse<ExportedSimilarityData>> => {
	if (ENVIRONMENT === 'development') {
		return {
			data: {
				// estructura mínima para evitar romper la UI; ajusta según tu dto
				generated_at: new Date().toISOString(),
				rows: [],
			} as unknown as ExportedSimilarityData,
			status: 200,
			statusText: 'OK',
			headers: {},
			config: {},
		} as AxiosResponse<ExportedSimilarityData>;
	}

	const response = await axios.get(`${API_BASE}/export-similarity-results/${format}/`, {
		responseType: format === 'json' ? 'json' : 'blob',
	});
	return response;
};
