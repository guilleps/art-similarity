import logging
import onnxruntime as ort
from PIL import Image
from torchvision import transforms
import numpy as np

logger = logging.getLogger(__name__)

session = ort.InferenceSession("clip_vision.onnx", providers=["CPUExecutionProvider"])

preprocess = transforms.Compose([
    transforms.Resize(224),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.4815, 0.4578, 0.4082], std=[0.2686, 0.2613, 0.2758])
])

def generate_embedding(image_path: str):
    try:
        logger.info("Procesando imagen para generar embedding...")
        image = Image.open(image_path).convert("RGB")
        if image.mode != "RGB":
            image = image.convert("RGB")

        input_tensor = preprocess(image).unsqueeze(0).numpy().astype(np.float32)
        outputs = session.run(None, {"pixel_values": input_tensor})
        
        embedding = np.array(outputs[0])[0, 0, :]
        logger.info("Embedding generado con éxito. Shape: %s", embedding.shape)

        return embedding.tolist()
    except Exception as e:
        logger.exception("Error al generar el embedding:")
        raise
        