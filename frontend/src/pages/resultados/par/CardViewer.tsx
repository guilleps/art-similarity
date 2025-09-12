import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { Award } from 'lucide-react';

type Transformation = {
	name: string;
	similarity: number;
	leftImage: string;
	rightImage: string;
};

interface CardViewerProps {
	index: number;
	isMax: boolean;
	transformation: Transformation;
}

export const CardViewer = ({ index, isMax, transformation }: CardViewerProps) => {
	const formatSimilarity = (value: number): string => `${(value * 100).toFixed(1)}%`;

	return (
		<>
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
		</>
	);
};
