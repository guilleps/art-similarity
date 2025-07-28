### ✅ **Resumen de Resultados por Fase**

#### 📌 **Fase 1 (Feature Extraction)**

* Buen comienzo: la red logra entrenar con pesos congelados y obtiene una **accuracy de validación de \~66.5%** en la mejor época.
* El modelo guardado (`efficientnet_phase1.keras`) se hace correctamente.

#### 📌 **Fase 2 (Fine-Tuning parcial desde capa 50)**

* **Decay de accuracy**: la validación baja progresivamente de \~62% a 59%, lo cual sugiere que al descongelar 50 capas sin una tasa de aprendizaje suficientemente baja, el modelo sobreajustó o destruyó parte del conocimiento previo.
* El LR scheduler fue aplicado, pero iniciar con `1e-4` puede haber sido demasiado alto para tantas capas.

#### 📌 **Fase 3 (Fine-Tuning total)**

* Aquí sí se usó una LR más conservadora `1e-5`, lo cual ayudó a estabilizar, pero:

  * La accuracy no mejora más allá de \~59%.
  * Indica que el modelo ya no está aprendiendo cosas nuevas, o que las capas iniciales no estaban suficientemente útiles para las nuevas clases.

#### 📌 **Evaluación Embeddings**

* Se logró calcular el **Silhouette Score** y el **Precision\@5**:

  ```
  Silhouette=0.1090, P@5=0.5162
  ```

  * El `P@5=51.6%` está bastante bien considerando que hay 10 clases.
  * Pero el `Silhouette Score=0.1090` es bajo → indica que las clases están poco separadas en el espacio de embeddings.

---

### 📉 Posibles Problemas Detectados

1. **Resolución de imagen (260x260)**:

   * No es problema que tus imágenes reales sean de 256x256 y luego se reescalen a 260x260.
   * Sin embargo, estás interpolando cada imagen, lo que podría estar suavizando detalles importantes de estilo (clave si estás analizando imágenes artísticas).
   * **👉 Recomendación**: prueba con imágenes en su tamaño original (256x256) usando `EfficientNetB0` o recorta inteligentemente las imágenes a 260x260 en lugar de escalarlas.

2. **Pocas épocas**:

   * 3 épocas por fase es muy poco para una tarea de fine-tuning.
   * En Fase 1, se nota que el modelo seguía mejorando.
   * **👉 Recomendación**: al menos 5-10 épocas por fase para capturar patrones, especialmente si usas EarlyStopping.

3. **Cantidad de capas descongeladas (50)**:

   * Es una cantidad significativa (más del 60% del modelo), lo cual exige una tasa de aprendizaje muy pequeña y un entrenamiento más largo.
   * **👉 Recomendación**: intenta descongelar primero desde block7 únicamente (las últimas 20-30 capas) y monitorea el cambio.

4. **Embeddings poco separables**:

   * El bajo Silhouette indica que no se están aprendiendo representaciones suficientemente discriminativas.
   * Puede deberse a:

     * Dataset pequeño o muy homogéneo.
     * Arquitectura no suficientemente profunda para capturar diferencias compositivas.
     * Embedding layer demasiado pequeño (`128`).
   * **👉 Recomendación**:

     * Probar `EMBEDDING_DIM=256` o `512`.
     * Añadir `BatchNormalization` justo después del `GlobalAveragePooling2D` o antes del embedding.

5. **Dataset**:

   * Mencionas que usas 5000 imágenes en train y `test/` (sin indicar cuántas).
   * **👉 Recomendación**: asegurarte de que el test dataset tenga al menos 100-200 imágenes por clase.

---

### ✅ Siguientes pasos recomendados

1. **Cambios para el próximo experimento**:

   * `IMG_SIZE = (256, 256)`
   * `EPOCHS_PHASE1 = 5`, `EPOCHS_PHASE2 = 5`, `EPOCHS_PHASE3 = 5`
   * Reducir capas descongeladas en Fase 2: `trainable_layers=20`
   * `EMBEDDING_DIM = 256`
   * Añadir `BatchNormalization()` después del pooling y antes del `Dense(embedding)`
   * Usar `CosineDecay` o `Warmup` como scheduler opcional

2. **Para evaluar resultados de forma más visual**:

   * Haz un `TSNE` o `PCA` de los embeddings para visualizar si las clases se agrupan.
   * Muestra ejemplos de errores en `Precision@5` para ver si son visualmente similares.