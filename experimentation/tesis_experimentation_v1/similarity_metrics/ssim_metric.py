from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import cv2
import numpy as np


def mse_loss(imageA, imageB): # suma de la diferencia entre 2 imgs
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    return err

def ssim_metric(imageA, imageB, title):

    mse = mse_loss(imageA, imageB)
    s_metric, _ = ssim(imageA, imageB, full=True)

    fig = plt.figure(title)
    plt.suptitle(f"MSE: {mse:.2f}, SSIM: {s_metric:.2f}")

    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap="gray")
    plt.axis("off")

    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap="gray")
    plt.axis("off")

    plt.show()

imageA = cv2.imread("../data/test/art_nouveau/a-y-jackson_a-copse-evening-1918.jpg")
imageB = cv2.imread("../data/test/art_nouveau/a-y-jackson_the-beothic-at-bache-post-ellesmere-island-1928.jpg")

# escala de grises
imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

fig = plt.figure("Imagenes")
images = [('Original', imageA), ('Comparacion', imageB)]

for (i, (name, image)) in enumerate(images):
    ax = fig.add_subplot(1, 3, i + 1)
    ax.set_title(name)
    plt.imshow(image, cmap="gray")
    plt.axis("off")

plt.show()

ssim_metric(imageA, imageA, "Original vs. Original")
ssim_metric(imageA, imageB, "Original vs. Contrast")