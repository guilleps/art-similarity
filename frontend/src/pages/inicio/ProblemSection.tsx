import { Zap } from "lucide-react";

export const ProblemSection = () => (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 space-y-12 scroll-view">
        <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="space-y-4">
                <h1 className="text-3xl font-bold text-blue-600">¿Cómo nace el Experimento?</h1>
                <p className="text-gray-700 max-w-2xl mx-auto justify-center">
                    Surgió la pregunta, ¿Cómo la similitud compositiva de pinturas impresionistas varía según las características visuales de bajo nivel mediante representaciones vectoriales?
                </p>
            </div>

            <div className="space-y-8">
                {[
                    {
                        title: "Problemática",
                        content:
                            "En el análisis computacional de obras de arte, las características visuales de bajo nivel, como el color y la textura, son esenciales para preservar la coherencia estilística. Sin embargo, el uso inadecuado de transformaciones visuales para representar estas características puede distorsionar los elementos compositivos de las pinturas, especialmente en estilos sensibles como el impresionismo. A esto se suma la limitación de los modelos actuales, que priorizan patrones estructurales pero descuidan detalles visuales finos. Por ello, se requiere un enfoque que permita evaluar cómo cada transformación afecta la representación de estas características, utilizando representaciones vectoriales que capten mejor la variación en la similitud compositiva.",
                    },
                    {
                        title: "Importancia",
                        content:
                            "Esta experimentación es relevante porque enfrenta una limitación crítica en el análisis digital del arte: la elección incorrecta de transformaciones visuales puede comprometer la fidelidad de las representaciones. Al identificar cuáles transformaciones de color y textura preservan mejor la similitud compositiva en pinturas impresionistas, se contribuye a una representación más precisa de las obras, facilitando el desarrollo de herramientas digitales más confiables para su análisis y conservación.",
                    },
                ].map(({ title, content }, idx) => (
                    <div key={idx} className="flex items-start space-x-3 text-left">
                        <div className="w-12 h-12 flex items-center justify-center">
                            <Zap className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold mb-3 mt-2">{title}</h2>
                            <p className="text-gray-700 leading-relaxed text-justify">{content}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    </div>
);
