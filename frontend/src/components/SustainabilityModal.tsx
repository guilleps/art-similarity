import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { Leaf, ExternalLink, Tv, Car, Smartphone } from 'lucide-react';

interface SustainabilityModalProps {
	open: boolean;
	onOpenChange: (open: boolean) => void;
}

export const SustainabilityModal = ({ open, onOpenChange }: SustainabilityModalProps) => {
	return (
		<Dialog open={open} onOpenChange={onOpenChange}>
			<DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto border-2 border-success">
				<DialogHeader>
					<DialogTitle className="flex items-center gap-2 text-2xl">
						<Leaf className="h-6 w-6 text-[#16a249]" />
						Sostenibilidad
					</DialogTitle>
					<p className="text-sm text-muted-foreground mt-2">
						Evaluación del consumo energético y emisiones de CO₂ generadas por ArtShift durante su
						ejecución en backend y frontend.
					</p>
				</DialogHeader>

				<div className="grid md:grid-cols-2 gap-6 mt-6">
					{/* CodeCarbon Card */}
					<div className="border border-border rounded-lg p-6 space-y-4">
						<div className="flex items-center justify-between">
							<h3 className="font-semibold text-lg">CodeCarbon (Backend)</h3>
							<a
								href="https://dashboard.codecarbon.io/public/projects/Xh2lFau8FPZ_Frv7FoHfFX5G4Cj3uwXA6pptubGCGBVqvDu7ojfl7CWXIvQqwnX1Yx41zhGQ38H2b6gWpPgY-g"
								target="_blank"
								rel="noopener noreferrer"
								className="text-muted-foreground hover:text-foreground transition-colors"
							>
								<ExternalLink className="h-4 w-4" />
							</a>
						</div>

						<div className="grid grid-cols-2 gap-4 text-center">
							<div>
								<p className="text-3xl font-bold text-[#16a249]">0.08 kWh</p>
								<p className="text-xs text-muted-foreground mt-1">
									Consumo
									<br />
									energético
								</p>
							</div>
							<div>
								<p className="text-3xl font-bold text-[#16a249]">0.02 kg</p>
								<p className="text-xs text-muted-foreground mt-1">
									Emisiones
									<br />
									CO₂eq
								</p>
							</div>
						</div>

						<div className="pt-4 border-t border-border space-y-3">
							<p className="text-sm font-medium">Equivale a:</p>
							<div className="flex items-center gap-3">
								<Tv className="h-8 w-8 text-muted-foreground flex-shrink-0" />
								<p className="text-sm">
									<span className="font-semibold">0,02 días</span> de ver la televisión
								</p>
							</div>
							<div className="flex items-center gap-3">
								<Car className="h-8 w-8 text-muted-foreground flex-shrink-0" />
								<p className="text-sm">
									<span className="font-semibold">0,15 km</span> recorridos en auto
								</p>
							</div>
						</div>
					</div>

					{/* Website Carbon Card */}
					<div className="border border-border rounded-lg p-6 space-y-4">
						<div className="flex items-center justify-between">
							<h3 className="font-semibold text-lg">Website Carbon (Frontend)</h3>
							<a
								href="https://www.websitecarbon.com/website/artshift-vercel-app/"
								target="_blank"
								rel="noopener noreferrer"
								className="text-muted-foreground hover:text-foreground transition-colors"
							>
								<ExternalLink className="h-4 w-4" />
							</a>
						</div>

						<div className="grid grid-cols-2 gap-4 text-center">
							<div>
								<p className="text-5xl font-bold text-[#16a249]">A</p>
								<p className="text-xs text-muted-foreground mt-1">Calificación</p>
							</div>
							<div>
								<p className="text-2xl font-bold text-[#16a249]">0.06 g</p>
								<p className="text-xs text-muted-foreground mt-1">
									Emisiones
									<br />
									CO₂eq/vista
								</p>
							</div>
						</div>

						<div className="pt-4 border-t border-border space-y-3">
							<p className="text-sm font-medium">En un año, 1000 vistas equivalen a:</p>
							<p className="text-lg font-semibold">1 kWh de energía</p>
							<div className="flex items-start gap-3">
								<Smartphone className="h-6 w-6 text-muted-foreground flex-shrink-0 mt-0.5" />
								<p className="text-sm">
									para cargar <span className="font-semibold">116 veces el 100%</span> de batería de
									un smartphone
								</p>
							</div>
							<div className="flex items-start gap-3">
								<Car className="h-6 w-6 text-muted-foreground flex-shrink-0 mt-0.5" />
								<p className="text-sm">
									para recorrer <span className="font-semibold">9 km</span> en un auto eléctrico
								</p>
							</div>
						</div>
					</div>
				</div>

				<div className="mt-6 pt-4 border-t border-border text-center">
					<p className="text-sm text-muted-foreground">
						Consulta el archivo{' '}
						<a
							href="https://github.com/guilleps/art-similarity/blob/main/SUSTAINABILITY.md"
							target="_blank"
							rel="noopener noreferrer"
							className="text-[#16a249] font-medium hover:underline transition-all inline-block relative after:absolute after:bottom-0 after:left-0 after:w-full after:h-0.5 after:bg-[#16a249] after:scale-x-0 hover:after:scale-x-100 after:transition-transform after:duration-300"
						>
							SUSTAINABILITY.md
						</a>{' '}
						con más detalles sobre mediciones, configuración y prácticas sostenibles.
					</p>
				</div>
			</DialogContent>
		</Dialog>
	);
};
