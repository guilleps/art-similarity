import { toast } from 'sonner'
import client from './client'
import { UploadResponse } from '@/domain/models'

export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('image', file)

  try {
    const response = await client.post<UploadResponse>('/upload/', formData)

    if (import.meta.env.MODE === 'development') {
      console.log('image_analize', response.data['image_analize'])
      console.log('similarities', response.data['similarities'])
    }

    return response.data
  } catch (err: any) {
    const msg = err?.response?.data?.error || 'Error inesperado'
    throw msg
  }
}
