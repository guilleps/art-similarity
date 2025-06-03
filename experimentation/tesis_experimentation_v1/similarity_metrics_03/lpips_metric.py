import lpips
import torch
from PIL import Image
import torchvision.transforms as transforms

def calculate_lpips(img_path1, img_path2, net_type='alex'):
    loss_fn = lpips.LPIPS(net=net_type)  # alex, vgg, squeeze

    # Transformacion a tensor y normalización
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])

    # Cargar y transformar imágenes
    img1 = transform(Image.open(img_path1).convert('RGB')).unsqueeze(0)
    img2 = transform(Image.open(img_path2).convert('RGB')).unsqueeze(0)

    # Calcular distancia perceptual LPIPS
    with torch.no_grad():
        distance = loss_fn(img1, img2)

    return distance.item()

lpips_score = calculate_lpips(
    "../data/test/art_nouveau/a-y-jackson_a-copse-evening-1918.jpg", 
    "../data/test/art_nouveau/a-y-jackson_the-beothic-at-bache-post-ellesmere-island-1928.jpg"
    )
print(f"LPIPS Score: {lpips_score:.4f}")
