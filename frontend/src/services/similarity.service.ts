// src/services/similarity.service.ts
import { ExportedSimilarityData } from '@/dto/similarity-export.dto';
import { SimilarityRaw } from '@/pages/resultados/GeneralResult';
import axios, { AxiosResponse } from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
const USE_MOCK = String(import.meta.env.VITE_USE_MOCK).toLowerCase() === 'true';

/** ======================
 *  Tipos basados en data.json
 *  ====================== */
type ParMetric = { files?: { image_1?: string; image_2?: string }; similarity?: number };
type ParEntry = {
	image_1?: string;
	image_2?: string;
	texture?: ParMetric;
	contrast?: ParMetric;
	hsv_hue?: ParMetric;
	hsv_saturation?: ParMetric;
	hsv_value?: ParMetric;
	heat_color_map?: ParMetric;
};
type DataJson = { par: Record<string, ParEntry> };

/** ======================
 * Helpers MOCK
 * ====================== */
const tMap = {
	// UI / endpoints  ->  JSON keys
	color_heat_map: 'heat_color_map',
	tone: 'hsv_hue',
	saturation: 'hsv_saturation',
	brightness: 'hsv_value',
	texture: 'texture',
	contrast: 'contrast',
} as const;

const rawKey = {
	color_heat_map: 'color_heat_map_transformation',
	tone: 'tone_transformation',
	saturation: 'saturation_transformation',
	brightness: 'brightness_transformation',
	texture: 'texture_transformation',
	contrast: 'contrast_transformation',
} as const;

async function loadJson(): Promise<DataJson> {
	const res = await fetch('/data.json');
	if (!res.ok) throw new Error(`No se pudo leer /data.json (${res.status})`);
	return res.json();
}

function toSimilarityRawArray(json: DataJson): (SimilarityRaw & { comparison_id: string })[] {
	// Ordenamos por número de par
	const entries = Object.entries(json.par).sort(([a], [b]) => Number(a) - Number(b));
	return entries.map(([par, p]) => ({
		// Sufijo *_transformation para tu clase SimilarityRaw
		color_heat_map_transformation: p.heat_color_map?.similarity ?? null,
		tone_transformation: p.hsv_hue?.similarity ?? null,
		saturation_transformation: p.hsv_saturation?.similarity ?? null,
		brightness_transformation: p.hsv_value?.similarity ?? null,
		texture_transformation: p.texture?.similarity ?? null,
		contrast_transformation: p.contrast?.similarity ?? null,
		// Usamos el índice de par como comparison_id mock (string)
		comparison_id: String(par),
	}));
}

/** ======================
 * Endpoints
 * ====================== */

export const getAllSimilarities = async (page = 1, limit = 10) => {
	if (USE_MOCK) {
		const json = await loadJson();
		const rows = toSimilarityRawArray(json);

		const start = (page - 1) * limit;
		const end = start + limit;

		const paged = rows.slice(start, end).map(r => ({
			// Shape que TableResults usa:
			color_heat_map_transformation: r.color_heat_map_transformation,
			tone_transformation: r.tone_transformation,
			saturation_transformation: r.saturation_transformation,
			brightness_transformation: r.brightness_transformation,
			texture_transformation: r.texture_transformation,
			contrast_transformation: r.contrast_transformation,
			comparison_id: r.comparison_id,
		}));

		const mockResponse = {
			data: {
				results: paged,
				count: rows.length,
				page,
				limit,
			},
			status: 200,
			statusText: 'OK',
			headers: {},
			config: {},
		} as AxiosResponse<any>;

		return mockResponse;
	}

	const response = await axios.get(`${API_BASE}/get-all-similarities/`, {
		params: { page, limit },
	});
	return response;
};

// en src/services/similarity.service.ts
export const getAllSimilaritiesRaw = async (): Promise<SimilarityRaw[]> => {
	if (USE_MOCK) {
		const json = await loadJson();
		// Reusamos tu helper para llevar data.json -> SimilarityRaw[]
		return toSimilarityRawArray(json).map(({ comparison_id, ...rest }) => rest);
	}
	const { data } = await axios.get(`${API_BASE}/get-all-similarities/raw/`);
	return data; // devolvemos el array directo también en la rama real
};

export const getSimilaritiesByTransform = async (transform: string) => {
	if (USE_MOCK) {
		const json = await loadJson();
		const key = tMap[transform as keyof typeof tMap];
		if (!key) return [];

		// Devolvemos [{par, value}] que tu TransformChart ya espera
		const data = Object.entries(json.par)
			.sort(([a], [b]) => Number(a) - Number(b))
			.map(([par, p]) => ({
				par: Number(par),
				value: (p as any)[key]?.similarity ?? null,
			}));

		return data;
	}

	const response = await axios.get(`${API_BASE}/get-similarity-by-transform/`, {
		params: { transform },
	});
	return response.data;
};

export const getSimilaritiesById = async (comparison_id: string) => {
	if (USE_MOCK) {
		const json = await loadJson();
		const p = json.par?.[comparison_id];
		if (!p) return null;

		// Construimos PaintingData (shape que tu app usa)
		const toImg = (url?: string) => ({
			original_image: url ?? '',
			transformations: {
				// Para cada transform, devolvemos una mini estructura con image_transformed
				color_heat_map: { image_transformed: p.heat_color_map?.files?.image_1 ?? '' },
				tone: { image_transformed: p.hsv_hue?.files?.image_1 ?? '' },
				saturation: { image_transformed: p.hsv_saturation?.files?.image_1 ?? '' },
				brightness: { image_transformed: p.hsv_value?.files?.image_1 ?? '' },
				texture: { image_transformed: p.texture?.files?.image_1 ?? '' },
				contrast: { image_transformed: p.contrast?.files?.image_1 ?? '' },
			},
		});

		const image_1 = toImg(p.image_1);
		const image_2 = {
			original_image: p.image_2 ?? '',
			transformations: {
				color_heat_map: { image_transformed: p.heat_color_map?.files?.image_2 ?? '' },
				tone: { image_transformed: p.hsv_hue?.files?.image_2 ?? '' },
				saturation: { image_transformed: p.hsv_saturation?.files?.image_2 ?? '' },
				brightness: { image_transformed: p.hsv_value?.files?.image_2 ?? '' },
				texture: { image_transformed: p.texture?.files?.image_2 ?? '' },
				contrast: { image_transformed: p.contrast?.files?.image_2 ?? '' },
			},
		};

		const similitud = {
			color_heat_map: { similarity: p.heat_color_map?.similarity ?? 0 },
			tone: { similarity: p.hsv_hue?.similarity ?? 0 },
			saturation: { similarity: p.hsv_saturation?.similarity ?? 0 },
			brightness: { similarity: p.hsv_value?.similarity ?? 0 },
			texture: { similarity: p.texture?.similarity ?? 0 },
			contrast: { similarity: p.contrast?.similarity ?? 0 },
		};

		const total = Object.keys(json.par).length;
		const current_index = Number(comparison_id) - 1;

		const paintingData = {
			comparison_id,
			image_1,
			image_2,
			similitud,
			total,
			current_index,
		};

		return paintingData;
	}

	const response = await axios.get(`${API_BASE}/get-similarity/${comparison_id}/`);
	return response.data;
};

export const getExportedSimilarityData = async (): Promise<ExportedSimilarityData> => {
	if (USE_MOCK) {
		const json = await loadJson();
		return json as any; // devolvemos el JSON directo
	}
	const { data } = await axios.get(`${API_BASE}/export-similarity-results/`);
	return data; // normalizamos: devolvemos data también en la rama real
};
