import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { RefreshCw } from "lucide-react";
import { formatSimilarity, getHighestSimilarity, getHighestTransformation } from "@/utils/similarity";
import { Button } from "@/components/ui/button";

interface SummarySectionProps {
  transformations: { similarity: number; name: string }[];
  onNext: () => void;
}

const SummarySection = ({ transformations, onNext }: SummarySectionProps) => {
  const highest = getHighestTransformation(transformations);

  return (
    <div className="text-center animate-fade-in-up">
      <Card className="p-8 max-w-2xl mx-auto mb-8 shadow-lg">
        <h3 className="text-xl font-serif font-bold text-gallery-800 mb-4">Resumen del Análisis</h3>
        <p className="text-gallery-600 mb-4">Mayor similitud composicional obtenida:</p>
        <div className="flex justify-center items-center space-x-4">
          <span className="text-lg font-medium text-gallery-700">{highest?.name}</span>
          <Badge className="bg-academic-600 text-white text-lg px-3 py-1">
            {formatSimilarity(getHighestSimilarity(transformations))}
          </Badge>
        </div>
      </Card>

      <Button onClick={onNext} size="lg" className="bg-gallery-700 hover:bg-gallery-800 text-white px-6 py-3 rounded-full shadow-lg hover:scale-105">
        <RefreshCw className="mr-2 h-5 w-5" />
        Siguiente Par de Pinturas
      </Button>
    </div>
  );
};

export default SummarySection;
