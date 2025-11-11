import { CarbonBadge } from '@/components/CarbonBadge';
import { Button } from '@/components/ui/button';
import { Link } from 'react-router-dom';

export const HeroSection = () => (
	<div className="min-h-screen flex flex-col items-center justify-center px-6 space-y-8 scroll-view">
		<div className="text-center space-y-4 max-w-4xl">
			<h1 className="text-4xl md:text-5xl font-bold leading-tight">
				<span className="text-blue-600">
					Análisis de características visuales de bajo nivel mediante representaciones vectoriales
				</span>
				<span className="text-black"> en la similitud compositiva de pinturas impresionistas</span>
			</h1>
		</div>
		<div className="text-center">
			<Link to="/resultados">
				<Button className="bg-gray-800 hover:bg-gray-700 font-bold text-white px-8 py-2 rounded-full">
					Ver resultados
				</Button>
			</Link>
		</div>

		<CarbonBadge />
	</div>
);
