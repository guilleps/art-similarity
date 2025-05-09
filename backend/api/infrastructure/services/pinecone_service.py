from pinecone import Pinecone
from pinecone import ServerlessSpec
import os

from api.infrastructure.exceptions import PineconeQueryError, PineconeUpsertError

api_key = os.environ.get("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY is not defined in .env")

pc = Pinecone(api_key=api_key)

PINECONE_DIMENSION = 1280 

index_name = os.environ.get('INDEX_NAME')

# evalua si el indice existe, sino crea uno neuvo
if index_name not in [index.name for index in pc.list_indexes()]:
    print(f"Index '{index_name}' not found. Creating new index...")
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
    print(f"Index '{index_name}' already exists. Using existing index.")

index = pc.Index(index_name)

def store_embedding(image_id, embedding, image_url):
    try:
        index.upsert(
            vectors=[(image_id, embedding, {'image_url': image_url})],
            namespace="workspacemoon"
        )
    except Exception as e:
        raise PineconeUpsertError() from e


def search_similar_images(query_embedding, top_k=3, image_id=None):
    try:
        query = {
            'vector': query_embedding,
            'top_k': top_k,
            'include_values': True,
            'include_metadata': True,
            'namespace': "workspacemoon"
        }

        result = index.query(**query)
    except Exception as e:
        raise PineconeQueryError() from e

    similar_images = []

    if 'matches' in result and result['matches']:
        for match in result['matches']:
            if match['id'] != image_id:
                id = match['id']
                image_url = match['metadata'].get('image_url')
                score = match['score']
                similarity_percentage = round(score * 100)

                similar_images.append({
                    'id': id,
                    'image_url': image_url, 
                    'similarity_percentage': similarity_percentage
                })
    else:
        print("No se encontraron imágenes similares.")

    return similar_images