# Vizel Art Similarity

## Resumen
Este proyecto esta diseñando para el análisis y comparación de obras de arte impresionistas bajo las caracteristicas de bajo nivel que posee la obra. Este experimento hace de algoritmos de similitud y metricas de comparación.

## Características
- **Comparación artística**: Compara pinturas por similitud visual.
- **Transformaciones**: Aplicamos transformaciones para destacar características para relevantes y afinar los resultados de la comparación.
- **Visualización interactiva**: Explore los resultados mediante visualizaciones dinámicas.

## Workflow
![Big Picture Vizel App Web](./resources/bigpicture_v2.png)

The workflow of the application includes:
1. **Ingesta de datos**: Cargar y preprocesar imágenes de obras de arte.
2.  **Extracción de características**: Extraer características visuales y contextuales numericamente utilizando redes neuronales profundas.
3. **Cálculo de similitudes**: Calcular puntuaciones de similitud entre obras de arte.
4. **Visualización**: Presentar los resultados a través de una interfaz web interactiva.

## Directory Structure
```
└── 📁tesis_project
    └── 📁backend                # servidor de la aplicacion: contiene endpoints, lógica y configuracion
        └── 📁api
        └── 📁backend
        └── 📁tests              # Pruebas unitarias y de integración.
    └── 📁experimentation
        └── 📁tesis_experimentation_v1  # Primera iteración de experimentos con datos.
        └── 📁tesis_experimentation_v2  # Segunda iteración con mejoras en los algoritmos.
        └── 📁tesis_experimentation_v3  # Iteración final con resultados optimizados.
    └── 📁frontend
    └── 📁resources             # Recursos estáticos como imágenes/documentos.
    └── 📁services
        └── 📁service-transform  # Servicio para aplicar transformaciones a las imágenes.
        └── 📁service-cnn        # Servicio para extracción de características con redes neuronales.
    └── .gitignore              # Archivos y carpetas ignorados por Git.
    └── README.md               # Documentación principal del proyecto.
```
