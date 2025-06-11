import { useEffect, useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Award, RefreshCw } from "lucide-react";
import PaintingData from "@/types/painting";
import { getSimilaritiesById } from "@/services/similarity.service";
import { getHighestSimilarity, formatSimilarity } from "@/utils/similarity";
import { Image } from "./Image";
import { SkeletonCard } from "./SkeletonCard";

interface Props {
  comparisonId: string;
}

const SimilarityViewer = ({ comparisonId }: Props) => {
  const [currentPairIndex, setCurrentPairIndex] = useState(0);
  const [showTransformations, setShowTransformations] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [data, setData] = useState<PaintingData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      const result = await getSimilaritiesById(comparisonId);
      setData(result);
    };
    fetchData();
  }, [comparisonId]);

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

  // const paintingPairs = [
  //   {
  //     "id": 1,
  //     "leftPainting": {
  //       "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop"
  //     },
  //     "rightPainting": {
  //       "image": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=400&fit=crop"
  //     },
  //     "transformations": [
  //       {
  //         "name": "Mapa de Calor",
  //         "similarity": 0.92,
  //         "leftImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=30",
  //         "rightImage": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=200&fit=crop&hue=30"
  //       },
  //       {
  //         "name": "Tono",
  //         "similarity": 0.87,
  //         "leftImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=60",
  //         "rightImage": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=200&fit=crop&hue=60"
  //       },
  //       {
  //         "name": "Saturación",
  //         "similarity": 0.95,
  //         "leftImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&saturation=1.3",
  //         "rightImage": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=200&fit=crop&saturation=1.3"
  //       },
  //       {
  //         "name": "Brillo",
  //         "similarity": 0.78,
  //         "leftImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&brightness=1.3",
  //         "rightImage": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=200&fit=crop&brightness=1.3"
  //       },
  //       {
  //         "name": "Contraste",
  //         "similarity": 0.89,
  //         "leftImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&contrast=1.4",
  //         "rightImage": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=200&fit=crop&contrast=1.4"
  //       },
  //       {
  //         "name": "Textura",
  //         "similarity": 0.83,
  //         "leftImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&blur=1",
  //         "rightImage": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=200&h=200&fit=crop&blur=1"
  //       }
  //     ]
  //   },
  //   {
  //     "id": 2,
  //     "leftPainting": {
  //       "image": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=400&h=400&fit=crop"
  //     },
  //     "rightPainting": {
  //       "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&hue=180"
  //     },
  //     "transformations": [
  //       {
  //         "name": "Mapa de Calor",
  //         "similarity": 0.88,
  //         "leftImage": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=200&h=200&fit=crop&hue=30",
  //         "rightImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=180&hue=30"
  //       },
  //       {
  //         "name": "Tono",
  //         "similarity": 0.94,
  //         "leftImage": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=200&h=200&fit=crop&hue=60",
  //         "rightImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=180&hue=60"
  //       },
  //       {
  //         "name": "Saturación",
  //         "similarity": 0.86,
  //         "leftImage": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=200&h=200&fit=crop&saturation=1.3",
  //         "rightImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=180&saturation=1.3"
  //       },
  //       {
  //         "name": "Brillo",
  //         "similarity": 0.79,
  //         "leftImage": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=200&h=200&fit=crop&brightness=1.3",
  //         "rightImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=180&brightness=1.3"
  //       },
  //       {
  //         "name": "Contraste",
  //         "similarity": 0.91,
  //         "leftImage": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=200&h=200&fit=crop&contrast=1.4",
  //         "rightImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=180&contrast=1.4"
  //       },
  //       {
  //         "name": "Textura",
  //         "similarity": 0.97,
  //         "leftImage": "https://images.unsplash.com/photo-1578321272176-b7bbc0679853?w=200&h=200&fit=crop&blur=1",
  //         "rightImage": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=200&h=200&fit=crop&hue=180&blur=1"
  //       }
  //     ]
  //   }
  // ]

  const currentPair = paintingPairs.length > 0 ? paintingPairs[currentPairIndex] : null;

  if (!currentPair) return null

  return (
    <div className="max-w-7xl mx-auto">

      {/* Main Images */}
      <div className={`grid md:grid-cols-2 gap-12 mb-12 transition-all duration-1000 ${showTransformations ? 'opacity-100' : 'opacity-0'}`}>
        <Image image={currentPair.leftPainting.image} />
        <Image image={currentPair.rightPainting.image} />
      </div>

      {/* Transformations Grid */}
      <div className="overflow-hidden transition-all duration-700 ease-in-out mb-12opacity-100 max-h-[1000px]">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
          {currentPair.transformations.map((transformation, index) => {
            const isHighest = transformation.similarity === getHighestSimilarity(currentPair.transformations);
            return (
              <Card
                key={index}
                className={`p-4 transition-all duration-500 ${showResults
                  ? isHighest
                    ? 'animate-highlight border-academic-500 border-2 bg-academic-50'
                    : 'animate-scale-in'
                  : ''
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
      </div>
    </div >
  );
};

export default SimilarityViewer;
