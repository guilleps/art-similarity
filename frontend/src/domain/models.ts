/* eslint-disable prettier/prettier */
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
