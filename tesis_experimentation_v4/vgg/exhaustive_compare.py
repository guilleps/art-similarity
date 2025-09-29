import numpy as np
import argparse
import sys
import os
from vgg19_extractor import VGG19EmbeddingExtractor
from sklearn.metrics.pairwise import cosine_similarity
import time


class ExhaustiveImageComparator:
    """
    Comparador que prueba TODAS las combinaciones método-capa posibles
    """

    def __init__(self, verbose=False):
        self.extractor = VGG19EmbeddingExtractor()
        self.verbose = verbose

        # Todas las capas disponibles en VGG-19
        self.all_layers = {
            "conv": [
                "conv1_1",
                "conv1_2",
                "conv2_1",
                "conv2_2",
                "conv3_1",
                "conv3_2",
                "conv3_3",
                "conv3_4",
                "conv4_1",
                "conv4_2",
                "conv4_3",
                "conv4_4",
                "conv5_1",
                "conv5_2",
                "conv5_3",
                "conv5_4",
            ],
            "gram": [
                "conv1_1",
                "conv1_2",
                "conv2_1",
                "conv2_2",
                "conv3_1",
                "conv3_2",
                "conv3_3",
                "conv3_4",
                "conv4_1",
                "conv4_2",
                "conv4_3",
                "conv4_4",
                "conv5_1",
                "conv5_2",
                "conv5_3",
                "conv5_4",
            ],
            "fc": ["fc1", "fc2", "fc3"],  # Capas fully connected
        }

        # Métodos a probar
        self.methods = ["gram", "conv", "fc"]

    def compute_cosine_similarity(self, embedding1, embedding2):
        """Calcula similitud coseno entre dos embeddings"""
        similarity_matrix = cosine_similarity([embedding1], [embedding2])
        return similarity_matrix[0][0]

    def normalize_embedding(self, embedding):
        """Normaliza un embedding (L2 normalization)"""
        norm = np.linalg.norm(embedding)
        if norm == 0:
            return embedding
        return embedding / norm

    def compare_single_config(self, image_path1, image_path2, method, layer):
        """
        Compara dos imágenes con una configuración específica

        Returns:
            float: Similitud coseno o None si hay error
        """
        try:
            # Crear nuevo extractor para evitar caché
            extractor = VGG19EmbeddingExtractor()

            # Extraer embeddings
            embedding1 = extractor.extract_embedding(
                image_path1, method=method, layer=layer
            )
            embedding2 = extractor.extract_embedding(
                image_path2, method=method, layer=layer
            )

            # Normalizar
            embedding1 = self.normalize_embedding(embedding1)
            embedding2 = self.normalize_embedding(embedding2)

            # Calcular similitud
            similarity = self.compute_cosine_similarity(embedding1, embedding2)

            return similarity

        except Exception as e:
            if self.verbose:
                print(f"    ❌ Error en {method}-{layer}: {e}")
            return None

    def compare_all_combinations(self, image_path1, image_path2):
        """
        Compara dos imágenes usando TODAS las combinaciones posibles

        Returns:
            dict: Resultados organizados por método y capa
        """
        # Verificar que las imágenes existen
        if not os.path.exists(image_path1):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path1}")
        if not os.path.exists(image_path2):
            raise FileNotFoundError(f"No se encontró la imagen: {image_path2}")

        results = {}
        total_combinations = sum(len(layers) for layers in self.all_layers.values())
        current = 0

        print(
            f"\n🔍 Comparando: {os.path.basename(image_path1)} vs {os.path.basename(image_path2)}"
        )
        print(f"📊 Probando {total_combinations} combinaciones método-capa...")
        print("=" * 80)

        # Iterar por cada método
        for method in self.methods:
            method_results = {}
            method_start_time = time.time()

            print(f"\n🧠 MÉTODO: {method.upper()}")
            print("-" * 50)

            # Iterar por cada capa del método actual
            for layer in self.all_layers[method]:
                current += 1

                if self.verbose:
                    print(
                        f"  [{current:2d}/{total_combinations}] Probando {method}-{layer}...",
                        end=" ",
                    )

                # Calcular similitud
                similarity = self.compare_single_config(
                    image_path1, image_path2, method, layer
                )

                if similarity is not None:
                    method_results[layer] = similarity
                    if self.verbose:
                        print(f"✓ {similarity:.6f}")
                    else:
                        print(f"  {layer:8s}: {similarity:.6f}")
                else:
                    method_results[layer] = None
                    if self.verbose:
                        print("✗ Error")

            # Estadísticas del método
            method_time = time.time() - method_start_time
            valid_results = [v for v in method_results.values() if v is not None]

            if valid_results:
                avg_sim = np.mean(valid_results)
                min_sim = np.min(valid_results)
                max_sim = np.max(valid_results)

                print(
                    f"  📈 Promedio: {avg_sim:.6f} | Rango: {min_sim:.6f} - {max_sim:.6f}"
                )
                print(f"  ⏱️  Tiempo: {method_time:.1f}s")

            results[method] = method_results

        return results

    def format_results_table(self, results):
        """
        Formatea los resultados en tabla para fácil visualización
        """
        print(f"\n{'='*80}")
        print("📋 TABLA COMPLETA DE RESULTADOS")
        print(f"{'='*80}")

        # Encabezado
        print(f"{'MÉTODO':<8} {'CAPA':<12} {'SIMILITUD':<12} {'INTERPRETACIÓN'}")
        print("-" * 80)

        # Función para interpretar similitud
        def interpret_similarity(similarity):
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

        # Mostrar resultados
        for method, method_results in results.items():
            for layer, similarity in method_results.items():
                if similarity is not None:
                    interpretation = interpret_similarity(similarity)
                    print(
                        f"{method:<8} {layer:<12} {similarity:<12.6f} {interpretation}"
                    )
                else:
                    print(f"{method:<8} {layer:<12} {'ERROR':<12} {'No disponible'}")

    def export_results_csv(self, results, image1_name, image2_name, output_file=None):
        """
        Exporta los resultados a CSV para análisis posterior
        """
        if output_file is None:
            output_file = f"similarity_results_{image1_name}_{image2_name}.csv"

        with open(output_file, "w") as f:
            # Encabezado
            f.write("Image1,Image2,Method,Layer,Similarity\n")

            # Datos
            for method, method_results in results.items():
                for layer, similarity in method_results.items():
                    if similarity is not None:
                        f.write(
                            f"{image1_name},{image2_name},{method},{layer},{similarity:.6f}\n"
                        )

        print(f"\n💾 Resultados exportados a: {output_file}")

    def find_best_configurations(self, results, top_n=5):
        """
        Encuentra las mejores configuraciones método-capa
        """
        all_results = []

        for method, method_results in results.items():
            for layer, similarity in method_results.items():
                if similarity is not None:
                    all_results.append(
                        {
                            "method": method,
                            "layer": layer,
                            "similarity": similarity,
                            "config": f"{method}-{layer}",
                        }
                    )

        # Ordenar por similitud descendente
        all_results.sort(key=lambda x: x["similarity"], reverse=True)

        print(f"\n🏆 TOP {top_n} CONFIGURACIONES:")
        print("-" * 50)
        for i, result in enumerate(all_results[:top_n], 1):
            print(
                f"  {i}. {result['config']:12s} → {result['similarity']:.6f} ({result['similarity']*100:.2f}%)"
            )

        print(f"\n🔻 BOTTOM {top_n} CONFIGURACIONES:")
        print("-" * 50)
        for i, result in enumerate(all_results[-top_n:], 1):
            print(
                f"  {i}. {result['config']:12s} → {result['similarity']:.6f} ({result['similarity']*100:.2f}%)"
            )

        return all_results


