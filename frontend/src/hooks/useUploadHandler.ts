/* eslint-disable prettier/prettier */
import React from 'react'
import { toast } from 'sonner'

type ProcessFileFn = (
  file: File,
  setLoading: (l: boolean) => void,
  setPreview: (s: string) => void,
  onSuccess: (imagePreview: string) => void
) => Promise<void>

export const useUploadHandler = (
  onUpload?: (file: File) => Promise<boolean>
): { processFile: ProcessFileFn } => {
  const processFile: ProcessFileFn = async (file, setProcessing, setPreview, onSuccess) => {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
    if (!allowedTypes.includes(file.type)) {
      toast.custom(
        (t) => (
          React.createElement(
            'div',
            { className: 'bg-red-600 text-white px-4 py-2 rounded-md border' },
            'Fomato inválido. Vuelva a intentarlo'
          )
        ),
        { duration: 6000 }
      )
      return
    }

    const reader = new FileReader()

    reader.onload = async (e) => {
      if (!e.target?.result) return

      const previewUrl = e.target?.result as string
      setPreview(previewUrl)
      setProcessing(true)

      try {
        const success = await onUpload?.(file)
        if (success) {
          onSuccess(previewUrl)
        } else {
          setProcessing(false)
          toast.custom(
            (t) => (
              React.createElement(
                'div',
                { className: 'bg-red-600 text-white px-4 py-2 rounded-md border' },
                'Hubo un error crítico al subir tu imagen. Intenta nuevamente.'
              )
            ),
            { duration: 6000 }
          )
        }
      } catch {
        toast.error('Error inesperado.')
      }
    }

    reader.readAsDataURL(file)
  }

  return { processFile }
}