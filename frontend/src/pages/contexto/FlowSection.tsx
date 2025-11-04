import { useAutoScrollView } from '@/hooks/useAutoScrollView';
import { Cpu, Database, Ruler, Sliders } from 'lucide-react';

export const FlowSection = () => {
	useAutoScrollView();

	return (
		<div className="min-h-screen flex flex-col items-center justify-center px-6 space-y-8 scroll-view">
			<div className="text-center space-y-6 max-w-6xl mx-auto">
				<h3 className="text-2xl font-bold">Representación del Flujo</h3>

				{/* Process Image */}
				<div className="relative group cursor-zoom-in">
					<img
						src="https://res.cloudinary.com/dnydakj9z/image/upload/v1759408565/workflow_nxcwll.jpg"
						alt="Proceso del experimento"
						className="transition-transform duration-300 group-hover:scale-110"
					/>
				</div>

				{/* Technical Details */}
				<div className="space-y-1 mt-2">
					<h2 className="text-lg font-bold mb-6 text-center text-primary">Detalles Técnicos</h2>
					<div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
						<div>
							<h3 className="flex items-center text-base font-semibold mb-1">
								<Database className="w-4 h-4 mr-2 text-blue-600" /> Dataset
							</h3>
							<p className="text-gray-700 mb-4">
								Conjunto de pares de imágenes similares de pinturas impresionistas.
							</p>
							<h3 className="flex items-center text-base font-semibold mb-1">
								<Sliders className="w-4 h-4 mr-2 text-blue-600" /> Transformaciones
							</h3>
							<p className="text-gray-700">
								Mapa de calor de color, tono, saturación, brillo, textura y contraste.
							</p>
						</div>

						<div>
							<h3 className="flex items-center text-base font-semibold mb-1">
								<Ruler className="w-4 h-4 mr-2 text-blue-600" /> Métrica
							</h3>
							<p className="text-gray-700 mb-4">Similitud de coseno.</p>
							<h3 className="flex items-center text-base font-semibold mb-1">
								<Cpu className="w-4 h-4 mr-2 text-blue-600" /> Representaciones vectoriales
							</h3>
							<p className="text-gray-700">
								Extraídas mediante la red neuronal profunda VGG-19 (Visual Geometry Group - 19
								capas).
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};
