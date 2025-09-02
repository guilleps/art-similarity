import { getAllSimilaritiesRaw } from '@/services/similarity.service';
import * as echarts from 'echarts';
import { useEffect, useRef, useState } from 'react';

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

export const GeneralResult = () => {
	const chartRef = useRef<HTMLDivElement>(null);
	const [isLoading, setIsLoading] = useState(true);
	const [hasData, setHasData] = useState(true);

	useEffect(() => {
		const chartInstance = { current: null as echarts.ECharts | null };
		const chartDom = chartRef.current;

		const loadChart = async () => {
			try {
				setIsLoading(true);
				const rawData: SimilarityRaw[] = await getAllSimilaritiesRaw();
				// console.log('pares', rawData);

				if (!Array.isArray(rawData) || rawData.length === 0) {
					setHasData(false);
					return;
				}

				setHasData(true);

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

				if (!chartDom) return;

				if (echarts.getInstanceByDom(chartDom)) {
					echarts.dispose(chartDom);
				}

				const chart = echarts.init(chartDom);
				chartInstance.current = chart;

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
							let tooltip = `Par ${params[0].axisValue}<br/>`;
							for (let i = 0; i < params.length; i++) {
								tooltip += `${params[i].marker} ${params[i].seriesName}: <b>${params[i].value[1]}</b><br/>`;
							}
							return tooltip;
						},
					},
					legend: {
						orient: 'horizontal',
						top: 0,
						left: 'center',
					},
					dataset: { source: results },
					xAxis: { type: 'category', name: 'Pares' },
					yAxis: { type: 'value', name: 'Similitud', min: 0, max: 1 },
					series: seriesList,
				});
			} catch (error) {
				console.error('Error al cargar los datos:', error);
				setHasData(false);
			} finally {
				setIsLoading(false);
			}
		};

		loadChart();

		return () => {
			if (chartDom && echarts.getInstanceByDom(chartDom)) {
				echarts.dispose(chartDom);
			}
		};
	}, []);

	return (
		<div className="min-h-screen flex flex-col justify-center px-6 py-8 items-center">
			<div className="text-center max-w-7xl mx-auto space-y-6">
				<h1 className="text-3xl font-bold text-blue-600">Resultados</h1>
				<h2 className="text-xl font-bold">Gráfico Total de Transformaciones</h2>
			</div>

			<div className="relative w-full max-w-6xl h-[28rem] bg-white pt-4">
				{isLoading && (
					<div className="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-80">
						<div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
					</div>
				)}

				{!isLoading && !hasData && (
					<div className="absolute inset-0 z-10 flex items-center justify-center bg-white bg-opacity-90">
						<p className="text-gray-600 text-lg">No hay datos disponibles para mostrar.</p>
					</div>
				)}

				<div ref={chartRef} className="w-full h-full" />
			</div>
		</div>
	);
};
