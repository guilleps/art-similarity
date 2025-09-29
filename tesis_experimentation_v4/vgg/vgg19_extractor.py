import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os


class VGG19EmbeddingExtractor:
    """
    Extractor de embeddings usando VGG-19 preentrenado.
    Puede extraer features de diferentes capas y calcular la Matriz de Gram.
    """

    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        """
        Inicializa el extractor VGG-19.

        Args:
            device: 'cuda' o 'cpu' para procesamiento
        """
        self.device = device

        # Cargar VGG-19 preentrenado con ImageNet
        self.model = models.vgg19(weights=models.VGG19_Weights.IMAGENET1K_V1).to(device)
        self.model.eval()  # Modo evaluación
        
        # Desactivar gradientes para inferencia
        for param in self.model.parameters():
            param.requires_grad = False

        # Definir las transformaciones estándar para VGG
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),  # VGG espera 224x224
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )

        # Definir capas de interés para extraer features
        self.feature_layers = {
            "conv1_1": 0,  # Características de muy bajo nivel (bordes, colores)
            "conv1_2": 2,
            "conv2_1": 5,  # Texturas simples
            "conv2_2": 7,
            "conv3_1": 10,  # Patrones más complejos
            "conv3_2": 12,
            "conv3_3": 14,
            "conv3_4": 16,
            "conv4_1": 19,  # Características de nivel medio
            "conv4_2": 21,
            "conv4_3": 23,
            "conv4_4": 25,
            "conv5_1": 28,  # Características de alto nivel
            "conv5_2": 30,
            "conv5_3": 32,
            "conv5_4": 34,
        }

    def load_image(self, image_path):
        """
        Carga y preprocesa una imagen.

        Args:
            image_path: Ruta completa a la imagen

        Returns:
            Tensor procesado listo para VGG-19
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path}")

        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        return image_tensor

    def compute_gram_matrix(self, features):
        """
        Calcula la Matriz de Gram para capturar estilo/textura.

        Args:
            features: Tensor de características [batch, channels, height, width]

        Returns:
            Matriz de Gram normalizada
        """
        batch_size, channels, height, width = features.size()

        # Reformatear features a matriz 2D
        features = features.view(batch_size * channels, height * width)

        # Calcular matriz de Gram (producto de features con su transpuesta)
        gram = torch.mm(features, features.t())

        # Normalizar por el número de elementos
        gram = gram.div(batch_size * channels * height * width)

        return gram

    def extract_features(self, image_path, layer_names=["conv4_2"]):
        """
        Extrae características de capas específicas.

        Args:
            image_path: Ruta a la imagen
            layer_names: Lista de nombres de capas de las que extraer features

        Returns:
            Dict con features por capa
        """
        # Cargar imagen
        image = self.load_image(image_path)

        # Almacenar features
        features = {}
        
        # Desactivar gradientes para inferencia
        with torch.no_grad():
            # Procesar por las capas convolucionales
            x = image
            for name, layer_idx in self.feature_layers.items():
                if name in layer_names:
                    # Aplicar capas hasta la deseada
                    for i in range(layer_idx + 1):
                        x = self.model.features[i](x)
                    features[name] = x.clone().detach()
                    x = image  # Reiniciar para siguiente capa si hay más
        
        return features

    def extract_embedding(self, image_path, method="fc", layer="fc2"):
        """
        Extrae un embedding de dimensión fija de una imagen.

        Args:
            image_path: Ruta a la imagen
            method: 'fc' para capas fully connected, 'conv' para convolucionales,
                   'gram' para matriz de Gram
            layer: Capa específica a usar

        Returns:
            Embedding como numpy array
        """
        image = self.load_image(image_path)

        if method == "fc":
            # Extraer de capas fully connected (clasificador)
            with torch.no_grad():
                # Pasar por todas las capas convolucionales
                x = self.model.features(image)
                x = self.model.avgpool(x)
                x = torch.flatten(x, 1)

                # Extraer de capas FC específicas
                if layer == "fc1":
                    x = self.model.classifier[0](x)  # Primera FC (4096-dim)
                    x = self.model.classifier[1](x)  # ReLU
                    x = self.model.classifier[2](x)  # Dropout
                elif layer == "fc2":
                    x = self.model.classifier[0](x)
                    x = self.model.classifier[1](x)
                    x = self.model.classifier[2](x)
                    x = self.model.classifier[3](x)  # Segunda FC (4096-dim)
                    x = self.model.classifier[4](x)  # ReLU
                    x = self.model.classifier[5](x)  # Dropout
                elif layer == "final":
                    x = self.model(image)  # Salida final (1000-dim)
                
                embedding = x.detach().cpu().numpy().flatten()
        
        elif method == 'conv':
            # Extraer de capa convolucional y aplanar
            features = self.extract_features(image_path, [layer])
            embedding = features[layer].detach().cpu().numpy().flatten()
        
        elif method == 'gram':
            # Usar matriz de Gram como embedding
            features = self.extract_features(image_path, [layer])
            gram = self.compute_gram_matrix(features[layer])
            embedding = gram.detach().cpu().numpy().flatten()
        
        else:
            raise ValueError(f"Método no reconocido: {method}")
        
        return embedding

    def extract_multi_scale_embedding(self, image_path, use_gram=True):
        """
        Extrae un embedding que combina múltiples escalas/capas.
        Ideal para capturar tanto detalles finos como patrones globales.

        Args:
            image_path: Ruta a la imagen
            use_gram: Si True, usa matrices de Gram; si False, usa features directas

        Returns:
            Embedding concatenado de múltiples capas
        """
        # Seleccionar capas de diferentes niveles
        layers = ["conv1_2", "conv2_2", "conv3_3", "conv4_3", "conv5_3"]

        embeddings = []
        features = self.extract_features(image_path, layers)

        for layer in layers:
            if use_gram:
                gram = self.compute_gram_matrix(features[layer])
                embedding = gram.detach().cpu().numpy().flatten()
            else:
                # Usar pooling para reducir dimensionalidad
                pooled = torch.nn.functional.adaptive_avg_pool2d(features[layer], (4, 4))
                embedding = pooled.detach().cpu().numpy().flatten()

            embeddings.append(embedding)

        # Concatenar todos los embeddings
        final_embedding = np.concatenate(embeddings)

        return final_embedding
