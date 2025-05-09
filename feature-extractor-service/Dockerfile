FROM tensorflow/tensorflow:2.19.0

ENV MODEL_NAME=efficientnet

WORKDIR /app

# Instala dependencias si las usas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script para exportar el modelo
COPY export_model.py .

# Ejecuta el script para exportar el modelo
RUN python export_model.py && mv model /models/${MODEL_NAME}

# Etapa 2: Runtime con TensorFlow Serving
FROM tensorflow/serving:2.19.0

COPY --from=0 /models /models

ENV MODEL_NAME=efficientnet

EXPOSE 8501

CMD ["--rest_api_port=8501", "--model_name=efficientnet", "--model_base_path=/models/efficientnet"]
