import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';
import { labelMap } from '@/types/similarity';

export type GeneralResultsChartProps = {
	results: (string | number)[][]; // dataset: first row is header
};

export const GeneralResultsChart = ({ results }: GeneralResultsChartProps) => {
	const chartRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		const chartDom = chartRef.current;
		if (!chartDom) return;
		if (!results || results.length === 0) return;

		if (echarts.getInstanceByDom(chartDom)) {
			echarts.dispose(chartDom);
		}

		const chart = echarts.init(chartDom);

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
				formatter: (
					params: Array<{
						axisValue: string | number;
						seriesName: string;
						marker: string;
						value: unknown;
						data?: unknown;
					}>,
				) => {
					const lines = [`Par ${String(params[0].axisValue)}`];
					for (let i = 0; i < params.length; i++) {
						const p = params[i];
						const baseKey = labelToKey[p.seriesName as string];
						const idx = header.indexOf(baseKey);
						let val: number | null = null;
						if (idx >= 0) {
							const fromValue = Array.isArray(p.value) ? (p.value as Array<unknown>)[idx] : p.value;
							const num =
								typeof fromValue === 'number'
									? fromValue
									: Array.isArray(p.data)
										? (p.data as Array<unknown>)[idx]
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
	}, [results]);

	return <div ref={chartRef} className="w-full h-full" />;
};
