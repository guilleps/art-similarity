import { Brain, Lightbulb, Shield } from "lucide-react";
import { ValueProp } from "./ValueProp";

export const About = () => (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 space-y-12 scroll-view">
        <div className="py-16 px-4 rounded-lg glass-panel my-24">
            <h2 className="text-3xl font-bold text-center mb-3">Acerca del Experimento</h2>
            <p className="text-xl text-center text-foreground/80 max-w-3xl mx-auto mb-16">
                Con el objetivo de determinar la variación de la similitud compositiva de pinturas
                impresionistas según las características visuales de bajo nivel mediante
                representaciones vectoriales, las fases que se siguieron fueron:
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <ValueProp
                    icon={<Brain className="w-8 h-8 text-blue-600" />}
                    title="Aplicar transformaciones visuales"
                    description="Resalta características visuales de bajo nivel."
                />
                <ValueProp
                    icon={<Shield className="w-8 h-8 text-blue-600" />}
                    title="Extraer representaciones vectoriales"
                    description="por cada transformación visual aplicada."
                />
                <ValueProp
                    icon={<Lightbulb className="w-8 h-8 text-blue-600" />}
                    title="Calcular la similitud compositiva"
                    description="a partir de las representaciones vectoriales de cada transformación aplicada."
                />
            </div>
        </div>
    </div>
);