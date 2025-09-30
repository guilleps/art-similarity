import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getAllSimilaritiesRaw } from '@/services/similarity.service';
import { SimilarityRaw, labelMap } from '@/types/similarity';

export type Extreme = {
	key: keyof SimilarityRaw;
	label: string;
	value: number;
};

export function computeExtremes(data: SimilarityRaw[] | undefined): {
	max?: Extreme;
	min?: Extreme;
} {
	if (!data || data.length === 0) return {};

	const baseKeys = Object.keys(labelMap) as Array<keyof typeof labelMap>;
	let max: Extreme | undefined;
	let min: Extreme | undefined;

	for (const base of baseKeys) {
		const tKey = (base + '_transformation') as keyof SimilarityRaw;
		const label = labelMap[base];
		for (const row of data) {
			const v = row[tKey];
			if (typeof v === 'number' && !Number.isNaN(v)) {
				if (max === undefined || v > max.value) max = { key: tKey, label, value: v };
				if (min === undefined || v < min.value) min = { key: tKey, label, value: v };
			}
		}
	}

	return { max, min };
}

export function useGeneralResultsData() {
	const { data, isLoading, isError } = useQuery<SimilarityRaw[]>({
		queryKey: ['similaritiesRaw'],
		queryFn: async () => (await getAllSimilaritiesRaw()).data,
		staleTime: 5 * 60 * 1000,
		refetchOnMount: false,
		refetchOnWindowFocus: false,
	});

	const extremes = useMemo(() => computeExtremes(data), [data]);

	const results = useMemo<(string | number)[][]>(() => {
		if (!data || !data.length) return [];

		const rows: (string | number)[][] = [
			['par', 'color_heat_map', 'tone', 'saturation', 'brightness', 'texture', 'contrast'],
		];

		data.forEach((item: SimilarityRaw, index: number) => {
			rows.push([
				(index + 1).toString(),
				item.color_heat_map_transformation ?? null,
				item.tone_transformation ?? null,
				item.saturation_transformation ?? null,
				item.brightness_transformation ?? null,
				item.texture_transformation ?? null,
				item.contrast_transformation ?? null,
			]);
		});

		return rows;
	}, [data]);

	return { data, isLoading, isError, results, extremes } as const;
}
