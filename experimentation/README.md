# Experimentos de Comparación de Similitud Compositiva de Obras de Arte

Este proyecto tiene como objetivo evaluar arquitecturas CNN (ResNet50, EfficientNetV2B0/B1, DenseNet121) para medir la **similitud compositiva** entre obras de arte a través de embeddings visuales.

## 🔧 Estructura de carpetas

```
└── 📁experimentation
    └── 📁data
    └── 📁output_data
    └── 📁similarity_calculation
        └── 📁logs
        └── cosine_similarity_metric.py
        └── euclidean_distance_metric.py
        └── mahalanobis_distance.py
    └── .gitignore
    └── architectures_cnn.py
    └── README.md
    └── requirements.txt
```


## 🚀 Cómo ejecutar los experimentos

### 1. Generar embeddings
```bash
python architectures_cnn.py
```

Esto extraerá embeddings de las imágenes en ./data/train usando las arquitecturas CNN seleccionadas. Los resultados se almacenan en ./output_data/arq_<model> y se registran automáticamente en W&B.

### 2. Calcular similitud entre obras

```bash
python similarity_calculation/cosine_similarity_metric.py
python similarity_calculation/euclidean_distance_metric.py
python similarity_calculation/mahalanobis_distance.py
```

Cada script:

* Selecciona una imagen aleatoria

* Calcula los top 3 más similares según la métrica especificada

* Guarda los resultados en logs/

* Reporta los datos automáticamente a W&B

## 📈 Resultados con Weights & Biases (wandb)

Cada experimento crea un log accesible en tu cuenta de wandb. Se registra:

* Modelo usado

* Métrica de similitud

* Imagen de referencia

* Top 3 similares

* Tiempo de procesamiento

* Desviación estándar de embeddings

Puedes visualizar tus resultados en línea, compartir reportes, o exportarlos como gráficos para tus presentaciones o tesis.

## 📦 Requisitos

Este proyecto utiliza **Python 3.12**. Puedes verificar la versión instalada ejecutando:

```bash
    python3 --version    
    python --version
```

> Instala `pip`, el gestor de paquetes de Python, si no está ya instalado.

## Instalación de Dependencias

1. Crea un entorno virtual para aislar las dependencias del proyecto:
    ```bash
    python -m venv venv
    ```

2. Activa el entorno virtual:
    - En **Linux/MacOS**:
      ```bash
      source venv/bin/activate
      ```
    - En **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```

3. Instala las dependencias desde el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4. Verifica que las dependencias se hayan instalado correctamente:
    ```bash
    pip list
    ```

5. Iniciar sesión en wandb:

    ```bash
    wandb login
    ```
