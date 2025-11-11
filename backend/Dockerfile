FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN echo "[codecarbon]" > /root/.codecarbon.config && \
    echo "api_endpoint = https://api.codecarbon.io" >> /root/.codecarbon.config && \
    echo "organization_id = d6e25e23-ccc0-4bb1-8669-ca4dfe63cf7c" >> /root/.codecarbon.config && \
    echo "project_id = 567237e0-296f-48a9-a3f3-fc5e9ed45d3d" >> /root/.codecarbon.config && \
    echo "experiment_id = ${EXPERIMENT_ID}" >> /root/.codecarbon.config && \
    echo "api_key = ${CODECARBON_API_KEY}" >> /root/.codecarbon.config && \
    echo "save_to_api = True" >> /root/.codecarbon.config && \
    echo "offline_mode = False" >> /root/.codecarbon.config && \
    echo "output_dir = /tmp" >> /root/.codecarbon.config && \
    echo "save_to_file = False" >> /root/.codecarbon.config

ENV EXPERIMENT_ID=${EXPERIMENT_ID}
ENV CODECARBON_API_KEY=${CODECARBON_API_KEY}

EXPOSE 8000

CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]