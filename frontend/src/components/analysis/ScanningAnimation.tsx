/* eslint-disable prettier/prettier */
import React, { useEffect, useState } from 'react'
import PixelScannerOverlay from './PixelScannerOverlay'

interface ScanningAnimationProps {
  isComplete?: boolean
  onComplete?: () => void
  imagePreview?: string | null
  onBack?: () => void
}

// FC -> Componente funcional que recibe props explicitos
const ScanningAnimation: React.FC<ScanningAnimationProps> = ({
  isComplete = false,
  onComplete,
  imagePreview,
  onBack
}) => {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    if (isComplete && onComplete) {
      onComplete()
    }
  }, [isComplete, onComplete])

  return (
    <div className="mx-auto w-full max-w-xl px-4 md:px-0">
      {onBack && (
        <button
          onClick={onBack}
          className="mb-6 inline-flex items-center text-white/70 transition-colors duration-200 hover:text-white"
        >
          <span>Volver</span>
        </button>
      )}

      <div className="flex flex-col items-center">
        <h2 className="mb-3 text-2xl font-bold text-white md:text-3xl">
          Analizando...
        </h2>
        <p className="mb-8 text-center text-white/60">
          Espere un momento, nuestro algoritmo está analizando la composición en
          busca de similitudes con otras obras.
        </p>

        <div className="relative flex justify-center items-center">
          {imagePreview && (
            <div className="relative max-h-80 w-auto">
              <img
                src={imagePreview}
                alt="Obra de arte cargada"
                className="block max-h-80 object-contain"
              />
              <div className="absolute inset-0">
                <PixelScannerOverlay />
              </div>
            </div>
          )}
        </div>

        
      </div>
    </div>
  )
}

export default ScanningAnimation
