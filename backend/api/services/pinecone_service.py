from pinecone import Pinecone
from pinecone import ServerlessSpec
import os

api_key = os.environ.get("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY is not defined in .env")

pc = Pinecone(api_key=api_key)

PINECONE_DIMENSION = 1280 

index_name = os.environ.get('INDEX_NAME')

# Verifica si el índice ya existe antes de crear uno nuevo
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
    print(f"Uploading embedding for image: {image_id}")
    query = {
        'vector': embedding,
        'top_k': 1,
        'include_values': True,
        'include_metadata': True,
        'namespace': "workspacemoon"
    }

    result = index.query(**query)
    if result['matches']:
        print("Image already exists in Pinecone. It is not uploaded again.")
    else:
        index.upsert(
            vectors=[(image_id, embedding, { 'image_url': image_url })],
            namespace="workspacemoon"
        )
        # print("Embedding successfully uploaded.")


def search_similar_images(query_embedding, top_k=3, image_id=None):
    query = {
        'vector': query_embedding,
        'top_k': top_k,
        'include_values': True,
        'include_metadata': True,
        'namespace': "workspacemoon"
    }

    result = index.query(**query)
    # print(f"Search results: {result}")

    similar_images = []

    if 'matches' in result and result['matches']:
        for match in result['matches']:
            if match['id'] != image_id:
                image_url = match['metadata'].get('image_url')
                similar_images.append(image_url)
    else:
        print("No similar images found.")

    return similar_images