import { z } from "zod";

export const UploadResponseSchema = z.object({
    image_analize: z.object({
        id: z.string(),
        url: z.string().url(),
    }),
    similarities: z.array(
        z.object({
            similar_image_id: z.string(),
            similar_image_url: z.string().url(),
            similarity_percentage: z.number()
        })
    )
})

export type UploadResponse = z.infer<typeof UploadResponseSchema>
export type Similarity = UploadResponse['similarities'][number]
