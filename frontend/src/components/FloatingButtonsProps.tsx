import { Leaf, Github } from 'lucide-react';
import { Button } from './ui/button';

interface FloatingButtonsProps {
	onSustainabilityClick: () => void;
}

export const FloatingButtons = ({ onSustainabilityClick }: FloatingButtonsProps) => {
	return (
		<div className="fixed bottom-4 right-4 z-40 flex flex-col gap-4">
			<Button
				size="icon"
				onClick={onSustainabilityClick}
				className="h-12 w-12 rounded-full bg-[#16a249] hover:bg-[#16a249]/90 shadow-lg transition-all hover:scale-105"
			>
				<Leaf className="h-6 w-6 text-white" />
			</Button>
			<Button
				size="icon"
				asChild
				className="h-12 w-12 rounded-full bg-gray-900 hover:bg-gray-800 shadow-lg transition-all hover:scale-105"
			>
				<a
					href="https://github.com/guilleps/art-similarity"
					target="_blank"
					rel="noopener noreferrer"
					aria-label="GitHub"
				>
					<Github className="h-6 w-6 text-white" />
				</a>
			</Button>
		</div>
	);
};
