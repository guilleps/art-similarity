from pinecone import Pinecone
from pinecone import ServerlessSpec
import os

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

PINECONE_DIMENSION = 156

index_name = os.environ.get('INDEX_NAME')
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=PINECONE_DIMENSION,
        metric='cosine',
        spec=ServerlessSpec(
            cloud=os.environ.get("PINECONE_CLOUD"),
            region=os.environ.get("PINECONE_REGION"),
        )
    )

index = pc.Index(index_name)

def store_embedding(image_id, embbeding, image_url):
    index.upsert(
        vectors=[
            (image_id, embbeding, { 'image_url': image_url })
        ],
        namespace=os.environ.get("PINECONE_NAMESPACE")
    )
