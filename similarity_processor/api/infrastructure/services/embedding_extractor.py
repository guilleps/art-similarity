import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import logging

logger = logging.getLogger(__name__)


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

    # Extract features from the second fully connected layer (fc2) of VGG-19
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


extractor = VGG19EmbeddingExtractor()

# Generate embedding using VGG-19's fc2 layer
def generate_embedding(image_path: str) -> list:
    return extractor.extract_embedding(image_path)
