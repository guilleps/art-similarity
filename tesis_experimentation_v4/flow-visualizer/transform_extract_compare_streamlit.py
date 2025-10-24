import os
import shutil
import cv2
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from utils_transformations import (
    apply_contrast_enhancement,
    apply_texture_direction,
    apply_color_distribution_map,
    apply_hsv_channels
)

class VGG19EmbeddingExtractor:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = models.vgg19(weights=models.VGG19_Weights.IMAGENET1K_V1).to(self.device)
        self.model.eval()
        for param in self.model.parameters():
            param.requires_grad = False
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])

    def extract_embedding(self, image_path: str) -> list:
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            x = self.model.features(image_tensor)
            x = self.model.avgpool(x)
            x = torch.flatten(x, 1)
            for i in range(6):
                x = self.model.classifier[i](x)
            embedding = x.cpu().numpy().flatten().tolist()
        return embedding

def apply_transformations(image):
    contrast = apply_contrast_enhancement(image)
    texture = apply_texture_direction(image)
    heatmap = apply_color_distribution_map(image)
    hsv = apply_hsv_channels(image)
    return {
        'contrast': contrast,
        'texture': texture,
        'heatmap': heatmap,
        'hue': hsv['hue'],
        'saturation': hsv['saturation'],
        'value': hsv['value']
    }

# ---- STREAMLIT INTERFACE ----
st.set_page_config(
    page_title="🔍 Art Similarity Analyzer",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .st-bb {
        background-color: #f0f2f6;
    }
    .st-bc {
        background-color: #ffffff;
    }
    .st-cb {
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Show all transformations by default
show_contrast = True
show_texture = True
show_heatmap = True
show_hsv = True

# Main content
st.title("🎨 Analizador de Similitud de Arte")
st.markdown("---")

# File uploaders
st.header("1️⃣ Sube las imágenes para comparar")
col1, col2 = st.columns(2)
with col1:
    img1_file = st.file_uploader("Primera imagen", type=["jpg", "jpeg", "png"], key="img1")
with col2:
    img2_file = st.file_uploader("Segunda imagen", type=["jpg", "jpeg", "png"], key="img2")

if img1_file and img2_file:
    # Initialize progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Load and display original images
    status_text.text("🔍 Cargando y procesando imágenes...")
    progress_bar.progress(10)
    
    extractor = VGG19EmbeddingExtractor()
    img1_np = np.array(Image.open(img1_file).convert("RGB"))
    img2_np = np.array(Image.open(img2_file).convert("RGB"))
    
    # Display original images
    st.header("2️⃣ Imágenes originales")
    col1, col2 = st.columns(2)
    with col1:
        st.image(img1_np, caption="Imagen 1", width='stretch')
    with col2:
        st.image(img2_np, caption="Imagen 2", width='stretch')
    
    # Apply transformations
    status_text.text("🔄 Aplicando transformaciones...")
    progress_bar.progress(30)
    
    transforms1 = apply_transformations(img1_np)
    transforms2 = apply_transformations(img2_np)
    
    # Create temp directory
    os.makedirs("temp_streamlit", exist_ok=True)
    
    # Define transformations to show based on sidebar selection
    transform_mapping = {
        'contrast': show_contrast,
        'texture': show_texture,
        'heatmap': show_heatmap,
        'hue': show_hsv,
        'saturation': show_hsv,
        'value': show_hsv
    }
    
    transform_names = [k for k, v in transform_mapping.items() if v]
    
    if not transform_names:
        st.warning("⚠️ Por favor selecciona al menos una transformación en la barra lateral.")
    else:
        st.header("3️⃣ Resultados de similitud")
        
        # Create tabs for better organization
        tab1, tab2 = st.tabs(["📊 Resumen", "🔍 Detalles"])
        
        with tab1:
            st.subheader("Resumen de similitudes")
            similarity_scores = {}
            
            # Calculate all similarities first
            for i, name in enumerate(transform_names):
                path1 = f"temp_streamlit/img1_{name}.jpg"
                path2 = f"temp_streamlit/img2_{name}.jpg"
                
                # Save images temporarily
                if name == 'heatmap':
                    plt.imsave(path1, transforms1[name])
                    plt.imsave(path2, transforms2[name])
                else:
                    cv2.imwrite(path1, cv2.cvtColor(transforms1[name], cv2.COLOR_RGB2BGR))
                    cv2.imwrite(path2, cv2.cvtColor(transforms2[name], cv2.COLOR_RGB2BGR))
                
                # Update progress
                progress = 40 + int((i + 1) * 50 / len(transform_names))
                status_text.text(f"📊 Calculando similitud para: {name.replace('_', ' ').title()}...")
                progress_bar.progress(min(progress, 90))
                
                # Calculate similarity
                emb1 = extractor.extract_embedding(path1)
                emb2 = extractor.extract_embedding(path2)
                similarity = cosine_similarity([emb1], [emb2])[0][0]
                similarity_scores[name] = similarity
                
                # Clean up
                os.remove(path1)
                os.remove(path2)
            
            # Display similarity scores as a bar chart
            if similarity_scores:
                import pandas as pd
                import plotly.express as px
                
                df = pd.DataFrame({
                    'Transformación': [t.replace('_', ' ').title() for t in similarity_scores.keys()],
                    'Similitud': [v for v in similarity_scores.values()]
                })
                
                fig = px.bar(
                    df, 
                    x='Transformación', 
                    y='Similitud',
                    color='Similitud',
                    color_continuous_scale='Viridis',
                    range_y=(0, 1.1),
                    title='Puntuaciones de Similitud por Transformación'
                )
                fig.update_layout(yaxis_tickformat=".2f")
                st.plotly_chart(fig, use_container_width=True)
                
                # Show overall similarity
                avg_similarity = sum(similarity_scores.values()) / len(similarity_scores)
                st.metric("Similitud Promedio", f"{avg_similarity:.2%}")
        
        with tab2:
            st.subheader("Detalles de las Transformaciones")
            
            for name in transform_names:
                with st.expander(f"🔧 {name.replace('_', ' ').title()}", expanded=True):
                    if name in similarity_scores:
                        similarity = similarity_scores[name]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(transforms1[name], width='stretch')
                        with col2:
                            st.image(transforms2[name], width='stretch')

                        name_map = {
                            'heatmap': 'Mapa de calor de color',
                            'texture': 'Textura',
                            'contrast': 'Contraste',
                            'hue': 'Tono',
                            'saturation': 'Saturación',
                            'value': 'Brillo'
                        }
                        display_name = name_map.get(name, name.replace('_', ' ').title())
                        
                        # Show similarity score with a nice gauge
                        st.metric(
                            label=f"Similitud en {display_name}", 
                            value=f"{similarity:.2%}",
                            help=f"Similitud basada en características de {display_name.lower()}"
                        )
                        st.progress(similarity)
    
    # Clean up
    shutil.rmtree("temp_streamlit", ignore_errors=True)
    progress_bar.progress(100)
    status_text.success("✅ Análisis completado!")
    
    # Add some space at the bottom
    st.markdown("---")
    st.markdown("### 📝 Notas")
    st.info("""
    - Los valores van de 0 (sin similitud) a 1 (idénticas)
    - Las transformaciones se aplican individualmente a cada imagen
    """)
