import os
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications.efficientnet import preprocess_input 

TRAIN_DIR = 'C:/workspace/data/train' 
IMG_SIZE = (224, 224)            
BATCH_SIZE = 32

def build_dataframe(dataset_dir):
    data = []
    for label in os.listdir(dataset_dir):
        label_dir = os.path.join(dataset_dir, label)
        if os.path.isdir(label_dir):
            for fname in os.listdir(label_dir):
                if fname.endswith(('.jpg', '.png', '.jpeg')):
                    data.append({'path': os.path.join(label_dir, fname), 'label': label})
    return pd.DataFrame(data)

df = build_dataframe(TRAIN_DIR)

df_sampled, _ = train_test_split(df, train_size=0.2, stratify=df['label'], random_state=42)  # Ej: 20% del total

num_classes = df_sampled['label'].nunique()

# Resto del pipeline
paths = df_sampled['path'].tolist()
labels = df_sampled['label'].astype('category').cat.codes.tolist()

def load_and_preprocess(path, label):
    image = tf.io.read_file(path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, IMG_SIZE)
    image = preprocess_input(image)
    return image, tf.one_hot(label, depth=num_classes)

ds = tf.data.Dataset.from_tensor_slices((paths, labels))
ds = ds.map(load_and_preprocess).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

import matplotlib.pyplot as plt

df_sampled['label'].value_counts().plot(kind='bar')
plt.title("Distribución de clases en el submuestreo estratificado")
plt.show()
