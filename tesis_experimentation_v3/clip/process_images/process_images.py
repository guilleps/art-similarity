import os
import json
from PIL import Image
from tqdm import tqdm
import torch
from transformers import CLIPProcessor, CLIPModel

# === Configuración inicial ===
INPUT_DIR = r'C:\workspace\tesis_project\experimentation\tesis_experimentation_v3\clip\process_images\similares'
OUTPUT_DIR = r'C:\workspace\tesis_project\experimentation\tesis_experimentation_v3\clip\process_images\output_embeddings_clip'
MODEL_NAME = "openai/clip-vit-base-patch32"

# === Validación del embedding (opcional) ===
def validate_embedding_format(embedding):
    return isinstance(embedding, list) and all(isinstance(x, float) for x in embedding)

# === Preprocesar imagen y extraer embedding ===
def extract_clip_embedding(image_path, model, processor, device):
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model.get_image_features(**inputs)
        return outputs[0].cpu().numpy().flatten().tolist()
    except Exception as e:
        print(f"❌ Error procesando {image_path}: {e}")
        return None

# === Guardar embedding en JSON ===
def save_embedding(embedding, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
    with open(output_path, 'w') as f:
        json.dump(embedding, f)

# === Recorrer todas las imágenes ===
def process_all_images(input_dir, output_dir):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained(MODEL_NAME).to(device)
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)

    image_files = []
    for root, _, files in os.walk(input_dir):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, f))

    total = len(image_files)
    success = 0
    failed = []

    for img_path in tqdm(image_files, desc="Extrayendo embeddings con CLIP"):
        filename = os.path.basename(img_path)
        embedding = extract_clip_embedding(img_path, model, processor, device)
        if embedding and validate_embedding_format(embedding):
            save_embedding(embedding, output_dir, filename)
            success += 1
        else:
            failed.append(filename)

    # === Reporte final ===
    print("\n📊 RESULTADOS")
    print(f"Total de imágenes procesadas: {total}")
    print(f"Embeddings generados correctamente: {success}")
    print(f"N° Errores: {len(failed)}")
    print(f"Porcentaje de éxito: {(success / total * 100):.2f}%")
    if failed:
        print("🛑 Errores en:")
        for fname in failed:
            print(f"- {fname}")

# === Ejecutar ===
if __name__ == "__main__":
    process_all_images(INPUT_DIR, OUTPUT_DIR)
