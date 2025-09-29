import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
import argparse
import sys
import os
from vgg19_extractor import VGG19EmbeddingExtractor


class ImageSimilarityComparator:

    def __init__(self, method="gram", layer="conv4_2", verbose=True):
        """
        Args:
            method: Método de extracción ('gram', 'conv', 'fc')
            layer: Capa de la que extraer features
            verbose: Si mostrar información detallada
        """
        self.extractor = VGG19EmbeddingExtractor()
        self.method = method
        self.layer = layer
        self.verbose = verbose

        if verbose:
            print(f"Comparador inicializado:")
            print(f"  - Método: {method}")
            print(f"  - Capa: {layer}")
            print(f"  - Device: {self.extractor.device}")
            print("-" * 50)

    def compute_cosine_similarity(self, embedding1, embedding2):
        """
        Calcula la similitud coseno entre dos embeddings.

        Args:
            embedding1: Primer embedding (numpy array)
            embedding2: Segundo embedding (numpy array)

        Returns:
            float: Similitud coseno entre -1 y 1
                   1 = idénticos
                   0 = ortogonales (sin relación)
                   -1 = opuestos
        """
        # Método 1: Usando scipy (devuelve distancia, no similitud)
        # cosine_distance = cosine(embedding1, embedding2)
        # similarity = 1 - cosine_distance

        # Método 2 alternativo: Usando sklearn (más directo)
        similarity_matrix = cosine_similarity([embedding1], [embedding2])
        similarity = similarity_matrix[0][0]

        return similarity

    def normalize_embedding(self, embedding):
        """
        Normaliza un embedding (L2 normalization).
        Útil para hacer las comparaciones más estables.

        Args:
            embedding: Embedding a normalizar

        Returns:
            Embedding normalizado
        """
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        return embedding / norm

    def compare_images(self, image_path1, image_path2, normalize=True):
        """
        Compara dos imágenes y devuelve su similitud.

        Args:
            image_path1: Ruta a la primera imagen
            image_path2: Ruta a la segunda imagen
            normalize: Si normalizar los embeddings antes de comparar

        Returns:
            dict: Diccionario con resultados de similitud
        """
        # Verificar que las imágenes existen
        if not os.path.exists(image_path1):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path1}")
        if not os.path.exists(image_path2):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path2}")

        if self.verbose:
            print(f"Procesando imagen 1: {os.path.basename(image_path1)}")

        # Extraer embedding de la primera imagen
        embedding1 = self.extractor.extract_embedding(
            image_path1, method=self.method, layer=self.layer
        )

        if self.verbose:
            print(f"  ✓ Embedding 1 extraído: shape={embedding1.shape}")
            print(f"\nProcesando imagen 2: {os.path.basename(image_path2)}")

        # Extraer embedding de la segunda imagen
        embedding2 = self.extractor.extract_embedding(
            image_path2, method=self.method, layer=self.layer
        )

        if self.verbose:
            print(f"  ✓ Embedding 2 extraído: shape={embedding2.shape}")

        # Normalizar si se requiere
        if normalize:
            embedding1 = self.normalize_embedding(embedding1)
            embedding2 = self.normalize_embedding(embedding2)
            if self.verbose:
                print(f"  ✓ Embeddings normalizados")

        # Calcular similitud coseno
        similarity = self.compute_cosine_similarity(embedding1, embedding2)

        # Crear resultado
        results = {
            "similarity": similarity,
            "similarity_percentage": similarity * 100,
            "embedding1_shape": embedding1.shape,
            "embedding2_shape": embedding2.shape,
            "method": self.method,
            "layer": self.layer,
            "normalized": normalize,
        }

        return results

    def interpret_similarity(self, similarity):
        if similarity >= 0.95:
            return "Prácticamente idénticas"
        elif similarity >= 0.85:
            return "Muy similares"
        elif similarity >= 0.70:
            return "Similares"
        elif similarity >= 0.50:
            return "Moderadamente similares"
        elif similarity >= 0.30:
            return "Poco similares"
        elif similarity >= 0.10:
            return "Muy poco similares"
        else:
            return "Diferentes"

    def compare_multiple_methods(self, image_path1, image_path2):
        """
        Compara dos imágenes usando múltiples métodos/capas.

        Args:
            image_path1: Ruta a la primera imagen
            image_path2: Ruta a la segunda imagen

        Returns:
            dict: Resultados para cada método
        """
        comparisons = {}

        # Diferentes configuraciones a probar
        configs = [
            ("gram", "conv3_3", "Texturas finas"),
            ("gram", "conv4_2", "Patrones medios"),
            ("gram", "conv5_3", "Características abstractas"),
            ("conv", "conv4_2", "Features espaciales"),
            ("fc", "fc2", "Representación semántica"),
        ]

        print("\n" + "=" * 60)
        print("COMPARACIÓN MULTI-MÉTODO")
        print("=" * 60)

        for method, layer, description in configs:
            self.method = method
            self.layer = layer

            print(f"\n{description} ({method} - {layer}):")
            print("-" * 40)

            try:
                results = self.compare_images(image_path1, image_path2, normalize=True)

                similarity = results["similarity"]
                interpretation = self.interpret_similarity(similarity)

                print(f"  Similitud: {similarity:.4f} ({similarity*100:.2f}%)")
                print(f"  Interpretación: {interpretation}")

                comparisons[f"{method}_{layer}"] = {
                    "similarity": similarity,
                    "description": description,
                    "interpretation": interpretation,
                }

            except Exception as e:
                print(f"  Error: {e}")
                comparisons[f"{method}_{layer}"] = None

        # Calcular promedio
        valid_similarities = [v["similarity"] for v in comparisons.values() if v]
        if valid_similarities:
            avg_similarity = np.mean(valid_similarities)
            print(f"\n{'='*60}")
            print(
                f"SIMILITUD PROMEDIO: {avg_similarity:.4f} ({avg_similarity*100:.2f}%)"
            )
            print(
                f"Interpretación general: {self.interpret_similarity(avg_similarity)}"
            )
            print(f"{'='*60}")

        return comparisons


