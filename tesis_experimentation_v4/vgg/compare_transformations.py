import numpy as np
import os
import csv
from pathlib import Path
from tqdm import tqdm
from vgg19_extractor import VGG19EmbeddingExtractor
from sklearn.metrics.pairwise import cosine_similarity


class TransformationComparator:
    """
    Compara transformaciones de imágenes usando VGG-19 FC2 embeddings
    """

    def __init__(self, method="fc", layer="fc2"):
        self.extractor = VGG19EmbeddingExtractor()
        self.method = method
        self.layer = layer

        # Transformaciones a comparar (sin _original)
        self.transformations = [
            "heatmap",
            "hsv_hue",
            "hsv_saturation",
            "hsv_value",
            "contrast",
            "texture",
        ]

    def normalize_embedding(self, embedding):
        """Normaliza un embedding (L2 normalization)"""
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        return embedding / norm

    def compute_cosine_similarity(self, embedding1, embedding2):
        """Calcula similitud coseno entre dos embeddings"""
        similarity_matrix = cosine_similarity([embedding1], [embedding2])
        return similarity_matrix[0][0]

    def extract_embedding(self, image_path):
        """Extrae embedding de una imagen"""
        try:
            embedding = self.extractor.extract_embedding(
                image_path, method=self.method, layer=self.layer
            )
            return self.normalize_embedding(embedding)
        except Exception as e:
            print(f"    ⚠️  Error extrayendo embedding de {image_path}: {e}")
            return None

    def find_image_pairs(self, folder_path):
        """
        Encuentra los pares de imágenes en una carpeta
        Asume que hay 2 imágenes base (ej: imagen1, imagen2)

        Returns:
            tuple: (base_name1, base_name2) o None si no hay exactamente 2
        """
        # Buscar imágenes originales
        original_images = [
            f
            for f in os.listdir(folder_path)
            if f.endswith("_original.jpg") or f.endswith("_original.png")
        ]

        if len(original_images) != 2:
            print(
                f"    ⚠️  Se esperaban 2 imágenes originales, se encontraron {len(original_images)}"
            )
            return None

        # Extraer nombres base (sin _original.jpg)
        base_names = []
        for img in original_images:
            base_name = img.replace("_original.jpg", "").replace("_original.png", "")
            base_names.append(base_name)

        return tuple(sorted(base_names))

    def compare_folder(self, folder_path):
        """
        Compara todas las transformaciones de un par de imágenes en una carpeta

        Returns:
            dict: {transformation: similarity_score}
        """
        # Encontrar pares de imágenes
        image_pair = self.find_image_pairs(folder_path)
        if image_pair is None:
            return None

        base_name1, base_name2 = image_pair
        results = {}

        # Comparar cada transformación
        for transformation in self.transformations:
            # Construir rutas de las imágenes transformadas
            img1_path = os.path.join(folder_path, f"{base_name1}_{transformation}.jpg")
            img2_path = os.path.join(folder_path, f"{base_name2}_{transformation}.jpg")

            # Verificar que ambas imágenes existen
            if not os.path.exists(img1_path):
                print(f"    ⚠️  No existe: {img1_path}")
                results[transformation] = None
                continue

            if not os.path.exists(img2_path):
                print(f"    ⚠️  No existe: {img2_path}")
                results[transformation] = None
                continue

            # Extraer embeddings
            embedding1 = self.extract_embedding(img1_path)
            embedding2 = self.extract_embedding(img2_path)

            if embedding1 is None or embedding2 is None:
                results[transformation] = None
                continue

            # Calcular similitud
            similarity = self.compute_cosine_similarity(embedding1, embedding2)
            results[transformation] = similarity

        return results

    def process_all_folders(self, base_dir):
        """
        Procesa todas las carpetas numeradas en el directorio base

        Returns:
            dict: {folder_number: {transformation: similarity}}
        """
        base_path = Path(base_dir)

        if not base_path.exists():
            raise FileNotFoundError(f"El directorio {base_dir} no existe")

        # Obtener carpetas numeradas
        numbered_folders = []
        for folder in base_path.iterdir():
            if folder.is_dir() and folder.name.isdigit():
                folder_num = int(folder.name)
                numbered_folders.append((folder_num, folder))

        # Ordenar por número
        numbered_folders.sort(key=lambda x: x[0])

        print(f"\n🔍 Encontradas {len(numbered_folders)} carpetas numeradas")
        print(f"📊 Método: {self.method.upper()}, Capa: {self.layer.upper()}")
        print("=" * 80)

        all_results = {}

        # Procesar cada carpeta
        for folder_num, folder_path in tqdm(
            numbered_folders, desc="Procesando carpetas"
        ):
            print(f"\n📁 Carpeta {folder_num}:")

            results = self.compare_folder(str(folder_path))

            if results is not None:
                all_results[folder_num] = results

                # Mostrar resultados de la carpeta
                for transformation, similarity in results.items():
                    if similarity is not None:
                        print(
                            f"  ✓ {transformation:15s}: {similarity:.6f} ({similarity*100:.2f}%)"
                        )
                    else:
                        print(f"  ✗ {transformation:15s}: ERROR")
            else:
                print(f"  ⚠️  No se pudo procesar la carpeta {folder_num}")

        return all_results

    def export_to_csv(self, results, output_file):
        """
        Exporta los resultados a un archivo CSV

        Args:
            results: dict con formato {folder_number: {transformation: similarity}}
            output_file: ruta del archivo CSV de salida
        """
        # Crear encabezado
        header = ["N° PAR"] + [t.upper() for t in self.transformations]

        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Escribir encabezado
            writer.writerow(header)

            # Escribir datos ordenados por número de carpeta
            for folder_num in sorted(results.keys()):
                row = [folder_num]

                for transformation in self.transformations:
                    similarity = results[folder_num].get(transformation)

                    if similarity is not None:
                        row.append(f"{similarity:.6f}")
                    else:
                        row.append("N/A")

                writer.writerow(row)

        print(f"\n💾 Resultados exportados a: {output_file}")

    def generate_statistics(self, results):
        """
        Genera estadísticas generales de todas las comparaciones
        """
        print(f"\n{'='*80}")
        print("📈 ESTADÍSTICAS GENERALES")
        print(f"{'='*80}")

        # Calcular estadísticas por transformación
        for transformation in self.transformations:
            values = []
            for folder_results in results.values():
                sim = folder_results.get(transformation)
                if sim is not None:
                    values.append(sim)

            if values:
                mean_sim = np.mean(values)
                std_sim = np.std(values)
                min_sim = np.min(values)
                max_sim = np.max(values)

                print(f"\n🎨 {transformation.upper()}:")
                print(f"  Media:       {mean_sim:.6f} ({mean_sim*100:.2f}%)")
                print(f"  Desv. Est.:  {std_sim:.6f}")
                print(f"  Rango:       {min_sim:.6f} - {max_sim:.6f}")
                print(f"  N° válidos:  {len(values)}")
            else:
                print(f"\n🎨 {transformation.upper()}: Sin datos válidos")


