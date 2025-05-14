import { UploadResponseSchema } from '../schemas/upload.schema'
import client from './client'

export const uploadImage = async (file: File) => {
  const formData = new FormData()
  formData.append('image', file)

  // console.log('📤 Enviando archivo al backend...', file)

  try {
    const response = await client.post('/upload/', formData)

    // console.log({ 'image_analize': response.data['image_analize'], 'similarities': response.data['similarities'] })

    const parsed = UploadResponseSchema.parse(response.data)

    return parsed
  } catch (err: any) {
    if (err.name === 'ZodError') {
      // console.error('❌ Error de validación Zod:', err.errors)
      throw new Error('La respuesta del servidor no es válida')
    }

    const msg = err?.response?.data?.error || 'Error inesperado'
    throw new Error(msg)
  }
}
