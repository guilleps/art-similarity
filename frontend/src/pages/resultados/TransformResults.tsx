import { Card } from "@/components/ui/card";
import { TransformChart } from "./TransformChart";

const transformations = [
    { key: "color_heat_map", label: "Mapa de calor de color (TMCC)" },
    { key: "tone", label: "Tono (TT)" },
    { key: "saturation", label: "Saturación (TS)" },
    { key: "brightness", label: "Brillo (TB)" },
    { key: "texture", label: "Textura (TX)" },
    { key: "contrast", label: "Contraste (TC)" },
];

export const TransformResults = () => {
    return (
        <div className="min-h-screen px-4 sm:px-6 lg:px-8 pt-12 pb-24 scroll-view">
            <div className="text-center space-y-6 max-w-6xl mx-auto">
                <div className="flex flex-col items-center text-center gap-2 mb-12">
                    <p className="text-foreground max-w-3xl text-xl font-bold md:text-2xl mt-2">Gráficos por Transformación</p>
                </div>

                <div className="relative">
                    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-3 gap-4">
                        {transformations.map(t => (
                            <div key={t.key} >
                                <span className="text-base font-bold text-center z-10 group-hover:scale-105 transition-transform duration-300">
                                    {t.label}
                                </span>
                                <TransformChart transform={t.key} />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
};
