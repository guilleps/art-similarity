# app/main.py
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from app.model_clip import generate_embedding
from app.cloudinary_config import upload_file_to_cloudinary
from io import BytesIO
from PIL import Image
import uuid
import logging
from app.logger_config import setup_logging

logger = logging.getLogger(__name__)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/embed":
            self.send_error(404, "Endpoint no encontrado")
            logger.warning("Intento a endpoint no definido: %s", self.path)
            return

        logger.info("Recibiendo imagen para generar embedding...")

        content_length = int(self.headers['Content-Length'])
        file_data = self.rfile.read(content_length)

        # Guardar temporal
        os.makedirs("/tmp", exist_ok=True)
        temp_image_path = "/tmp/uploaded_image.jpg"
        with open(temp_image_path, "wb") as f:
            f.write(file_data)

        # Generar embedding
        embedding = generate_embedding(temp_image_path)
        logger.info("Embedding generado con éxito.")

        # Guardar embedding en JSON
        embedding_id = str(uuid.uuid4())
        json_path = f"/tmp/embedding_{embedding_id}.json"
        with open(json_path, "w") as f:
            json.dump(embedding, f)

        # Subir JSON a Cloudinary
        secure_url = upload_file_to_cloudinary(json_path, f"embedding_{embedding_id}.json")
        logger.info("Embedding subido a Cloudinary: %s", secure_url)
        
        # Responder con URL del embedding
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"embedding_url": secure_url}).encode())

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8002):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servicio CNN corriendo en puerto {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002))  # usa el puerto 8002 por defecto si PORT no está definida
    run(port=port)
