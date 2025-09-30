import { useEffect, useMemo, useState } from 'react';
import PaintingData from '@/types/painting';
import { getSimilaritiesById } from '@/services/similarity.service';
import { Image } from './Image';
import { TypeAnimation } from 'react-type-animation';
import { CardViewer } from './CardViewer';

interface Props {
	comparisonId: string;
	onLoaded?: () => void;
}

const SimilarityViewer = ({ comparisonId, onLoaded }: Props) => {
	const [data, setData] = useState<PaintingData | null>(null);

	useEffect(() => {
		const fetchData = async () => {
			const result = await getSimilaritiesById(comparisonId);
			setData(result);
			onLoaded?.(); // Notifica que cargó
		};
		fetchData();
	}, [comparisonId, onLoaded]);

	const paintingPairs = useMemo(() => {
		if (!data?.similitud || !data?.image_1 || !data?.image_2) return [];

		const transformations = Object.keys(data.similitud).map(key => ({
			name:
				{
					contrast: 'Contraste',
					texture: 'Textura',
					heat_color_map: 'Mapa de Calor',
					hsv_hue: 'Tono',
					hsv_saturation: 'Saturación',
					hsv_value: 'Brillo',
				}[key] || key,
			similarity: data.similitud[key].similarity,
			leftImage: data.image_1[key].image_transformed,
			rightImage: data.image_2[key].image_transformed,
		}));

		const analysis = data.analysis;

		return [
			{
				id: 1,
				leftPainting: { image: data.image_1.original_image },
				rightPainting: { image: data.image_2.original_image },
				transformations,
				analysis,
			},
		];
	}, [data]);

	const pair = paintingPairs[0];

	if (!pair) return null;

	// Calcular la mayor similitud para resaltar ese Card
	const maxSimilarity = Math.max(...pair.transformations.map(t => t.similarity ?? 0));

	return (
		<div className="max-w-7xl mx-auto">
			<div className="flex items-stretch">
				<div className="flex-1">
					{/* Main Images */}
					<div className="grid md:grid-cols-2 gap-12 mb-12">
						<Image image={pair.leftPainting.image} />
						<Image image={pair.rightPainting.image} />
					</div>

					{/* Transformations Grid */}
					<div className="overflow-hidden transition-all duration-700 ease-in-out opacity-100 max-h-[1000px]">
						<div className="grid grid-cols-2 md:grid-cols-3 gap-6">
							{pair.transformations.map((transformation, index) => {
								const isMax = transformation.similarity === maxSimilarity;
								return (
									<CardViewer
										key={`${index}-${transformation.name}`}
										index={index}
										isMax={isMax}
										transformation={transformation}
									/>
								);
							})}
						</div>
					</div>
				</div>
				<div className="w-[2px] bg-gray-300 self-stretch mx-4" aria-hidden="true"></div>
				{/* Llamar al servicio LLM prompting para interpretar los valores */}
				<aside className="w-25 md:w-46 lg:w-80 shrink-0 bg-white">
					<div className="h-full w-full">
						<TypeAnimation
							sequence={[pair.analysis.explanation, 1500]}
							wrapper="span"
							speed={50}
							style={{ fontWeight: 'bold' }}
							repeat={Infinity}
						/>
					</div>
				</aside>
			</div>
		</div>
	);
};

export default SimilarityViewer;
