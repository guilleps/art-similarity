import { getAllSimilaritiesRaw } from '@/services/similarity.service';
import * as echarts from 'echarts';
import { useEffect, useMemo, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { CardValue } from '@/components/CardValue';

const labelMap: Record<string, string> = {
	color_heat_map: 'Mapa de calor',
	tone: 'Tono',
	saturation: 'Saturación',
	brightness: 'Brillo',
	texture: 'Textura',
	contrast: 'Contraste',
};

export class SimilarityRaw {
	color_heat_map_transformation: number | null;
	tone_transformation: number | null;
	saturation_transformation: number | null;
	brightness_transformation: number | null;
	texture_transformation: number | null;
	contrast_transformation: number | null;
}

type Extreme = {
	key: keyof SimilarityRaw;
	label: string;
	value: number;
};

function computeExtremes(data: SimilarityRaw[] | undefined): { max?: Extreme; min?: Extreme } {
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

export const GeneralResult = () => {
	const chartRef = useRef<HTMLDivElement>(null);
	const {
		data: rawData,
		isLoading,
		isError,
	} = useQuery<SimilarityRaw[]>({
		queryKey: ['similaritiesRaw'],
		queryFn: async () => (await getAllSimilaritiesRaw()).data,
		staleTime: 5 * 60 * 1000,
		refetchOnMount: false,
		refetchOnWindowFocus: false,
	});

	const extremes = useMemo(() => computeExtremes(rawData), [rawData]);

	useEffect(() => {
		const chartDom = chartRef.current;
		if (!chartDom) return;

		if (!rawData || !rawData.length) return;

		const results: (string | number)[][] = [
			['par', 'color_heat_map', 'tone', 'saturation', 'brightness', 'texture', 'contrast'],
		];

		rawData.forEach((item: SimilarityRaw, index: number) => {
			results.push([
				(index + 1).toString(),
				item.color_heat_map_transformation ?? null,
				item.tone_transformation ?? null,
				item.saturation_transformation ?? null,
				item.brightness_transformation ?? null,
				item.texture_transformation ?? null,
				item.contrast_transformation ?? null,
			]);
		});

		if (echarts.getInstanceByDom(chartDom)) {
			echarts.dispose(chartDom);
		}

		const chart = echarts.init(chartDom);

		// Build helpers to map from visible series label back to dataset column name
		const header = results[0] as string[];
		const labelToKey = Object.fromEntries(
			Object.entries(labelMap).map(([key, label]) => [label, key]),
		) as Record<string, string>;

		const fieldNames = Object.keys(labelMap);
		const seriesList: echarts.SeriesOption[] = fieldNames.map(name => ({
			type: 'line',
			name: labelMap[name],
			showSymbol: false,
			encode: { x: 'par', y: name },
			emphasis: { focus: 'series' },
			labelLayout: { moveOverlap: 'shiftY' },
			lineStyle: { width: 3 },
		}));

		chart.setOption({
			color: ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc949'],
			animationDuration: 1500,
			animationEasing: 'cubicInOut',
			tooltip: {
				trigger: 'axis',
				backgroundColor: '#fff',
				borderColor: '#ccc',
				textStyle: { color: '#000' },
				formatter: params => {
					const lines = [`Par ${params[0].axisValue}`];
					for (let i = 0; i < params.length; i++) {
						const p = params[i];
						const baseKey = labelToKey[p.seriesName as string];
						const idx = header.indexOf(baseKey);
						let val: number | null = null;
						if (idx >= 0) {
							const fromValue = Array.isArray(p.value) ? p.value[idx] : p.value;
							const num =
								typeof fromValue === 'number'
									? fromValue
									: Array.isArray(p.data)
										? p.data[idx]
										: null;
							val = typeof num === 'number' && !Number.isNaN(num) ? num : null;
						}
						lines.push(
							`${p.marker} ${p.seriesName}: <b>${val !== null ? val.toFixed(4) : '—'}</b>`,
						);
					}
					return lines.join('<br/>');
				},
			},
			legend: { orient: 'horizontal', top: 0, left: 'center' },
			dataset: { source: results },
			xAxis: { type: 'category', name: 'Pares' },
			yAxis: { type: 'value', name: 'Similitud', min: 0, max: 1 },
			series: seriesList,
		});

		const onResize = () => chart.resize();
		window.addEventListener('resize', onResize);
		return () => {
			window.removeEventListener('resize', onResize);
			if (echarts.getInstanceByDom(chartDom)) echarts.dispose(chartDom);
		};
	}, [rawData]);

	return (
		<div className="min-h-screen flex flex-col justify-center px-6 items-center">
			<div className="text-center max-w-7xl mx-auto space-y-6">
				<h1 className="text-3xl font-bold text-blue-600">Resultados</h1>
				<h2 className="text-xl font-bold">Gráfico Total de Transformaciones</h2>
			</div>

			<div className="w-full max-w-6xl space-y-6">
				<div className="relative w-full h-[28rem] bg-white">
					{isLoading && (
						<div className="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-80">
							<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
						</div>
					)}

					{!isLoading && (isError || !rawData || rawData.length === 0) && (
						<div className="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-90">
							<p className="text-gray-600 text-lg">No hay datos disponibles para mostrar.</p>
						</div>
					)}

					<div ref={chartRef} className="w-full h-full" />
				</div>

				{extremes?.max && extremes?.min ? (
					<div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">
						<CardValue
							title="Máximo"
							value={extremes.max.value}
							metric={extremes.max.label}
							type="max"
							size="sm"
							delay={300}
						/>
						<CardValue
							title="Mínimo"
							value={extremes.min.value}
							metric={extremes.min.label}
							type="min"
							size="sm"
							delay={300}
						/>
					</div>
				) : null}
			</div>
		</div>
	);
};
