import { useEffect, useMemo, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import PaintingData from '@/types/painting';
import { getSimilaritiesById } from '@/services/similarity.service';
import { Image } from './Image';
import { Award, AwardIcon } from 'lucide-react';

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

		return [
			{
				id: 1,
				leftPainting: { image: data.image_1.original_image },
				rightPainting: { image: data.image_2.original_image },
				transformations,
			},
		];
	}, [data]);

	const formatSimilarity = (value: number): string => {
		return `${(value * 100).toFixed(1)}%`;
	};

	const pair = paintingPairs[0];

	if (!pair) return null;

	// Calcular la mayor similitud para resaltar ese Card
	const maxSimilarity = Math.max(...pair.transformations.map(t => t.similarity ?? 0));

	return (
		<div className="max-w-7xl mx-auto">
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
							<Card
								key={index}
								className={`p-4 transition-all duration-500 animate-highlight bg-academic-50 ${
									isMax ? 'border-4 border-yellow-500' : 'border-2 border-academic-500'
								}`}
							>
								<div className="grid grid-cols-2 gap-2 mb-3">
									<img
										src={transformation.leftImage}
										alt={`${transformation.name} izquierda`}
										className="w-full h-20 object-cover rounded aspect-square"
									/>
									<img
										src={transformation.rightImage}
										alt={`${transformation.name} derecha`}
										className="w-full h-20 object-cover rounded aspect-square"
									/>
								</div>
								<p className="text-sm font-medium text-gallery-700 mb-2 text-center">
									{transformation.name}
								</p>
								<div className="flex items-center justify-center group transition-transform duration-300 group-hover:scale-105 gap-1">
									{isMax ? (
										<>
											<Award className="w-4 h-4" />
											<Badge variant="default">{transformation.similarity}</Badge>
											{/* <Badge variant="default">{formatSimilarity(transformation.similarity)}</Badge> */}
										</>
									) : (
										<Badge variant="secondary">{transformation.similarity}</Badge>
									)}
								</div>
							</Card>
						);
					})}
				</div>
			</div>
		</div>
	);
};

export default SimilarityViewer;
