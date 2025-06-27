export interface PaintingImage {
    original_image: string;
    transformations: {
        [transformation: string]: { image_transformed: string };
    };
}

export interface PaintingSimilarity {
    [transformation: string]: {
        similarity: number;
    };
}

export default interface PaintingData {
    comparison_id: string;
    image_1: PaintingImage;
    image_2: PaintingImage;
    similitud: PaintingSimilarity;
    total?: number;
    current_index?: number;
}
