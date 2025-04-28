import { toast } from 'sonner'
import { API_ROUTES } from '../constants/apiRoutes'
import client from './client'

export interface SimilarityResult {
  similar_image_id: string
  similar_image_url: string
  similarity_percentage: number
}

export interface UploadResponse {
  image_analyze: {
    id: string
    url: string
  }
  similarities: SimilarityResult[]
}

export const uploadImage = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('image', file)

  try {
    const response = await client.post<UploadResponse>('/upload/', formData)

    console.log('image_analize', response.data['image_analize'])
    console.log('similarities', response.data['similarities'])

    return response.data
  } catch (err: any) {
    console.error('Error al subir imagen:', err)

    const msg = err?.response?.data?.error || 'Error desconocido'
    toast.error(msg)
    throw err
  }
}
