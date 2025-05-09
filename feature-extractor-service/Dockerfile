FROM tensorflow/serving

ENV MODEL_NAME=efficientnet

# Copia el modelo a la carpeta que TF Serving espera
COPY model /models/${MODEL_NAME}

# Expone el puerto REST por defecto
EXPOSE 8501

# Comando por defecto
CMD ["--rest_api_port=8501", "--model_name=efficientnet", "--model_base_path=/models/efficientnet"]
