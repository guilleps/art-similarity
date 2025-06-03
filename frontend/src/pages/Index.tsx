import { useState, useEffect, useMemo } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Play, RefreshCw, Award } from 'lucide-react';
import Image from './Image';
import Header from './Header';
import PaintingData from '@/types/painting';
import { formatSimilarity, getHighestSimilarity, getHighestTransformation } from '@/utils/similarity';
import { fetchSimilarityData } from "@/services/similarityService";

const Index = () => {
  const [currentStep, setCurrentStep] = useState<'intro' | 'analysis'>('intro');
  const [currentPairIndex, setCurrentPairIndex] = useState(0);
  const [showTransformations, setShowTransformations] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [data, setData] = useState<PaintingData | null>(null);

  useEffect(() => {
    const fetchInitial = async () => {
      try {
        const result = await fetchSimilarityData();
        setData(result);
      } catch (err) {
        console.error('Error al cargar datos:', err);
      }
    };

    fetchInitial();
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
  console.log(paintingPairs);

  const currentPair = paintingPairs.length > 0 ? paintingPairs[currentPairIndex] : null;

  const handleStart = () => {
    setCurrentStep('analysis');
    setTimeout(() => setShowTransformations(true), 500);
    setTimeout(() => setShowResults(true), 1500);
  };

  const handleNextPair = async () => {
    try {
      const result = await fetchSimilarityData();
      setData(result);
    } catch (err) {
      console.error("Error al obtener comparación aleatoria", err);
    }
  };

  if (currentStep === 'intro') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gallery-50 to-academic-100 flex items-center justify-center p-8">
        <div className="text-center max-w-4xl mx-auto animate-fade-in">
          {/* Title */}
          <h1 className="text-5xl md:text-6xl font-serif font-bold text-gallery-800 mb-6 leading-tight">
            Análisis de Similitud Composicional
            <span className="text-academic-600 block">en Pinturas Impresionistas</span>
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gallery-600 mb-12 leading-relaxed max-w-3xl mx-auto">
            Resultados de la comparación de transformaciones aplicadas según características visuales de bajo nivel
          </p>

          {/* Start Button */}
          <Button
            onClick={handleStart}
            size="lg"
            className="bg-academic-600 hover:bg-academic-700 text-white px-8 py-4 text-lg font-medium rounded-full shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-xl"
          >
            <Play className="mr-2 h-5 w-5" />
            Comenzar
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gallery-50 to-academic-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <Header currentPairIndex={currentPairIndex + 1} paintingPairs={paintingPairs.length} ></Header>

        {/* Main Images */}
        <div className={`grid md:grid-cols-2 gap-12 mb-12 transition-all duration-1000 ${showTransformations ? 'animate-fade-in-up' : 'opacity-0'}`}>
          {/* Left Main Image */}
          <Image image={currentPair.leftPainting.image} ></Image>

          {/* Right Main Image */}
          <Image image={currentPair.rightPainting.image} ></Image>
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
                  <img
                    src={transformation.leftImage}
                    alt={`${transformation.name} izquierda`}
                    className="w-full h-20 object-cover rounded aspect-square"
                  />
                  <img
                    src={transformation.rightImage}
                    alt={`${transformation.name} derecha`}
                    className="w-full h-20 object-cover rounded aspect-square"
                  />
                </div>
                <p className="text-sm font-medium text-gallery-700 mb-2 text-center">{transformation.name}</p>
                <div className="flex justify-center">
                  <Badge
                    variant={isHighest && showResults ? "default" : "secondary"}
                    className={isHighest && showResults ? "bg-academic-600 text-white" : ""}
                  >
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

        {/* Summary and Controls */}
        {showResults && (
          <div className="text-center animate-fade-in-up">
            <Card className="p-8 max-w-2xl mx-auto mb-8 shadow-lg">
              <h3 className="text-xl font-serif font-bold text-gallery-800 mb-4">Resumen del Análisis</h3>
              <p className="text-gallery-600 mb-4">
                Mayor similitud composicional obtenida:
              </p>
              <div className="flex justify-center items-center space-x-4">
                <span className="text-lg font-medium text-gallery-700">
                  {getHighestTransformation(currentPair.transformations)?.name}
                </span>
                <Badge className="bg-academic-600 text-white text-lg px-3 py-1">
                  {formatSimilarity(getHighestSimilarity(currentPair.transformations))}
                </Badge>
              </div>
            </Card>

            <Button
              onClick={handleNextPair}
              size="lg"
              className="bg-gallery-700 hover:bg-gallery-800 text-white px-6 py-3 rounded-full shadow-lg transform transition-all duration-300 hover:scale-105"
            >
              <RefreshCw className="mr-2 h-5 w-5" />
              Siguiente Par de Pinturas
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;
