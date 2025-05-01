## Fase 0: **Preparación de datos**

 **Dataset**:
- 60000 imágenes (normalizadas o preprocesadas mínimamente: resize, normalization 0-1 o -1 a 1).

 **Divisiones**:
- *Entrenamiento* (70%) / *Validacion* (15%) / *Pruebas* (15%).

 **Preprocesamiento base**:
- Resize a 224x224 o el tamaño requerido por [EfficientNetB7](https://www.tensorflow.org/api_docs/python/tf/keras/applications/EfficientNetB7) y [ResNet50](https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50).
- Normalización (`imagen = imagen / 255.0` o adaptada al modelo).

---

## Fase 1: **Extracción de Embeddings con Modelos Preentrenados** 

 **Modelos base**:
- `EfficientNetB7` preentrenado en ImageNet.
- `ResNet50` preentrenado en ImageNet.

 **Procedimiento**:
1. **Cargar el modelo sin la capa de clasificación final** (`include_top=False`).
2. **Agregar un GlobalAveragePooling2D** para sacar el embedding final.
3. **Extraer embeddings de todas las imágenes** (guardar en archivos .json).

 **Normalización**:
- Normalizar cada embedding al tener norma 1 (`L2 normalization`).

---

## Fase 2: **Evaluación básica de similitud** 

 **Métricas a evaluar**:
- **Similitud del coseno**.
- **Distancia euclidiana**.

 **Experimento**:
- Para cada imagen:
  - Encontrar sus **5 imágenes más similares** usando **coseno**.
  - Encontrar sus **5 imágenes más similares** usando **euclidiana**.
- Verificar visualmente resultados o calcular métricas (por ejemplo, **precision@5**, si tienes etiquetas).

 **Visualización de espacio de embeddings**:
- Aplicar **PCA** o **t-SNE** para ver si los embeddings están:
  - Compactos.
  - Distribuidos.
  - Aplastados (anisotropía).

---

## Fase 3: **Entrenamiento de Redes con Pérdidas Especializadas** 

 **Funciones de pérdida** a probar:
- **Triplet Loss** (con márgenes adecuados).
- **Contrastive Loss**.
- **ArcFace Loss**.

 **Procedimiento**:
1. **Tomar EfficientNetB7 y ResNet50 como base** (cargar solo pesos de convolución, no clasificación).
2. **Agregar nuevas capas de embeddings** (por ejemplo, Dense(512), BatchNormalization, L2Norm).
3. **Entrenar desde el embedding** con las nuevas pérdidas sobre tu dataset.

 **Técnica importante**:
- Crear pares o tríadas de imágenes (positiva-negativa) si tu dataset no tiene "parejas" naturales.

 **Normalizar embeddings** al final del modelo (muy importante para ArcFace o Triplet Loss).

---

## Fase 4: **Nueva Evaluación Post-Entrenamiento** 

 **Extraer nuevamente embeddings** de modelos entrenados con las pérdidas especializadas.

 **Repetir evaluación de similitud**:
- Similaridad del coseno.
- Distancia euclidiana.
- Comparar con los resultados de Fase 2.

 **Métricas adicionales**:
- **Mean Average Precision (mAP)**.
- **Precision@k**.
- **Recall@k**.

 **Visualización de Embeddings mejorados**:
- t-SNE o UMAP para ver si ahora los grupos son más compactos y separados.

---

## Fase 5: **Comparación y Análisis Final** 

 **Comparar**:
- ¿Qué arquitectura base funciona mejor? (EfficientNetB7 vs ResNet50).
- ¿Qué función de pérdida generó embeddings más "discriminativos"?
- ¿La métrica coseno o euclidiana funciona mejor ahora?

 **Observaciones**:
- ¿Se redujo la anisotropía?
- ¿Embeddings ahora reflejan mejor la similitud semántica?