def main():
    """
    Función principal con interfaz de línea de comandos
    """
    parser = argparse.ArgumentParser(
        description="Comparación exhaustiva entre dos imágenes usando TODAS las combinaciones VGG-19",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python exhaustive_compare.py imagen1.jpg imagen2.jpg
  python exhaustive_compare.py imagen1.jpg imagen2.jpg --verbose
  python exhaustive_compare.py imagen1.jpg imagen2.jpg --export results.csv
  python exhaustive_compare.py imagen1.jpg imagen2.jpg --top 10
        """,
    )

    parser.add_argument("image1", help="Ruta a la primera imagen")
    parser.add_argument("image2", help="Ruta a la segunda imagen")

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Mostrar progreso detallado durante el procesamiento",
    )

    parser.add_argument(
        "--export",
        help="Exportar resultados a archivo CSV (especifica nombre o usa auto)",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Número de mejores/peores configuraciones a mostrar (default: 5)",
    )

    parser.add_argument(
        "--no-table",
        action="store_true",
        help="No mostrar tabla completa de resultados",
    )

    args = parser.parse_args()

    # Crear comparador
    comparator = ExhaustiveImageComparator(verbose=args.verbose)

    try:
        start_time = time.time()

        # Realizar comparación exhaustiva
        results = comparator.compare_all_combinations(args.image1, args.image2)

        total_time = time.time() - start_time

        # Mostrar tabla completa (si no se desactivó)
        if not args.no_table:
            comparator.format_results_table(results)

        # Encontrar mejores configuraciones
        comparator.find_best_configurations(results, top_n=args.top)

        # Exportar a CSV si se solicita
        if args.export:
            img1_name = os.path.splitext(os.path.basename(args.image1))[0]
            img2_name = os.path.splitext(os.path.basename(args.image2))[0]

            csv_file = args.export if args.export != "auto" else None
            comparator.export_results_csv(results, img1_name, img2_name, csv_file)

        # Resumen final
        total_configs = sum(len(method_results) for method_results in results.values())
        successful_configs = sum(
            len([v for v in method_results.values() if v is not None])
            for method_results in results.values()
        )

        print(f"\n{'='*80}")
        print(f"✅ COMPARACIÓN COMPLETADA")
        print(f"{'='*80}")
        print(f"  Configuraciones probadas: {successful_configs}/{total_configs}")
        print(f"  Tiempo total: {total_time:.1f} segundos")
        print(f"  Tiempo promedio por config: {total_time/successful_configs:.2f}s")
        print(f"{'='*80}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
