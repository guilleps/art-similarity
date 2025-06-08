FROM tensorflow/tensorflow:2.19.0

WORKDIR /app

COPY export_model.py .
COPY *.keras .
RUN pip install tensorflow==2.19.0
RUN python export_model.py && mv model /models/efficientnet

FROM tensorflow/serving:2.19.0
COPY --from=0 /models /models

ENV MODEL_NAME=efficientnet
EXPOSE 8501
CMD ["/usr/bin/tensorflow_model_server", "--rest_api_port=8501", "--model_name=efficientnet", "--model_base_path=/models/efficientnet"]
