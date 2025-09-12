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
	analysis?: {
		best_transformation: {
			type: string;
			similarity: number;
			label: string;
			image_1_url: string;
			image_2_url: string;
		};
		explanation: string;
	};
	total?: number;
	current_index?: number;
}
