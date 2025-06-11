import { getAllSimilaritiesRaw } from "@/services/similarity.service";
import * as echarts from "echarts";
import { useEffect, useRef } from "react"

// const results: (string | number)[][] = [
//     ['par', 'color_heat_map', 'tone', 'saturation', 'brightness', 'texture', 'contrast'],
//     ['1', 0.912, 0.941, 0.789, 0.851, 0.964, 0.902],
//     ['2', 0.873, 0.884, 0.795, 0.742, 0.926, 0.813],
//     ['3', 0.733, 0.896, 0.813, 0.917, 0.702, 0.941],
//     ['4', 0.884, 0.958, 0.837, 0.896, 0.991, 0.888],
//     ['5', 0.785, 0.722, 0.861, 0.909, 0.748, 0.732],
//     ['6', 0.972, 0.984, 0.937, 0.976, 0.958, 0.961],
//     ['7', 0.801, 0.748, 0.753, 0.798, 0.778, 0.812],
//     ['8', 0.853, 0.893, 0.892, 0.844, 0.932, 0.871],
//     ['9', 0.741, 0.739, 0.708, 0.719, 0.726, 0.781],
//     ['10', 0.911, 0.938, 0.901, 0.923, 0.944, 0.889],
//     ['11', 0.765, 0.845, 0.823, 0.861, 0.799, 0.849],
//     ['12', 0.879, 0.928, 0.887, 0.842, 0.911, 0.866],
//     ['13', 0.793, 0.769, 0.778, 0.757, 0.817, 0.741],
//     ['14', 0.821, 0.856, 0.849, 0.837, 0.891, 0.853],
//     ['15', 0.956, 0.974, 0.963, 0.945, 0.967, 0.973],
//     ['16', 0.674, 0.483, 0.617, 0.342, 0.651, 0.492],
//     ['17', 0.559, 0.691, 0.462, 0.579, 0.409, 0.376],
//     ['18', 0.384, 0.421, 0.689, 0.577, 0.358, 0.335],
//     ['19', 0.429, 0.397, 0.627, 0.336, 0.581, 0.679],
//     ['20', 0.537, 0.537, 0.494, 0.644, 0.684, 0.509],
//     ['21', 0.489, 0.683, 0.597, 0.457, 0.422, 0.642],
//     ['22', 0.609, 0.655, 0.422, 0.583, 0.488, 0.672],
//     ['23', 0.321, 0.459, 0.534, 0.689, 0.343, 0.528],
//     ['24', 0.485, 0.661, 0.381, 0.417, 0.591, 0.437],
//     ['25', 0.698, 0.549, 0.361, 0.504, 0.395, 0.662],
//     ['26', 0.531, 0.445, 0.593, 0.697, 0.553, 0.493],
//     ['27', 0.368, 0.374, 0.619, 0.346, 0.673, 0.362],
//     ['28', 0.619, 0.625, 0.413, 0.462, 0.489, 0.387],
//     ['29', 0.543, 0.552, 0.685, 0.552, 0.613, 0.597],
//     ['30', 0.582, 0.588, 0.664, 0.325, 0.434, 0.627],
// ];

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