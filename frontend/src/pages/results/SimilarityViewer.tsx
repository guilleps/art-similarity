import { useEffect, useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Award, RefreshCw } from "lucide-react";
import Header from "@/pages/Header";
import Image from "@/pages/Image";
import SummarySection from "./SummarySection";
import PaintingData from "@/types/painting";
import { fetchSimilarityData } from "@/services/similarityService";
import { getHighestSimilarity, formatSimilarity } from "@/utils/similarity";

const SimilarityViewer = () => {
  const [currentPairIndex, setCurrentPairIndex] = useState(0);
  const [showTransformations, setShowTransformations] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [data, setData] = useState<PaintingData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await fetchSimilarityData(data?.comparison_id);
        setData(result);
        setShowTransformations(true);
        setTimeout(() => setShowResults(true), 1000);
      } catch (err) {
        console.error("Error al cargar datos:", err);
      }
    };

    fetchData();
  }, []);

  const paintingPairs = useMemo(() => {
    if (!data || !data.similitud || !data.imagen_1 || !data.imagen_2) return [];

    const transformations = Object.keys(data.similitud).map((key) => ({
      name: {
        contrast: "Contraste",
        texture: "Textura",
        heat_color_map: "Mapa de Calor",
        hsv_hue: "Tono",
        hsv_saturation: "Saturación",
        hsv_value: "Brillo",
      }[key] || key,
      similarity: data.similitud[key].similarity,
      leftImage: data.imagen_1[key].image_transformed,
      rightImage: data.imagen_2[key].image_transformed,
    }));

    return [
      {
        id: 1,
        leftPainting: { image: data.imagen_1.original_image },
        rightPainting: { image: data.imagen_2.original_image },
        transformations,
      },
    ];
  }, [data]);

  const currentPair = paintingPairs.length > 0 ? paintingPairs[currentPairIndex] : null;

  const handleNextPair = async () => {
    try {
      const result = await fetchSimilarityData(data?.comparison_id);
      setData(result);
      setShowTransformations(false);
      setShowResults(false);
      setTimeout(() => setShowTransformations(true), 300);
      setTimeout(() => setShowResults(true), 1000);
    } catch (error) {
      console.error("Error al obtener comparación aleatoria", error);
    }
  };

  if (!currentPair) return null;

  return (
    <div className="max-w-7xl mx-auto">
      <Header currentPairIndex={currentPairIndex + 1} paintingPairs={paintingPairs.length} />

      {/* Main Images */}
      <div className={`grid md:grid-cols-2 gap-12 mb-12 transition-all duration-1000 ${showTransformations ? 'animate-fade-in-up' : 'opacity-0'}`}>
        <Image image={currentPair.leftPainting.image} />
        <Image image={currentPair.rightPainting.image} />
      </div>

      {/* Transformations Grid */}
      <div className={`grid grid-cols-2 md:grid-cols-3 gap-6 mb-12 transition-all duration-1000 ${showTransformations ? 'animate-fade-in-up' : 'opacity-0'}`}>
        {currentPair.transformations.map((transformation, index) => {
          const isHighest = transformation.similarity === getHighestSimilarity(currentPair.transformations);
          return (
            <Card
              key={index}
              className={`p-4 transition-all duration-500 ${showResults
                ? isHighest
                  ? 'animate-highlight border-academic-500 border-2 bg-academic-50'
                  : 'animate-scale-in'
                : 'opacity-0'
                }`}
              style={{ animationDelay: `${index * 200}ms` }}
            >
              <div className="grid grid-cols-2 gap-2 mb-3">
                <img src={transformation.leftImage} alt={`${transformation.name} izquierda`} className="w-full h-20 object-cover rounded aspect-square" />
                <img src={transformation.rightImage} alt={`${transformation.name} derecha`} className="w-full h-20 object-cover rounded aspect-square" />
              </div>
              <p className="text-sm font-medium text-gallery-700 mb-2 text-center">{transformation.name}</p>
              <div className="flex justify-center">
                <Badge variant={isHighest && showResults ? "default" : "secondary"} className={isHighest && showResults ? "bg-academic-600 text-white" : ""}>
                  {formatSimilarity(transformation.similarity)}
                </Badge>
                {isHighest && showResults && (
                  <Award className="h-4 w-4 text-academic-600 ml-2" />
                )}
              </div>
            </Card>
          );
        })}
      </div>

      {showResults && (
        <SummarySection
          transformations={currentPair.transformations}
          onNext={handleNextPair}
        />
      )}
    </div>
  );
};

export default SimilarityViewer;
