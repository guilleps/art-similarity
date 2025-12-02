import { useEffect, useRef, useMemo } from 'react';
import * as echarts from 'echarts';
import { getSimilaritiesByTransform } from '@/services/similarity.service';
import { useQuery } from '@tanstack/react-query';
import { Card } from '@/components/ui/card';
import { TrendingUp, TrendingDown, Gauge } from 'lucide-react';

const colors: Record<string, string> = {
	color_heat_map: '#4e79a7',
	tone: '#f28e2b',
	saturation: '#e15759',
	brightness: '#76b7b2',
	texture: '#59a14f',
	contrast: '#edc949',
};

type Point = { pair: number; value: number };

export const TransformChart = ({ transform }: { transform: string }) => {
	const chartRef = useRef<HTMLDivElement>(null);

	const { data, isLoading, isError } = useQuery<Point[]>({
		queryKey: ['transform', transform],
		queryFn: () => getSimilaritiesByTransform(transform) as Promise<Point[]>,
		staleTime: 5 * 60 * 1000,
		refetchOnMount: false,
		refetchOnWindowFocus: false,
	});

	const stats = useMemo(() => {
		const values = (data || [])
			.map(d => d.value)
			.filter(v => typeof v === 'number' && !Number.isNaN(v));
		if (!values.length) return null;
		const min = Math.min(...values);
		const max = Math.max(...values);
		const avg = values.reduce((a, b) => a + b, 0) / values.length;
		return { min, max, avg };
	}, [data]);

	useEffect(() => {
		const chartDom = chartRef.current;
		if (!chartDom) return;

		if (!data || !data.length) return;

		if (echarts.getInstanceByDom(chartDom)) {
			echarts.dispose(chartDom);
		}
		const chart = echarts.init(chartDom);
		chart.setOption({
			color: [colors[transform]],
			tooltip: { trigger: 'axis' },
			xAxis: { type: 'category', data: data.map(d => d.pair.toString()) },
			yAxis: { type: 'value', min: 0, max: 1 },
			series: [
				{
					type: 'line',
					data: data.map(d => d.value),
					smooth: true,
					areaStyle: { opacity: 0.1 },
				},
			],
		});

		const handleResize = () => chart.resize();
		window.addEventListener('resize', handleResize);
		return () => {
			window.removeEventListener('resize', handleResize);
			if (echarts.getInstanceByDom(chartDom)) {
				echarts.dispose(chartDom);
			}
		};
	}, [data, transform]);

	return (
		<div className="relative w-full h-80 md:h-96 lg:h-[32rem] bg-white rounded">
			{isLoading && (
				<div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
					<div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
				</div>
			)}
			{!isLoading && (!data || data.length === 0 || isError) && (
				<div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-90 z-10">
					<p className="text-gray-500 text-sm text-center px-2">No hay datos disponibles.</p>
				</div>
			)}
			<div className="flex h-full gap-4">
				<div className="flex-1">
					<div ref={chartRef} className="w-full h-full" />
				</div>
				<aside className="basis-1/4 min-w-0">
					{stats ? (
						<>
							<div className="w-full h-full flex flex-col items-center justify-center gap-4">
								<Card className="py-3 px-8 bg-gradient-card border-border/50 shadow-md hover:shadow-lg transition-all duration-300 animate-slide-up group hover:scale-105">
									<div className="font-bold flex flex-row items-center justify-center">
										<TrendingUp className="h-6 w-6 mr-2 text-green-400 rounded-lg bg-green-400/10" />
										Max: {stats.max.toFixed(4)}
									</div>
								</Card>

								<Card className="py-3 px-8 bg-gradient-card border-border/50 shadow-md hover:shadow-lg transition-all duration-300 animate-slide-up group hover:scale-105">
									<div className="font-bold flex flex-row items-center justify-center">
										<Gauge className="h-6 w-6 mr-2 text-red-400 rounded-lg bg-red-400/10" />
										Avg: {stats.avg.toFixed(4)}
									</div>
								</Card>

								<Card className="py-3 px-8 bg-gradient-card border-border/50 shadow-md hover:shadow-lg transition-all duration-300 animate-slide-up group hover:scale-105">
									<div className="font-bold flex flex-row items-center justify-center">
										<TrendingDown className="h-6 w-6 mr-2 text-orange-400 rounded-lg bg-orange-400/10" />
										Min: {stats.min.toFixed(4)}
									</div>
								</Card>
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
