from vgg19_extractor import VGG19EmbeddingExtractor

# Crear el extractor
extractor = VGG19EmbeddingExtractor()

# Extraer embedding de una imagen
image_path = "./adalbert-erdeli_self-portrait_heatmap.jpg"
embedding = extractor.extract_embedding(image_path, method='gram', layer='conv4_2')

print(f"Embedding shape: {embedding.shape}")