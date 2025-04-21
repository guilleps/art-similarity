from pinecone import Pinecone
from pinecone import ServerlessSpec
import os

api_key = os.environ.get("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY no está definido en .env")

pc = Pinecone(api_key=api_key)

PINECONE_DIMENSION = 1280 

index_name = os.environ.get('INDEX_NAME')

# Verifica si el índice ya existe antes de crear uno nuevo
if index_name not in [index.name for index in pc.list_indexes()]:
    print(f"Índice '{index_name}' no encontrado. Creando nuevo índice...")
    pc.create_index(
        name=index_name,
        dimension=PINECONE_DIMENSION,
        metric='cosine',
        spec=ServerlessSpec(
            cloud="aws",
            region=os.environ.get("PINECONE_ENV_REGION"),
        )
    )
else:
    print(f"Índice '{index_name}' ya existe. Usando índice existente.")

index = pc.Index(index_name)

def store_embedding(image_id, embbeding, image_url):
    index.upsert(
        vectors=[
            (image_id, embbeding, { 'image_url': image_url })
        ],
        namespace="workspacemoon"
    )