def main():
    """
    Función principal
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Compara transformaciones de imágenes usando VGG-19",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python compare_transformations.py data_transformations
  python compare_transformations.py data_transformations --output results.csv
  python compare_transformations.py data_transformations --method fc --layer fc2
        """,
    )

    parser.add_argument(
        "--output",
        "-o",
        default="transformation_similarities.csv",
        help="Archivo CSV de salida (default: transformation_similarities.csv)",
    )

    parser.add_argument(
        "--method",
        default="fc",
        choices=["fc", "conv", "gram"],
        help="Método de extracción VGG-19 (default: fc)",
    )

    parser.add_argument(
        "--layer", default="fc2", help="Capa VGG-19 a usar (default: fc2)"
    )

    parser.add_argument(
        "--no-stats",
        action="store_true",
        help="No mostrar estadísticas generales",
    )

    args = parser.parse_args()

    try:
        # Crear comparador
        comparator = TransformationComparator(method=args.method, layer=args.layer)

        # Procesar todas las carpetas
        results = comparator.process_all_folders("/home/guille/workspace/pairs_transformation")

        if not results:
            print("\n⚠️  No se obtuvieron resultados")
            return

        # Exportar a CSV
        comparator.export_to_csv(results, args.output)

        # Mostrar estadísticas
        if not args.no_stats:
            comparator.generate_statistics(results)

        # Resumen final
        print(f"\n{'='*80}")
        print("✅ PROCESO COMPLETADO")
        print(f"{'='*80}")
        print(f"  Carpetas procesadas: {len(results)}")
        print(f"  Archivo CSV: {args.output}")
        print(f"{'='*80}\n")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
