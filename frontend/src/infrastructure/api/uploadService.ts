import { toast } from 'sonner'
import { API_ROUTES } from '../constants/apiRoutes'
import client from './client'

export interface UploadReponse {
  secure_url: string
  similarities: string[]
}

export const uploadImage = async (file: File): Promise<UploadReponse> => {
  const formData = new FormData()
  formData.append('image', file)

  try {
    const response = await client.post<UploadReponse>('/upload/', formData)

    console.log('response.data', response.data)

    return response.data
  } catch (err: any) {
    console.error('Error al subir imagen:', err)

    const msg = err?.response?.data?.error || 'Error desconocido'
    toast.error(msg) // 👈 te dirá si es "No image provided", etc.
  }
}
