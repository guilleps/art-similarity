import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import {
	getAllSimilarities,
	getAllSimilaritiesRaw,
	getSimilaritiesByTransform,
} from '@/services/similarity.service';

const transforms = [
	'color_heat_map',
	'tone',
	'saturation',
	'brightness',
	'texture',
	'contrast',
] as const;

export function usePrefetchResultsData() {
	const qc = useQueryClient();

	useEffect(() => {
		const staleTime = 5 * 60 * 1000; // 5 min en caché

		// Gráfico general
		qc.prefetchQuery({
			queryKey: ['similaritiesRaw'],
			queryFn: async () => (await getAllSimilaritiesRaw()).data,
			staleTime,
		});

		// Tabla (primera página)
		qc.prefetchQuery({
			queryKey: ['similarities', { page: 1, limit: 10 }],
			queryFn: () => getAllSimilarities(1, 10).then(r => r.data),
			staleTime,
		});

		// Cada transformación
		transforms.forEach(t =>
			qc.prefetchQuery({
				queryKey: ['transform', t],
				queryFn: () => getSimilaritiesByTransform(t),
				staleTime,
			}),
		);
	}, [qc]);
}
