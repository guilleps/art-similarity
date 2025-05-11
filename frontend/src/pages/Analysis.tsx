import { useState, useEffect, useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import UploadArea from '@/components/UploadArea'
import ScanningAnimation from '@/components/ScanningAnimation'
import ResultsCard from '@/components/ResultsCard'
import Footer from '@/components/Footer'
import Header from '@/components/Header'
import { applyBodyGradient, resetBodyGradient } from '@/lib/body-analysis'
import {
  SimilarityResult,
  uploadImage
} from '@/infrastructure/api/uploadService'

const Analysis = () => {
  const [currentStep, setCurrentStep] = useState<
    'upload' | 'scanning' | 'results'
  >('upload')
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [similarities, setSimilarities] = useState<SimilarityResult[]>([])
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    applyBodyGradient()
    return () => resetBodyGradient()
  }, [])

  const handleNavigationFromUpload = useCallback(() => {
    const params = new URLSearchParams(window.location.search)
    const state = location.state as { imagePreview?: string } | null

    if (params.get('from') === 'upload') {
      if (state?.imagePreview) {
        setImagePreview(state.imagePreview)
      }

      setCurrentStep('scanning')
      setTimeout(() => setCurrentStep('results'), 6000)
    }
  }, [location])

  useEffect(() => {
    handleNavigationFromUpload()
  }, [location, handleNavigationFromUpload])

  const handleBack = () => {
    setCurrentStep('upload')
    setImagePreview(null)
  }

  const handleImageUpload = async (file: File) => {
    try {
      const response = await uploadImage(file) // Llamada a la API de subida de imagen
      if (response) {
        // Actualizar el estado de similitudes con la respuesta de la API
        setSimilarities(response.similarities)
        setCurrentStep('scanning') // Cambiar al paso de escaneo
        setTimeout(() => setCurrentStep('results'), 6000)
      }
    } catch (error) {
      console.error('Error al cargar la imagen:', error)
    }
  }

  const renderStepContent = () => {
    switch (currentStep) {
      case 'upload':
        return (
          <UploadArea
            onBack={() => navigate('/')}
            onUpload={handleImageUpload}
          />
        )
      case 'scanning':
        return (
          <ScanningAnimation
            imagePreview={imagePreview}
            onComplete={() => setCurrentStep('results')}
            onBack={handleBack}
          />
        )
      case 'results':
        return (
          <ResultsCard
            imagePreview={imagePreview}
            similarities={similarities}
          />
        )
    }
  }

  return (
    <div className="flex min-h-screen flex-col bg-gradient-radial from-[#10183d] to-[#080e24]">
      <Header completed={false} />

      <main className="min-w-screen flex flex-1 flex-col items-center justify-center px-4 py-0 md:px-8">
        <div className="container mx-auto w-full max-w-6xl">
          {currentStep === 'results' && (
            <div className="mb-6">
              <button
                onClick={handleBack}
                className="inline-flex items-center text-white/70 transition-colors duration-200 hover:text-white"
              >
                <span>Cargar otra imagen</span>
              </button>
            </div>
          )}

          {renderStepContent()}
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default Analysis
