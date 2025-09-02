import { useEffect, useMemo, useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import PaintingData from '@/types/painting';
import { getSimilaritiesById } from '@/services/similarity.service';
import { Image } from './Image';

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
	}, [comparisonId]);

	const paintingPairs = useMemo(() => {
		if (!data?.similitud || !data?.image_1 || !data?.image_2) return [];

		// claves normalizadas por el servicio mock
		const labelByKey: Record<string, string> = {
			contrast: 'Contraste',
			texture: 'Textura',
			color_heat_map: 'Mapa de Calor',
			tone: 'Tono',
			saturation: 'Saturación',
			brightness: 'Brillo',
		};

		const transformations = Object.keys(data.similitud).map((key) => {
			const left = (data.image_1.transformations as any)?.[key]?.image_transformed ?? data.image_1.original_image;
			const right = (data.image_2.transformations as any)?.[key]?.image_transformed ?? data.image_2.original_image;

			return {
				name: labelByKey[key] ?? key,
				similarity: data.similitud[key].similarity,
				leftImage: left,
				rightImage: right,
			};
		});

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
						return (
							<Card
								key={index}
								className="p-4 transition-all duration-500 animate-highlight border-academic-500 border-2 bg-academic-50"
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
								<div className="flex justify-center">
									<Badge variant="secondary">{formatSimilarity(transformation.similarity)}</Badge>
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
