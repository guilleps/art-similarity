import pytest
from api.infrastructure.services import ComparisonSessionService
from api.domain.models import ImageComparisonSession, TransformedImageEmbedding

@pytest.mark.django_db
def test_create_session_and_embeddings(mocker):
    service = ComparisonSessionService()
    urls = ['url1.png', 'url2.jpg', 'url3.gif']

    session = service.create_session(urls)

    assert isinstance(session, ImageComparisonSession)

    embeddings = TransformedImageEmbedding.objects.filter(comparison=session).order_by('image_index')
    assert embeddings.count() == 3

    for i, emb in enumerate(embeddings, start=1):
        assert emb.image_index == i
        assert emb.transform_type == "original_image"
        assert emb.filename == urls[i-1]
        assert emb.embedding_url == urls[i-1]

@pytest.mark.django_db
def test_create_session_no_images(mocker):
    service = ComparisonSessionService()
    urls = []

    session = service.create_session(urls)

    assert isinstance(session, ImageComparisonSession)
    assert TransformedImageEmbedding.objects.filter(comparison=session).count() == 0
