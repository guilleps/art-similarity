import { Brain, Layers, BarChart3 } from 'lucide-react';
import { ValueProp } from './ValueProp';
import { useAutoScrollView } from '@/hooks/useAutoScrollView';

export const About = () => {
	useAutoScrollView();

	return (
		<section className="min-h-screen flex flex-col items-center justify-center px-6 space-y-8 scroll-view">
			<div className="text-center space-y-6 max-w-6xl mx-auto">
				<div className="text-center mb-16">
					<h2 className="text-2xl font-bold mb-4">Sobre la Investigación</h2>
					<div className="w-24 h-1 bg-blue-600 mx-auto mb-6"></div>
					<p className="text-lg text-gray-600 max-w-4xl mx-auto">
						Este proyecto explora cómo las técnicas de visión por computadora pueden ofrecer nuevas
						perspectivas sobre la composición artística en el movimiento impresionista, analizando
						patrones visuales y relaciones compositivas que no siempre resultan evidentes a simple
						vista.
					</p>
				</div>

				<div className="grid md:grid-cols-3 gap-12">
					<ValueProp
						icon={<Brain className="w-8 h-8 text-blue-600" />}
						title="Metodología"
						description="Aplicamos redes neuronales profundas para analizar características visuales de bajo nivel en más de 5 000 obras impresionistas."
					/>
					<ValueProp
						icon={<Layers className="w-8 h-8 text-blue-600" />}
						title="Conjunto de Datos"
						description="Proviene de un repositorio compuesto por obras impresionistas procesadas y normalizadas para futuras pruebas."
					/>
					<ValueProp
						icon={<BarChart3 className="w-8 h-8 text-blue-600" />}
						title="Resultados"
						description="Detectamos variaciones en la similitud compositiva y en las características visuales mediante filtros y transformaciones."
					/>
				</div>
			</div>
		</section>
	);
};
