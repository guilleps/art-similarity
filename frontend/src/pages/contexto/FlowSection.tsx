import { useAutoScrollView } from '@/hooks/useAutoScrollView';

export const FlowSection = () => {
	useAutoScrollView();

	return (
		<div className="min-h-screen flex flex-col items-center justify-center px-6 space-y-8 scroll-view">
			<div className="text-center space-y-6 max-w-6xl mx-auto">
				<h3 className="text-2xl font-bold">Representación del Flujo</h3>

				{/* Process Image */}
				<div className="w-full flex justify-center">
					<img
						src="https://res.cloudinary.com/dnydakj9z/image/upload/v1759408565/workflow_nxcwll.jpg"
						alt="Proceso del experimento"
						className="max-w-full h-auto"
					/>
				</div>

				{/* Technical Details */}
				<div className="space-y-1 mt-2">
					<h2 className="text-lg font-bold mb-6 text-center text-primary">Detalles Técnicos</h2>
					<div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
						<div>
							<h3 className="text-base font-bold mb-1">Dataset</h3>
							<p className="text-foreground/80 mb-4 text-base">
								Conjunto de pares de imágenes similares de pinturas impresionistas.
							</p>
							<h3 className="text-base font-bold mb-1">Transformaciones</h3>
							<p className="text-foreground/80 text-base">
								Mapa de calor de color, tono, saturación, brillo, textura y contraste.
							</p>
						</div>
						<div>
							<h3 className="text-base font-bold mb-1">Métrica</h3>
							<p className="text-foreground/80 mb-4 text-base">Similitud de coseno.</p>
							<h3 className="text-base font-bold mb-1">Representaciones vectoriales</h3>
							<p className="text-foreground/80 text-base">
								a través de la red neuronal CLIP (Contrastive Language-Image Pretraining).
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};
