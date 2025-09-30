export interface SimilarityRaw {
	color_heat_map_transformation: number | null;
	tone_transformation: number | null;
	saturation_transformation: number | null;
	brightness_transformation: number | null;
	texture_transformation: number | null;
	contrast_transformation: number | null;
}

export const labelMap: Record<string, string> = {
	color_heat_map: 'Mapa de calor',
	tone: 'Tono',
	saturation: 'Saturación',
	brightness: 'Brillo',
	texture: 'Textura',
	contrast: 'Contraste',
};
