import React from 'react'
import { AspectRatio } from '@/components/ui/aspect-ratio'
import { SimilarityResult } from '@/infrastructure/api/uploadService'

interface ResultsCardProps {
  imagePreview: string | null
  similarities: SimilarityResult[]
}

// FC -> Componente funcional que recibe props explicitos
const ResultsCard: React.FC<ResultsCardProps> = ({
  imagePreview,
  similarities
}) => {
  return (
    <div className="mx-auto mb-8 w-full max-w-4xl space-y-6">
      <h2 className="md:text-1xl mb-3 text-center text-xl font-bold text-white">
        Análisis de Similitud
      </h2>

      <div className="mb-8 flex justify-center">
        {imagePreview ? (
          <img
            src={imagePreview}
            alt="Imagen Analizada"
            className="max-h-60 object-contain"
          />
        ) : (
          <div className="flex h-40 w-40 items-center justify-center bg-[#1a2342]">
            <p className="text-white/60">No hay imagen</p>
          </div>
        )}
      </div>

      {/* Similar works section */}
      <div className="space-y-4">
        <h3 className="mb-6 text-center text-xl font-medium text-white">
          Obras Similares
        </h3>

        <div className="flex flex-wrap justify-center gap-4 md:gap-6">
          {similarities.map((similarity) => (
            <div
              key={similarity.similar_image_id}
              className="w-full max-w-[250px] md:w-1/3"
            >
              <div className="group relative w-full">
                <AspectRatio ratio={1 / 1}>
                  <div className="h-full w-full bg-[#1a2342]">
                    <img
                      src={similarity.similar_image_url}
                      className="h-full w-full object-cover"
                    />
                  </div>
                </AspectRatio>
                <p className="mt-2 text-center text-base font-medium text-white">
                  {similarity.similarity_percentage} %
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ResultsCard
