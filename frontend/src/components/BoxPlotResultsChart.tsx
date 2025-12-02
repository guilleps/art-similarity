import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';

export type BoxPlotResultsChartProps = {
	results: (string | number)[][]; // dataset: first row is header ['metric','min','Q1','median','Q3','max']
};

export const BoxPlotResultsChart = ({ results }: BoxPlotResultsChartProps) => {
	const chartRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		const chartDom = chartRef.current;
		if (!chartDom) return;
		if (!results || results.length === 0) return;

		if (echarts.getInstanceByDom(chartDom)) {
			echarts.dispose(chartDom);
		}

		const chart = echarts.init(chartDom);

		const palette = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f', '#edc949'];
		const labels = results.slice(1).map(row => String(row[0]));
		type BoxDatum = {
			value: [number, number, number, number, number];
			itemStyle: { color: string; borderColor: string };
		};
		const dataItems: BoxDatum[] = results.slice(1).map((row, idx) => ({
			value: [Number(row[1]), Number(row[2]), Number(row[3]), Number(row[4]), Number(row[5])],
			itemStyle: {
				color: palette[idx % palette.length],
				borderColor: palette[idx % palette.length],
			},
		}));

		const seriesList: echarts.SeriesOption[] = [
			{
				name: 'boxplot',
				type: 'boxplot',
				data: dataItems,
			},
		];

		chart.setOption({
			color: palette,
			animationDuration: 1200,
			animationEasing: 'cubicInOut',
			tooltip: {
				trigger: 'axis',
				confine: true,
			},
			legend: { show: false },
			xAxis: {
				type: 'value',
				name: 'Similitud',
				min: 0,
				max: 1,
				nameLocation: 'middle',
				nameGap: 30,
				scale: true,
			},
			yAxis: { type: 'category', data: labels },
			grid: {
				top: 24,
				right: 24,
				bottom: 24,
				left: 100,
			},
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
