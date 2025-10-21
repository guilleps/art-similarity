import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels
)
import shutil

class VGG19EmbeddingExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = models.vgg19(weights=models.VGG19_Weights.IMAGENET1K_V1).to(
            self.device
        )
        self.model.eval()

        # Freeze all parameters
        for param in self.model.parameters():
            param.requires_grad = False

        # Define image transformations
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

    def extract_embedding(self, image_path: str) -> list:
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert("RGB")
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)

            # Extract features
            with torch.no_grad():
                # Forward pass through feature extractor
                x = self.model.features(image_tensor)
                x = self.model.avgpool(x)
                x = torch.flatten(x, 1)

                # Pass through classifier layers up to fc2
                x = self.model.classifier[0](x)
                x = self.model.classifier[1](x)
                x = self.model.classifier[2](x)
                x = self.model.classifier[3](x)
                x = self.model.classifier[4](x)
                x = self.model.classifier[5](x)

                # Convert to numpy array and then to list
                embedding = x.cpu().numpy().flatten().tolist()

            return embedding

        except Exception as e:
            logger.exception("Error extracting VGG-19 features:")
            raise

def apply_transformations(image):
    # Aplicar transformaciones (igual que en el código original)
    contrast = apply_contrast_enhancement(image)
    texture = apply_texture_direction(image)
    heatmap = apply_color_distribution_map(image)
    hsv = apply_hsv_channels(image)
    
    return {
        'original': image,
        'contrast': contrast,
        'texture': texture,
        'heatmap': heatmap,
        'hue': hsv['hue'],
        'saturation': hsv['saturation'],
        'value': hsv['value']
    }

def main():
    extractor = VGG19EmbeddingExtractor()
    
    # Example usage
    image1_path = "./images/antoine-blanchard_boulevard-de-la-madeleine-2.jpg"
    image2_path = "./images/antoine-blanchard_boulevard-de-la-madeleine-9.jpg"
    
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    # Apply transformations
    transforms1 = apply_transformations(img1)
    transforms2 = apply_transformations(img2)
    
    # Save transformed images temporarily
    os.makedirs("temp_transformed", exist_ok=True)
    
    # Solo estas transformaciones se compararán
    transform_names = ['contrast', 'texture', 'heatmap', 'hue', 'saturation', 'value']
    
    for name in transform_names:
        # Guardar imágenes transformadas temporalmente
        path1 = f"temp_transformed/img1_{name}.jpg"
        path2 = f"temp_transformed/img2_{name}.jpg"
        
        if (name == 'heatmap'):
            plt.imsave(path1, transforms1[name])
            plt.imsave(path2, transforms2[name])
        else:
            cv2.imwrite(path1, transforms1[name])
            cv2.imwrite(path2, transforms2[name])
        
        try:
            # Extraer embeddings
            emb1 = extractor.extract_embedding(path1)
            emb2 = extractor.extract_embedding(path2)
            
            # Calcular similitud
            similarity = cosine_similarity([emb1], [emb2])[0][0]
            print(f"Similitud para {name}: {similarity:.4f}")
            
        except Exception as e:
            print(f"Error procesando {name}: {str(e)}")
            
        # Eliminar archivos temporales
        os.remove(path1)
        os.remove(path2)
    
    # Eliminar directorio temporal
    shutil.rmtree("temp_transformed")

if __name__ == "__main__":
    main()