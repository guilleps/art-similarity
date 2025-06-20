export interface SimilarityTransformBlock {
    files: {
        image_1: string;
        image_2: string;
    };
    similarity: number;
}

export interface SimilarityParData {
    image_1: string;
    image_2: string;
    contrast?: SimilarityTransformBlock;
    texture?: SimilarityTransformBlock;
    heat_color_map?: SimilarityTransformBlock;
    hsv_hue?: SimilarityTransformBlock;
    hsv_saturation?: SimilarityTransformBlock;
    hsv_value?: SimilarityTransformBlock;
}

export interface ExportedSimilarityData {
    par: {
        [parId: string]: SimilarityParData;
    };
}
