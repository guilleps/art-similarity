import { useUploadHandler } from '@/hooks/useUploadHandler'
import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

interface UploadAreaProps {
  onBack?: () => void
  onUpload?: (file: File) => Promise<boolean>
}

// FC -> Componente funcional que recibe props explicitos
const UploadArea: React.FC<UploadAreaProps> = ({ onBack, onUpload }) => {
  const [dragging, setDragging] = useState(false)
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  const { processFile } = useUploadHandler(onUpload)

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setDragging(false)
  }

  const handleFile = (file: File) => {
    setFile(file)
    const reader = new FileReader()

    reader.onload = async (e) => {
      if (!e.target?.result) return

      const previewUrl = e.target.result as string
      setPreview(previewUrl)

      navigate('/analysis?from=upload', {
        state: { imagePreview: previewUrl, file }
      })
    }

    reader.readAsDataURL(file)
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) handleFile(e.target.files[0])
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setDragging(false)
    if (e.dataTransfer.files?.[0]) handleFile(e.dataTransfer.files[0])
  }

  const openFileDialog = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  return (
    <div className="mx-auto w-full max-w-2xl p-8 text-center">
      {onBack && (
        <div className="mb-4 w-full text-left">
          <button
            onClick={() => navigate('/')}
            className="inline-flex items-center text-white/70 transition-colors duration-200 hover:text-white"
          >
            <span>Volver</span>
          </button>
        </div>
      )}

      <h2 className="mb-3 text-2xl font-bold text-white md:text-3xl">
        Carga tu obra de arte
      </h2>
      <p className="mb-6 text-white/60">
        Sube una imagen para analizar su composición.
      </p>

      <div
        className={`border-2 ${
          dragging ? 'border-blue-400' : 'border-white/10'
        } rounded-lg border-dashed bg-[#0a1128]/50 p-10 transition-all duration-300`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="flex flex-col items-center justify-center gap-4">
          <h3 className="text-xl font-medium text-white">Arrastre y suelte</h3>

          <p className="my-8 max-w-md text-sm text-white/60">
            Cargue una imagen digital de su obra para analizar su composición
            visual y buscar similitudes con otras obras artísticas
          </p>

          <button
            onClick={openFileDialog}
            className="mt-4 flex items-center gap-2 rounded-full border border-blue-400/20 bg-[#1a2342] px-5 py-2.5 text-white transition-colors duration-300 hover:bg-[#232d54]"
          >
            <span className="text-sm">Seleccionar imagen</span>
          </button>

          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            className="hidden"
            accept="image/jpeg,image/jpg,image/png"
          />
        </div>
      </div>
    </div>
  )
}

export default UploadArea
