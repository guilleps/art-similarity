import { TransformChart } from './TransformChart';
import useEmblaCarousel from 'embla-carousel-react';
import Autoplay from 'embla-carousel-autoplay';
import { useCallback, useRef, useState, useEffect } from 'react';

const transformations = [
	{ key: 'color_heat_map', label: 'Mapa de calor de color (TMCC)' },
	{ key: 'tone', label: 'Tono (TT)' },
	{ key: 'saturation', label: 'Saturación (TS)' },
	{ key: 'brightness', label: 'Brillo (TB)' },
	{ key: 'texture', label: 'Textura (TX)' },
	{ key: 'contrast', label: 'Contraste (TC)' },
];

export const TransformResults = () => {
	const autoplay = useRef(
		Autoplay({ delay: 4000, stopOnInteraction: false, stopOnMouseEnter: true }),
	);

	const [emblaRef, emblaApi] = useEmblaCarousel({ loop: false }, [autoplay.current]);

	const [canPrev, setCanPrev] = useState(false);
	const [canNext, setCanNext] = useState(false);
	const [selectedIndex, setSelectedIndex] = useState(0);
	const [scrollSnaps, setScrollSnaps] = useState<number[]>([]);

	const onSelect = useCallback(() => {
		if (!emblaApi) return;
		setCanPrev(emblaApi.canScrollPrev());
		setCanNext(emblaApi.canScrollNext());
	}, [emblaApi]);

	useEffect(() => {
		if (!emblaApi) return;
		const handleSelect = () => {
			onSelect();
			setSelectedIndex(emblaApi.selectedScrollSnap());
		};
		const handleReInit = () => {
			setScrollSnaps(emblaApi.scrollSnapList());
			handleSelect();
		};
		// Init
		setScrollSnaps(emblaApi.scrollSnapList());
		handleSelect();

		emblaApi.on('select', handleSelect);
		emblaApi.on('reInit', handleReInit);
		return () => {
			emblaApi.off('select', handleSelect);
			emblaApi.off('reInit', handleReInit);
		};
	}, [emblaApi, onSelect]);

	const scrollPrev = useCallback(() => {
		autoplay.current?.stop();
		emblaApi?.scrollPrev();
	}, [emblaApi]);

	const scrollNext = useCallback(() => {
		autoplay.current?.stop();
		emblaApi?.scrollNext();
	}, [emblaApi]);

	const scrollTo = useCallback(
		(index: number) => {
			autoplay.current?.stop();
			emblaApi?.scrollTo(index);
		},
		[emblaApi],
	);

	return (
		<>
			<div className="min-h-screen px-4 sm:px-6 lg:px-8 pt-12 pb-12 scroll-view">
				<div className="text-center space-y-6 max-w-6xl mx-auto">
					<div className="flex flex-col items-center text-center gap-2 mb-12">
						<p className="text-foreground max-w-3xl text-xl font-bold md:text-2xl mt-2">
							Estadísticas por Transformación
						</p>
					</div>

					<div className="relative">
						<div className="gap-4">
							<div className="flex items-center gap-3">
								{/* Prev */}
								<button
									type="button"
									onClick={scrollPrev}
									disabled={!canPrev}
									aria-label="Anterior"
									className="rounded-full bg-white/90 hover:bg-white shadow px-4 py-3 text-xl disabled:opacity-50 transition duration-200 hover:shadow-lg hover:-translate-y-0.5 ring-1 ring-black/5 hover:ring-black/10"
								>
									‹
								</button>

								{/* Carousel */}
								<div className="overflow-hidden flex-1" ref={emblaRef}>
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

								{/* Next */}
								<button
									type="button"
									onClick={scrollNext}
									disabled={!canNext}
									aria-label="Siguiente"
									className="rounded-full bg-white/90 hover:bg-white shadow px-4 py-3 text-xl disabled:opacity-50 transition duration-200 hover:shadow-lg hover:-translate-y-0.5 ring-1 ring-black/5 hover:ring-black/10"
								>
									›
								</button>
							</div>
						</div>
					</div>
					{/* Dot navigation */}
					<div className="mt-4 flex items-center justify-center gap-2">
						{scrollSnaps.map((_, i) => (
							<button
								key={i}
								type="button"
								aria-label={`Ir al slide ${i + 1}`}
								onClick={() => scrollTo(i)}
								className={`h-2.5 w-2.5 rounded-full transition-all duration-200 ${i === selectedIndex ? 'bg-blue-600 w-5' : 'bg-gray-300 hover:bg-gray-400'}`}
							/>
						))}
					</div>
				</div>
			</div>
		</>
	);
};
