import { AxiosResponse } from 'axios';

export const getSimilaritiesByIdMock = (comparison_id: string) => {
	return {
		comparison_id,
		image_1: {
			original_image:
				'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825864/ftbfcramvyjjlfrjttnu.jpg',
			contrast: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825867/uoiez9wfm3qoa8pozb7c.jpg',
			},
			texture: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825867/dm4oocw2btixnssn9mgw.jpg',
			},
			heat_color_map: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825868/vl5xvv4q91tkovvy9wv8.jpg',
			},
			hsv_hue: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825869/t3ilbee3sonrn28ehpwk.jpg',
			},
			hsv_saturation: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825870/qowpdzbb2xvutiwlv7dp.jpg',
			},
			hsv_value: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825872/oql95yx8pjxn2ojnylxw.jpg',
			},
		},
		image_2: {
			original_image:
				'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825865/cxz6pr3ri9swz03dcrla.jpg',
			contrast: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825873/ihhwnyhyxs5ow8jdzfin.jpg',
			},
			texture: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825874/wkvb0ldtyphuwfr5udx8.jpg',
			},
			heat_color_map: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825874/ohg4tqgeix5bedb1jjkf.jpg',
			},
			hsv_hue: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825875/byjxinlc9wnjcla73tc8.jpg',
			},
			hsv_saturation: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825876/cu3m40gb3ugd9b8ihjdi.jpg',
			},
			hsv_value: {
				image_transformed:
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825876/ro8wxlfjtxlzfgfuetvq.jpg',
			},
		},
		similitud: {
			texture: {
				files: [
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825867/dm4oocw2btixnssn9mgw.jpg',
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825874/wkvb0ldtyphuwfr5udx8.jpg',
				],
				similarity: 0.9591,
			},
			contrast: {
				files: [
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825867/uoiez9wfm3qoa8pozb7c.jpg',
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825873/ihhwnyhyxs5ow8jdzfin.jpg',
				],
				similarity: 0.8903,
			},
			hsv_hue: {
				files: [
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825869/t3ilbee3sonrn28ehpwk.jpg',
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825875/byjxinlc9wnjcla73tc8.jpg',
				],
				similarity: 0.9294,
			},
			hsv_saturation: {
				files: [
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825870/qowpdzbb2xvutiwlv7dp.jpg',
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825876/cu3m40gb3ugd9b8ihjdi.jpg',
				],
				similarity: 0.9107,
			},
			hsv_value: {
				files: [
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825872/oql95yx8pjxn2ojnylxw.jpg',
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825876/ro8wxlfjtxlzfgfuetvq.jpg',
				],
				similarity: 0.8937,
			},
			heat_color_map: {
				files: [
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825868/vl5xvv4q91tkovvy9wv8.jpg',
					'https://res.cloudinary.com/dnydakj9z/image/upload/v1756825874/ohg4tqgeix5bedb1jjkf.jpg',
				],
				similarity: 0.9226,
			},
		},
	};
};

export const getSimilaritiesByIdMocks = async (
	comparison_id: string,
): Promise<AxiosResponse<typeof getSimilaritiesByIdMock>> => {
	return {
		data: getSimilaritiesByIdMock(comparison_id),
		status: 200,
		statusText: 'OK',
		headers: {},
		config: {},
	} as unknown as AxiosResponse<typeof getSimilaritiesByIdMock>;
};
