import { getAllSimilaritiesRaw } from "@/services/similarity.service";
import * as echarts from "echarts";
import { useEffect, useRef } from "react"

const labelMap: Record<string, string> = {
    color_heat_map: "Mapa de calor",
    tone: "Tono",
    saturation: "Saturación",
    brightness: "Brillo",
    texture: "Textura",
    contrast: "Contraste"
};

export const GeneralResult = () => {
    const chartRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const chartInstance = { current: null as echarts.ECharts | null };

        const loadChart = async () => {
            try {
                const response = await getAllSimilaritiesRaw(); 
                const rawData = response.data;

                // Convertimos a formato tabular para ECharts
                const results: (string | number)[][] = [
                    ['par', 'color_heat_map', 'tone', 'saturation', 'brightness', 'texture', 'contrast']
                ];

                rawData.forEach((item: any, index: number) => {
                    results.push([
                        (index + 1).toString(),
                        item.color_heat_map_transformation ?? null,
                        item.tone_transformation ?? null,
                        item.saturation_transformation ?? null,
                        item.brightness_transformation ?? null,
                        item.texture_transformation ?? null,
                        item.contrast_transformation ?? null
                    ]);
                });

                if (echarts.getInstanceByDom(chartRef.current!)) {
                    echarts.dispose(chartRef.current!);
                }

                const chart = echarts.init(chartRef.current!);
                chartInstance.current = chart;

                const fieldNames = [
                    'color_heat_map',
                    'tone',
                    'saturation',
                    'brightness',
                    'texture',
                    'contrast'
                ];

                const seriesList: echarts.SeriesOption[] = fieldNames.map((name) => ({
                    type: 'line',
                    name: labelMap[name],
                    showSymbol: false,
                    encode: {
                        x: 'par',
                        y: name
                    },
                    emphasis: {
                        focus: 'series'
                    },
                    labelLayout: {
                        moveOverlap: 'shiftY'
                    },
                    lineStyle: { width: 3 }
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
                        formatter: (params) => {
                            let tooltip = `Par ${params[0].axisValue}<br/>`;
                            for (let i = 0; i < params.length; i++) {
                                tooltip += `${params[i].marker} ${params[i].seriesName}: <b>${params[i].value[1]}</b><br/>`;
                            }
                            return tooltip;
                        }
                    },
                    legend: {
                        orient: 'horizontal',
                        top: 0,
                        left: 'center'
                    },
                    dataset: {
                        source: results
                    },
                    xAxis: {
                        type: 'category',
                        name: 'Pares'
                    },
                    yAxis: {
                        type: 'value',
                        name: 'Similitud',
                        min: 0,
                        max: 1
                    },
                    series: seriesList
                });

                return () => chart.dispose();
            } catch (error) {
                console.error('Error al cargar los datos:', error);
                throw Error('Error al cargar los datos')
            }
        };

        loadChart();
        return () => {
            if (chartInstance.current) {
                chartInstance.current.dispose();
            }
        };
    }, []);

    return <div className="min-h-screen flex flex-col justify-center px-6 py-8 scroll-view items-center">
        <div className="text-center max-w-7xl mx-auto space-y-6">
            <h1 className="text-3xl font-bold text-blue-600">Resultados</h1>
            <h2 className="text-xl font-bold">Gráfico Total de Transformaciones</h2>
        </div>
        <div ref={chartRef} className="w-full max-w-6xl h-[28rem] bg-white pt-4" />
    </div>
};