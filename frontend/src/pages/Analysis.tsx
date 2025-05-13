/* eslint-disable prettier/prettier */
import { useState, useEffect, useCallback } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import UploadArea from '@/components/analysis/UploadArea'
import ScanningAnimation from '@/components/analysis/ScanningAnimation'
import ResultsCard from '@/components/analysis/ResultsCard'
import Footer from '@/components/layout/Footer'
import Header from '@/components/layout/Header'
import { applyBodyGradient, resetBodyGradient } from '@/lib/body-analysis'
import { uploadImage } from '@/infrastructure/api/uploadService'
import { SimilarityResult } from '@/domain/models'
import { toast } from "sonner";
import React from 'react'

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
      if (!state?.imagePreview) {
        navigate('/')
        return
      }

      setImagePreview(state.imagePreview)
      setCurrentStep('scanning')
      setTimeout(() => setCurrentStep('results'), 6000)
    }
  }, [location.state, navigate])

  useEffect(() => {
    handleNavigationFromUpload()
  }, [location, handleNavigationFromUpload])

  const handleBack = () => {
    setCurrentStep('upload')
    setImagePreview(null)
  }

  const handleImageUpload = async (file: File): Promise<boolean> => {
    setImagePreview(URL.createObjectURL(file))
    setCurrentStep('scanning')

    try {
      const response = await uploadImage(file)
      if (response && response.similarities.length > 0) {
        setSimilarities(response.similarities)
        setCurrentStep('results')
        return true
      } else {
        toast.custom(
          (t) => (
            React.createElement(
              'div',
              { className: 'bg-red-600 text-white px-4 py-2 rounded-md border' },
              'No se encontraron similitudes'
            )
          ),
          { duration: 6000 }
        )
        setCurrentStep('upload')
        return false
      }
    } catch (error) {
      toast.custom(
        (t) => (
          React.createElement(
            'div',
            { className: 'bg-red-600 text-white px-4 py-2 rounded-md border' },
            'Error al analizar la imagen'
          )
        ),
        { duration: 6000 }
      )
      setCurrentStep('upload')
      return false
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
