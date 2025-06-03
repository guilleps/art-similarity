![Arquitectura Interna del Modelo](resources/img/cnn_bp.png)

### Proceso de Fine-Tuning de EfficientNetB0

La imagen anterior muestra la arquitectura interna utilizada para el proceso de **fine-tuning** de **EfficientNetB0** con el dataset **Art Bench 10**. Este procedimiento permite ajustar los pesos preentrenados de EfficientNetB0, un modelo eficiente y ampliamente utilizado para la clasificación de imágenes, adaptándolo a las características específicas de este conjunto de datos.

#### Descripción del Procedimiento

1. **Congelación de Capas Iniciales**:  
    Las capas iniciales del modelo, que contienen características generales aprendidas de un dataset más grande, se congelan para preservar este conocimiento previo.

2. **Entrenamiento de Capas Superiores**:  
    Las capas superiores del modelo se entrenan utilizando el dataset **Art Bench 10**, permitiendo que el modelo se especialice en clasificar las categorías específicas de este nuevo conjunto de datos.
