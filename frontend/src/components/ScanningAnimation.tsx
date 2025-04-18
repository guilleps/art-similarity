import React, { useEffect, useState } from 'react'

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
      return
    }

    const totalDuration = 6000 // 6 segundos
    const interval = 100 // intervalo 100ms
    const totalSteps = totalDuration / interval
    let currentStep = 0

    const timer = setInterval(() => {
      currentStep++
      const newProgress = Math.min(
        100,
        Math.floor((currentStep / totalSteps) * 100)
      )
      setProgress(newProgress)

      if (currentStep >= totalSteps) {
        clearInterval(timer)
        if (onComplete) onComplete()
      }
    }, interval)

    return () => clearInterval(timer)
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

        <div className="relative mx-auto mb-8 w-full max-w-md">
          {imagePreview && (
            <div className="flex justify-center">
              <img
                src={imagePreview}
                alt="Obra de arte cargada"
                className="max-h-80 object-contain"
              />
            </div>
          )}
        </div>

        {/* Barra de progreso */}
        <div className="relative h-2 w-full max-w-md overflow-hidden rounded-full bg-[#1a2342]">
          <div
            className="h-full bg-gradient-to-r from-purple-500 to-blue-400"
            style={{ width: `${progress}%`, transition: 'width 0.3s ease-out' }}
          ></div>
        </div>
        <div className="mt-1 flex w-full max-w-md justify-end">
          <span className="text-sm text-blue-400">{progress}%</span>
        </div>
      </div>
    </div>
  )
}

export default ScanningAnimation
