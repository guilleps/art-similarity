import os
import numpy as np
from pathlib import Path
from typing import List, Tuple
import torch
from PIL import Image
import faiss
from transformers import CLIPProcessor, CLIPModel
from tqdm import tqdm
import pickle


class ArtSimilaritySearch:
    """
    Sistema de búsqueda de similitud para pinturas de arte.
    Usa CLIP para extraer embeddings y FAISS para búsqueda rápida.
    """
    
    def __init__(self, model_name: str = "openai/clip-vit-large-patch14"):
        """
        Inicializa el modelo CLIP y el procesador.
        
        Args:
            model_name: Nombre del modelo CLIP a usar (default: ViT-L/14)
        """
        print(f"🎨 Cargando modelo CLIP: {model_name}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Usando dispositivo: {self.device}")
        
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model.eval()  # Modo evaluación
        
        self.index = None
        self.image_paths = []
        self.embeddings = None
        
    def extract_embedding(self, image_path: str) -> np.ndarray:
        """
        Extrae el embedding de una imagen usando CLIP.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            Vector embedding normalizado
        """
        try:
            image = Image.open(image_path).convert("RGB")
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
            
            # Normalizar para similitud del coseno
            embedding = image_features.cpu().numpy()
            embedding = embedding / np.linalg.norm(embedding)
            
            return embedding.flatten()
        
        except Exception as e:
            print(f"⚠️  Error procesando {image_path}: {e}")
            return None
    
    def build_index(self, images_dir: str, save_path: str = None):
        """
        Construye el índice FAISS a partir de un directorio de imágenes.
        
        Args:
            images_dir: Directorio con las imágenes del dataset
            save_path: Ruta para guardar el índice (opcional)
        """
        print(f"\n📂 Escaneando directorio: {images_dir}")
        
        # Obtener todas las imágenes
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        image_files = []
        
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                if Path(file).suffix.lower() in image_extensions:
                    image_files.append(os.path.join(root, file))
        
        print(f"   Encontradas {len(image_files)} imágenes")
        
        if len(image_files) == 0:
            raise ValueError("No se encontraron imágenes en el directorio especificado")
        
        # Extraer embeddings
        print(f"\n🔍 Extrayendo embeddings con CLIP...")
        embeddings_list = []
        valid_paths = []
        
        for img_path in tqdm(image_files, desc="Procesando imágenes"):
            embedding = self.extract_embedding(img_path)
            if embedding is not None:
                embeddings_list.append(embedding)
                valid_paths.append(img_path)
        
        if len(embeddings_list) == 0:
            raise ValueError("No se pudieron extraer embeddings de ninguna imagen")
        
        self.embeddings = np.array(embeddings_list).astype('float32')
        self.image_paths = valid_paths
        
        print(f"   Embeddings extraídos: {self.embeddings.shape}")
        
        # Crear índice FAISS con IVF (Inverted File Index)
        print(f"\n⚡ Construyendo índice FAISS...")
        dimension = self.embeddings.shape[1]
        
        # Para dataset de ~60k imágenes, usar IVF con ~sqrt(n) clusters
        n_images = len(self.embeddings)
        nlist = min(int(np.sqrt(n_images)), 100)  # Número de clusters
        
        # Cuantizador: IndexFlatIP para Inner Product (equivalente a coseno con vectores normalizados)
        quantizer = faiss.IndexFlatIP(dimension)
        
        # Índice IVF con similitud del coseno (Inner Product con vectores normalizados)
        self.index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_INNER_PRODUCT)
        
        # Entrenar el índice
        print(f"   Entrenando índice con {nlist} clusters...")
        self.index.train(self.embeddings)
        
        # Agregar vectores al índice
        print(f"   Agregando {n_images} vectores al índice...")
        self.index.add(self.embeddings)
        
        print(f"   ✅ Índice construido exitosamente")
        
        # Guardar índice si se especifica ruta
        if save_path:
            self.save_index(save_path)
    
    def save_index(self, save_path: str):
        """
        Guarda el índice FAISS y los metadatos.
        
        Args:
            save_path: Directorio donde guardar los archivos
        """
        os.makedirs(save_path, exist_ok=True)
        
        # Guardar índice FAISS
        index_file = os.path.join(save_path, "faiss_index.bin")
        faiss.write_index(self.index, index_file)
        
        # Guardar metadatos
        metadata = {
            'image_paths': self.image_paths,
            'embeddings': self.embeddings
        }
        metadata_file = os.path.join(save_path, "metadata.pkl")
        with open(metadata_file, 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"\n💾 Índice guardado en: {save_path}")
    
    def load_index(self, load_path: str):
        """
        Carga un índice FAISS previamente guardado.
        
        Args:
            load_path: Directorio con los archivos del índice
        """
        print(f"\n📥 Cargando índice desde: {load_path}")
        
        # Cargar índice FAISS
        index_file = os.path.join(load_path, "faiss_index.bin")
        self.index = faiss.read_index(index_file)
        
        # Cargar metadatos
        metadata_file = os.path.join(load_path, "metadata.pkl")
        with open(metadata_file, 'rb') as f:
            metadata = pickle.load(f)
        
        self.image_paths = metadata['image_paths']
        self.embeddings = metadata['embeddings']
        
        print(f"   ✅ Índice cargado: {len(self.image_paths)} imágenes")
    
    def search(self, query_image_path: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Busca las k imágenes más similares a la imagen de consulta.
        
        Args:
            query_image_path: Ruta de la imagen de consulta
            top_k: Número de resultados a devolver (default: 3)
            
        Returns:
            Lista de tuplas (ruta_imagen, similitud)
        """
        if self.index is None:
            raise ValueError("Primero debe construir o cargar un índice")
        
        print(f"\n🔎 Buscando imágenes similares a: {query_image_path}")
        
        # Extraer embedding de la consulta
        query_embedding = self.extract_embedding(query_image_path)
        if query_embedding is None:
            raise ValueError("No se pudo procesar la imagen de consulta")
        
        query_vector = query_embedding.reshape(1, -1).astype('float32')
        
        # Búsqueda en FAISS (nprobe controla cuántos clusters explorar)
        self.index.nprobe = min(10, self.index.nlist)  # Buscar en 10 clusters
        distances, indices = self.index.search(query_vector, top_k)
        
        # Preparar resultados
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx != -1:  # FAISS retorna -1 si no encuentra suficientes vecinos
                results.append((self.image_paths[idx], float(dist)))
        
        return results
    
    def display_results(self, query_image_path: str, results: List[Tuple[str, float]]):
        """
        Muestra los resultados de búsqueda.
        
        Args:
            query_image_path: Ruta de la imagen de consulta
            results: Lista de resultados de la búsqueda
        """
        print(f"\n{'='*80}")
        print(f"🎨 RESULTADOS DE BÚSQUEDA")
        print(f"{'='*80}")
        print(f"\n📷 Imagen de consulta: {query_image_path}")
        print(f"\n🏆 Top {len(results)} imágenes más similares:\n")
        
        for i, (path, similarity) in enumerate(results, 1):
            # Convertir Inner Product a porcentaje de similitud
            similarity_percent = (similarity + 1) / 2 * 100  # Normalizar de [-1,1] a [0,100]
            print(f"   {i}. Similitud: {similarity_percent:.2f}%")
            print(f"      Ruta: {path}")
            print()


def main():
    """
    Ejemplo de uso del sistema de búsqueda de similitud.
    """
    # Configuración
    IMAGES_DIR = "/home/guille/workspace/dataset"  # ← CAMBIAR AQUÍ
    QUERY_IMAGE = "./query_image/alfred-sisley_flooding-at-moret-1889.jpg"  # ← CAMBIAR AQUÍ
    INDEX_SAVE_PATH = "./faiss_index"  # Donde guardar/cargar el índice
    TOP_K = 3  # Número de imágenes similares a buscar
    
    # Inicializar sistema
    search_system = ArtSimilaritySearch(model_name="openai/clip-vit-large-patch14")
    
    # Opción 1: Construir nuevo índice (primera vez o actualización)
    if not os.path.exists(INDEX_SAVE_PATH):
        search_system.build_index(IMAGES_DIR, save_path=INDEX_SAVE_PATH)
    else:
        # Opción 2: Cargar índice existente (mucho más rápido)
        search_system.load_index(INDEX_SAVE_PATH)
    
    # Realizar búsqueda
    results = search_system.search(QUERY_IMAGE, top_k=TOP_K)
    
    # Mostrar resultados
    search_system.display_results(QUERY_IMAGE, results)


if __name__ == "__main__":
    main()