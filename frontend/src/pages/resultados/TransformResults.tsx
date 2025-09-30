import { TransformChart } from './TransformChart';
import useEmblaCarousel from 'embla-carousel-react';
import Autoplay from 'embla-carousel-autoplay';

const transformations = [
	{ key: 'color_heat_map', label: 'Mapa de calor de color (TMCC)' },
	{ key: 'tone', label: 'Tono (TT)' },
	{ key: 'saturation', label: 'Saturación (TS)' },
	{ key: 'brightness', label: 'Brillo (TB)' },
	{ key: 'texture', label: 'Textura (TX)' },
	{ key: 'contrast', label: 'Contraste (TC)' },
];

export const TransformResults = () => {
	const [emblaRef] = useEmblaCarousel({ loop: false }, [Autoplay()]);

	return (
		<>
			<div className="min-h-screen px-4 sm:px-6 lg:px-8 pt-12 pb-24 scroll-view">
				<div className="text-center space-y-6 max-w-6xl mx-auto">
					<div className="flex flex-col items-center text-center gap-2 mb-12">
						<p className="text-foreground max-w-3xl text-xl font-bold md:text-2xl mt-2">
							Estadísticas por Transformación
						</p>
					</div>

					<div className="relative">
						<div className="gap-4">
							<div className="overflow-hidden" ref={emblaRef}>
								<div className="flex">
									{transformations.map(t => {
										return (
											<div key={t.key} className="min-h-0 min-w-0 flex-[0_0_100%]">
												<span className="text-base font-bold text-center z-10">{t.label}</span>

												<TransformChart transform={t.key} />
											</div>
										);
									})}
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
};
