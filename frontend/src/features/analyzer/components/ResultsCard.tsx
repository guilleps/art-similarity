import React, { useState } from 'react'
import { AspectRatio } from '@/components/ui/aspect-ratio'
import type { Similarity } from '@/features/analyzer'

interface ResultsCardProps {
  imagePreview: string | null
  similarities: Similarity[]
}

// FC -> Componente funcional que recibe props explicitos
const ResultsCard: React.FC<ResultsCardProps> = ({
  imagePreview,
  similarities
}) => {
  const [erroredImages, setErroredImages] = useState<{ [key: string]: boolean }>({})

  const handleImageError = (id: string) => {
    setErroredImages((prev) => ({ ...prev, [id]: true }))
  }

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
                    {!erroredImages[similarity.similar_image_id] ? (
                      <img
                        src={similarity.similar_image_url}
                        className="h-full w-full object-cover"
                        onError={() =>
                          handleImageError(similarity.similar_image_id)
                        }
                        alt={`Obra similar ${similarity.similar_image_id}`}
                      />
                    ) : (
                      <div className="h-full w-full animate-pulse bg-gradient-to-r from-[#1f2a4d] via-[#263355] to-[#1f2a4d] flex items-center justify-center text-white/40 text-sm" />
                    )}
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
