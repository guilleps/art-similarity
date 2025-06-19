import { useEffect, useRef, useState } from "react";
import * as echarts from "echarts";
import { getSimilaritiesByTransform } from "@/services/similarity.service";

const colors: Record<string, string> = {
    color_heat_map: '#4e79a7',
    tone: '#f28e2b',
    saturation: '#e15759',
    brightness: '#76b7b2',
    texture: '#59a14f',
    contrast: '#edc949'
};

export const TransformChart = ({ transform }: { transform: string; }) => {
    const chartRef = useRef<HTMLDivElement>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [hasData, setHasData] = useState(true);

    useEffect(() => {
        const chartDom = chartRef.current;

        const renderChart = async () => {
            try {
                setIsLoading(true);
                const data = await getSimilaritiesByTransform(transform);

                if (!Array.isArray(data) || data.length === 0) {
                    setHasData(false);
                    return;
                }

                setHasData(true);

                if (!chartDom) return;

                if (echarts.getInstanceByDom(chartDom)) {
                    echarts.dispose(chartDom);
                }

                const chart = echarts.init(chartDom);
                chart.setOption({
                    color: [colors[transform]],
                    tooltip: { trigger: 'axis' },
                    xAxis: { type: 'category', data: data.map(d => d.par.toString()) },
                    yAxis: { type: 'value', min: 0, max: 1 },
                    series: [{
                        type: 'line',
                        data: data.map(d => d.value),
                        smooth: true,
                        areaStyle: { opacity: 0.1 },
                    }]
                });

            } catch (error) {
                console.error("Error al cargar datos de transformación:", error);
                setHasData(false);
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
        // <div ref={chartRef} className="w-full h-60 bg-white rounded shadow" />
        <div className="relative w-full h-60 bg-white rounded shadow">
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
            <div ref={chartRef} className="w-full h-full" />
        </div>
    );
};
