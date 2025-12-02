import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getAllSimilaritiesRaw } from '@/services/similarity.service';
import { SimilarityRaw, labelMap } from '@/types/similarity';

export type BoxRow = [string, number, number, number, number, number];

export type Extreme = {
	key: keyof SimilarityRaw;
	label: string;
	value: number;
};

function percentile(arr: number[], p: number): number {
	if (!arr.length) return 0;
	const idx = (arr.length - 1) * p;
	const lo = Math.floor(idx);
	const hi = Math.ceil(idx);
	if (lo === hi) return arr[lo];
	const h = idx - lo;
	return arr[lo] * (1 - h) + arr[hi] * h;
}

function computeFiveNumber(values: number[]): {
	min: number;
	q1: number;
	median: number;
	q3: number;
	max: number;
} {
	if (!values.length) {
		return { min: 0, q1: 0, median: 0, q3: 0, max: 0 };
	}
	const v = [...values].sort((a, b) => a - b);
	return {
		min: v[0],
		q1: percentile(v, 0.25),
		median: percentile(v, 0.5),
		q3: percentile(v, 0.75),
		max: v[v.length - 1],
	};
}

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

export function useBoxPlotResultsData() {
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

		const header: (string | number)[] = ['metric', 'min', 'Q1', 'median', 'Q3', 'max'];
		const rows: (string | number)[][] = [header];

		const baseKeys = Object.keys(labelMap) as Array<keyof typeof labelMap>;
		for (const base of baseKeys) {
			const tKey = (base + '_transformation') as keyof SimilarityRaw;
			const label = labelMap[base];
			const values: number[] = [];
			for (const row of data) {
				const v = row[tKey];
				if (typeof v === 'number' && !Number.isNaN(v)) values.push(v);
			}
			const { min, q1, median, q3, max } = computeFiveNumber(values);
			rows.push([label, min, q1, median, q3, max]);
		}

		return rows;
	}, [data]);

	return { data, isLoading, isError, results, extremes } as const;
}
