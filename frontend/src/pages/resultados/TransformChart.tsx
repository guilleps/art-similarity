import { useEffect, useRef } from "react";
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

    useEffect(() => {
        const renderChart = async () => {
            const data = await getSimilaritiesByTransform(transform);

            if (echarts.getInstanceByDom(chartRef.current!)) {
                echarts.dispose(chartRef.current!);
            }

            const chart = echarts.init(chartRef.current!);
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
        };

        renderChart();
    }, [transform]);

    return <div ref={chartRef} className="w-full h-60 bg-white rounded shadow" />;
};
