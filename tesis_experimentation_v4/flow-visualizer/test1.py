import cv2
import numpy as np
import argparse

def apply_laplacian(image_path, output_path=None, ksize=3, scale=1, delta=0):
    """
    Apply Laplacian edge detection to an image.
    
    Args:
        image_path (str): Path to the input image
        output_path (str, optional): Path to save the result. If None, shows the result.
        ksize (int): Aperture size for the Laplacian operator. Must be odd.
        scale (float): Optional scale factor for computed Laplacian values
        delta (float): Optional delta value that is added to the results
    """
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Could not read the image. Please check the file path.")
    
    # Apply Gaussian blur to reduce noise
    img_blur = cv2.GaussianBlur(img, (3, 3), 0)
    
    # Apply Laplacian
    laplacian = cv2.Laplacian(img_blur, cv2.CV_64F, ksize=ksize, scale=scale, delta=delta)
    
    # Convert to absolute values and scale to 0-255
    laplacian_abs = cv2.convertScaleAbs(laplacian)
    
    # Show or save the result
    if output_path:
        cv2.imwrite(output_path, laplacian_abs)
        print(f"Result saved to {output_path}")
    else:
        cv2.imshow('Original', img)
        cv2.imshow('Laplacian Edges', laplacian_abs)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return laplacian_abs

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Apply Laplacian edge detection to an image.')
    parser.add_argument('image_path', type=str, help='Path to the input image')
    parser.add_argument('--output', type=str, default=None, 
                       help='Path to save the result (optional)')
    parser.add_argument('--ksize', type=int, default=3, 
                       help='Aperture size for the Laplacian operator (must be odd)')
    
    args = parser.parse_args()
    
    # Apply Laplacian
    try:
        apply_laplacian(args.image_path, args.output, args.ksize)
    except Exception as e:
        print(f"Error: {e}")