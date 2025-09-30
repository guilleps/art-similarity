from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests
import tempfile
from transformation_core import save_transformed_images

app = FastAPI()

@app.post("/transform")
async def transform_from_urls(request: Request):
    data = await request.json()
    image_1_url = data["image_1_url"]
    image_2_url = data["image_2_url"]

    results = {}

    for idx, (label, url) in enumerate([("image_1", image_1_url), ("image_2", image_2_url)], start=1):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return JSONResponse(status_code=400, content={"error": f"Error al descargar imagen {label}"})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            temp_path = tmp_file.name

        transformed_urls = save_transformed_images(temp_path, "/tmp/outputs")
        transformed_urls["original_image"] = url  # incluir la original
        results[label] = transformed_urls

        os.remove(temp_path)

    # Puedes calcular aquí similitud si deseas y agregar un campo "similitud"
    return JSONResponse(results)
