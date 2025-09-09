import { getSimilaritiesByTransform } from '@/services/similarity.service';
import { TransformChart } from './TransformChart';
import { useEffect, useState } from 'react';
import { TypeAnimation } from 'react-type-animation';

type TransformKey =
	| 'color_heat_map'
	| 'tone'
	| 'saturation'
	| 'brightness'
	| 'texture'
	| 'contrast';

type Point = { par: number; value: number };

const transformations = [
	{ key: 'color_heat_map', label: 'Mapa de calor de color (TMCC)' },
	{ key: 'tone', label: 'Tono (TT)' },
	{ key: 'saturation', label: 'Saturación (TS)' },
	{ key: 'brightness', label: 'Brillo (TB)' },
	{ key: 'texture', label: 'Textura (TX)' },
	{ key: 'contrast', label: 'Contraste (TC)' },
];

export const TransformResults = () => {
	const [dataByKey, setDataByKey] = useState<Record<TransformKey, Point[]>>({
		color_heat_map: [],
		tone: [],
		saturation: [],
		brightness: [],
		texture: [],
		contrast: [],
	});
	const [statsByKey, setStatsByKey] = useState<
		Record<TransformKey, { min: number; max: number; avg: number } | null>
	>({
		color_heat_map: null,
		tone: null,
		saturation: null,
		brightness: null,
		texture: null,
		contrast: null,
	});
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		let cancelled = false;

		const fetchAll = async () => {
			try {
				setLoading(true);

				// Obtiene datos en paralelo para cada transformación
				const results = await Promise.all(
					transformations.map(async ({ key }) => {
						const resp = await getSimilaritiesByTransform(key);
						const arr = Array.isArray(resp) ? (resp as Point[]) : [];
						// calcula stats
						const values = arr
							.map(d => d.value)
							.filter(v => typeof v === 'number' && !Number.isNaN(v));
						const stats =
							values.length > 0
								? {
										min: Math.min(...values),
										max: Math.max(...values),
										avg: values.reduce((a, b) => a + b, 0) / values.length,
									}
								: null;
						return { key, arr, stats };
					}),
				);

				if (cancelled) return;

				// Arma los diccionarios
				const nextData: Record<TransformKey, Point[]> = { ...dataByKey };
				const nextStats: Record<TransformKey, { min: number; max: number; avg: number } | null> = {
					...statsByKey,
				};

				for (const r of results) {
					nextData[r.key] = r.arr;
					nextStats[r.key] = r.stats;
				}

				setDataByKey(nextData);
				setStatsByKey(nextStats);
			} finally {
				if (!cancelled) setLoading(false);
			}
		};

		fetchAll();
		return () => {
			cancelled = true;
		};
	}, []); // carga una vez

	return (
		<div className="min-h-screen px-4 sm:px-6 lg:px-8 pt-12 pb-24 scroll-view">
			<div className="text-center space-y-6 max-w-6xl mx-auto">
				<div className="flex flex-col items-center text-center gap-2 mb-12">
					<p className="text-foreground max-w-3xl text-xl font-bold md:text-2xl mt-2">
						Gráficos por Transformación
					</p>
				</div>

				<div className="relative">
					<div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-2 gap-4">
						{transformations.map(t => {
							const stats = statsByKey[t.key];
							const data = dataByKey[t.key];

							return (
								<div key={t.key} className="p-6">
									<span className="text-base font-bold text-center z-10 group-hover:scale-105 transition-transform duration-300">
										{t.label}
									</span>

									<TransformChart transform={t.key} data={data} />

									{/* Interpretacion */}
									{loading ? (
										<div className="mt-2 text-sm text-gray-500">
											<TypeAnimation sequence={['Cargando...', 1000]} speed={50} />
										</div>
									) : stats ? (
										<div className="mt-2 text-sm text-gray-700">
											<TypeAnimation
												key={`${t.key}-${stats.min}-${stats.max}-${stats.avg}`}
												sequence={[
													`Min: ${stats.min.toFixed(4)} - Max: ${stats.max.toFixed(4)} - Avg: ${stats.avg.toFixed(4)}`,
													1000,
												]}
												speed={50}
												wrapper="p"
												cursor={false}
												style={{ fontWeight: 'bold' }}
												repeat={0}
											/>
										</div>
									) : (
										<div className="mt-2 text-sm text-gray-500">Sin datos</div>
									)}
								</div>
							);
						})}
					</div>
				</div>
			</div>
		</div>
	);
};
