import client from './client'
import { UploadResponse } from '@/domain/models'

export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('image', file)

  // console.log('📤 Enviando archivo al backend...', file)

  try {
    const response = await client.post<UploadResponse>('/upload/', formData)
    
    // console.log('image_analize', response.data['image_analize'])
    // console.log('similarities', response.data['similarities'])

    return response.data
  } catch (err: any) {
    // console.error('❌ Error al subir imagen:', err)
    const msg = err?.response?.data?.error || 'Error inesperado'
    throw msg
  }
}
