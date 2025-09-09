import { useEffect, useRef, useState } from 'react';
import * as echarts from 'echarts';
import { getSimilaritiesByTransform } from '@/services/similarity.service';

const colors: Record<string, string> = {
	color_heat_map: '#4e79a7',
	tone: '#f28e2b',
	saturation: '#e15759',
	brightness: '#76b7b2',
	texture: '#59a14f',
	contrast: '#edc949',
};

type Point = { par: number; value: number };

export const TransformChart = ({ transform }: { transform: string }) => {
	const chartRef = useRef<HTMLDivElement>(null);
	const [isLoading, setIsLoading] = useState(true);
	const [hasData, setHasData] = useState(true);
	const [data, setData] = useState<Point[]>([]);
	const [stats, setStats] = useState<{ min: number; max: number; avg: number } | null>(null);

	useEffect(() => {
		const chartDom = chartRef.current;

		const renderChart = async () => {
			try {
				setIsLoading(true);

				// fetch data for this transform
				const resp = await getSimilaritiesByTransform(transform);
				const arr: Point[] = Array.isArray(resp) ? (resp as Point[]) : [];
				setData(arr);

				if (!Array.isArray(arr) || arr.length === 0) {
					setHasData(false);
					setStats(null);
					return;
				}

				// compute stats
				const values = arr.map(d => d.value).filter(v => typeof v === 'number' && !Number.isNaN(v));
				if (values.length === 0) {
					setHasData(false);
					setStats(null);
					return;
				}
				const min = Math.min(...values);
				const max = Math.max(...values);
				const avg = values.reduce((a, b) => a + b, 0) / values.length;
				setStats({ min, max, avg });

				setHasData(true);

				if (!chartDom) return;

				if (echarts.getInstanceByDom(chartDom)) {
					echarts.dispose(chartDom);
				}

				const chart = echarts.init(chartDom);
				chart.setOption({
					color: [colors[transform]],
					tooltip: { trigger: 'axis' },
					xAxis: { type: 'category', data: arr.map(d => d.par.toString()) },
					yAxis: { type: 'value', min: 0, max: 1 },
					series: [
						{
							type: 'line',
							data: arr.map(d => d.value),
							smooth: true,
							areaStyle: { opacity: 0.1 },
						},
					],
				});
			} catch (error) {
				console.error('Error al cargar datos de transformación:', error);
				setHasData(false);
				setStats(null);
			} finally {
				setIsLoading(false);
			}
		};

		renderChart();

		return () => {
			if (chartDom && echarts.getInstanceByDom(chartDom)) {
				echarts.dispose(chartDom);
			}
		};
	}, [transform]);

	return (
		<div className="relative w-full h-80 md:h-96 lg:h-[32rem] bg-white rounded shadow">
			{isLoading && (
				<div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
					<div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
				</div>
			)}
			{!isLoading && !hasData && (
				<div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90 z-10">
					<p className="text-gray-500 text-sm text-center px-2">No hay datos disponibles.</p>
				</div>
			)}
			<div className="flex h-full gap-4">
				<div className="flex-1">
					<div ref={chartRef} className="w-full h-full" />
				</div>
				<aside className="w-52 md:w-60 lg:w-64 shrink-0">
					{stats ? (
						<>
							<div className="w-full h-full flex flex-col items-center justify-center gap-4">
								<span className="font-medium w-full border rounded-sm border-slate-600 p-3">
									Min: {stats.min.toFixed(4)}
								</span>
								<span className="font-medium w-full border rounded-sm border-slate-600 p-3">
									Max: {stats.max.toFixed(4)}
								</span>
								<span className="font-medium w-full border rounded-sm border-slate-600 p-3">
									Avg: {stats.avg.toFixed(4)}
								</span>
							</div>
						</>
					) : (
						<p className="text-sm text-gray-500">No hay datos disponibles.</p>
					)}
				</aside>
			</div>
		</div>
	);
};
