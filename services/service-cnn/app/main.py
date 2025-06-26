import os
import uuid
import json
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse
from app.logger_config import setup_logging
from app.model_clip import generate_embedding
from app.cloudinary_config import upload_file_to_cloudinary
import logging
from onnxruntime import InferenceSession

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/embed")
async def embed(request: Request):
    logger.info(f"Content-Type recibido: { request.headers.get('content-type') }")
    try:
        logger.info("Recibiendo imagen para generar embedding...")

        image_bytes = await request.body()

        # Guardar temporal
        os.makedirs("/tmp", exist_ok=True)
        temp_image_path = "/tmp/uploaded_image.jpg"
        with open(temp_image_path, "wb") as f:
            # f.write(await file.read())
            f.write(image_bytes)

        # Generar embedding
        embedding = generate_embedding(temp_image_path)

        # Guardar embedding en JSON
        embedding_id = str(uuid.uuid4())
        json_path = f"/tmp/embedding_{embedding_id}.json"
        with open(json_path, "w") as f:
            json.dump(embedding, f)

        # Subir JSON a Cloudinary
        secure_url = upload_file_to_cloudinary(json_path, f"embedding_{embedding_id}.json")
        logger.info("Embedding subido a Cloudinary: %s", secure_url)

        return JSONResponse(status_code=200, content={"embedding_url": secure_url})

    except Exception as e:
        logger.exception("Error al procesar imagen:")
        raise HTTPException(status_code=500, detail=str(e))
    