def main():
    """
    Función principal con interfaz de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Compara la similitud entre dos imágenes usando VGG-19",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python compare_images.py imagen1.jpg imagen2.jpg
  python compare_images.py imagen1.jpg imagen2.jpg --method gram --layer conv4_2
  python compare_images.py imagen1.jpg imagen2.jpg --all-methods
  python compare_images.py imagen1.jpg imagen2.jpg --quiet
        """,
    )

    parser.add_argument("image1", help="Ruta a la primera imagen")
    parser.add_argument("image2", help="Ruta a la segunda imagen")

    parser.add_argument(
        "--method",
        choices=["gram", "conv", "fc"],
        default="gram",
        help="Método de extracción de embeddings (default: gram)",
    )

    parser.add_argument(
        "--layer",
        default="conv4_2",
        help="Capa de la que extraer features (default: conv4_2)",
    )

    parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="No normalizar los embeddings antes de comparar",
    )

    parser.add_argument(
        "--all-methods",
        action="store_true",
        help="Comparar usando todos los métodos disponibles",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Modo silencioso, solo mostrar resultado final",
    )

    args = parser.parse_args()

    # Crear comparador
    comparator = ImageSimilarityComparator(
        method=args.method, layer=args.layer, verbose=not args.quiet
    )

    try:
        if args.all_methods:
            # Comparar con múltiples métodos
            results = comparator.compare_multiple_methods(args.image1, args.image2)
        else:
            # Comparación simple
            if not args.quiet:
                print("\n" + "=" * 60)
                print("COMPARACIÓN DE SIMILITUD ENTRE IMÁGENES")
                print("=" * 60)
                print(f"Imagen 1: {args.image1}")
                print(f"Imagen 2: {args.image2}")
                print("-" * 60)

            results = comparator.compare_images(
                args.image1, args.image2, normalize=not args.no_normalize
            )

            similarity = results["similarity"]
            interpretation = comparator.interpret_similarity(similarity)

            # Mostrar resultados
            if args.quiet:
                # Modo silencioso: solo el número
                print(f"{similarity:.6f}")
            else:
                print("\n" + "=" * 60)
                print("RESULTADOS")
                print("=" * 60)
                print(f"📊 Similitud Coseno: {similarity:.6f} | 📈 Porcentaje: {results['similarity_percentage']:.2f}%")
                print(f"💡 Interpretación: {interpretation}")
                print("-" * 60)
                print(f"ℹ️  Método: {results['method']}")
                print(f"ℹ️  Capa: {results['layer']}")
                print(f"ℹ️  Normalizado: {'Sí' if results['normalized'] else 'No'}")
                print(f"ℹ️  Dimensiones embedding: {results['embedding1_shape'][0]}")
                print("=" * 60)

                # Escala visual
                print("\nESCALA DE SIMILITUD:")
                print("  0% ────────────────────────────────── 100%")
                print(
                    "  |"
                    + " " * int(similarity * 36)
                    + "▓"
                    + " " * (36 - int(similarity * 36))
                    + "|"
                )
                print(f"  └─> {similarity*100:.1f}% similar")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


# Función de conveniencia para uso directo en Python
def compare_images_simple(image1_path, image2_path, method="gram", layer="conv4_2"):
    """
    Función simple para comparar dos imágenes.

    Args:
        image1_path: Ruta a la primera imagen
        image2_path: Ruta a la segunda imagen
        method: Método de extracción ('gram', 'conv', 'fc')
        layer: Capa a usar

    Returns:
        float: Similitud coseno (0 a 1)

    Ejemplo:
        >>> similarity = compare_images_simple('foto1.jpg', 'foto2.jpg')
        >>> print(f"Las imágenes son {similarity*100:.1f}% similares")
    """
    comparator = ImageSimilarityComparator(method=method, layer=layer, verbose=False)
    results = comparator.compare_images(image1_path, image2_path)
    return results["similarity"]


if __name__ == "__main__":
    main()
