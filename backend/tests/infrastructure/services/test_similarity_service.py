import pytest
from sklearn.metrics.pairwise import cosine_similarity
from api.infrastructure.services.similarity_service import SimilarityService
from api.domain.models import ImageComparisonSession, SimilarityMetricResult

@pytest.mark.django_db
def test_compute_and_save_creates_records(mocker):
    # Mocks
    mocker.patch(
        'api.infrastructure.services.similarity_service.ExternalRequestService.fetch_json',
        side_effect=[
            [1, 0, 0],  # embedding vector 1
            [0.5, 0.5, 0.5]  # embedding vector 2
        ]
    )
    # Mock cosine_similarity to return known value
    mocker.patch(
        'api.infrastructure.services.similarity_service.cosine_similarity',
        return_value=[[0.8]]
    )

    service = SimilarityService()
    fake_session = ImageComparisonSession.objects.create()
    embeddings = {1: {'foo': 'url1'}, 2: {'foo': 'url2'}} # transformación simulada 'foo'

    service.compute_and_save(fake_session, embeddings)

    results = SimilarityMetricResult.objects.filter(comparison=fake_session)
    assert results.count() == 1
    saved = results.first()
    assert saved.transform_type == 'foo'
    assert abs(saved.similarity_score - 0.8) < 1e-6
    assert saved.file_1 == 'url1'
    assert saved.file_2 == 'url2'

# garantizar que al subir la imagen no se rompa si hay enalces faltantes==None, y no guarde resultados de similitud inválidos
@pytest.mark.django_db
@pytest.mark.parametrize("embeddings, expected_count", [
    (
        {1: {'a': None}, 2: {'a': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831160/hvy6qmma5kul9tkiz4bs.jpg'}},  # file_1 es None
        0
    ),
    (
        {1: {'a': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831160/dot1wmhgjgktl68nboap.jpg'}, 2: {'a': None}},  # file_2 es None
        0
    ),
    (
        {1: {}, 2: {}},  # no hay claves en absoluto
        0
    ),
])
def test_compute_and_save_skips_missing_urls(mocker, embeddings, expected_count):
    mocker.patch(
        'api.infrastructure.services.similarity_service.ExternalRequestService.fetch_json',
        return_value=[1, 2, 3]
    )
    mocker.patch(
        'api.infrastructure.services.similarity_service.cosine_similarity',
        return_value=[[0.999]]
    )

    service = SimilarityService()
    session = ImageComparisonSession.objects.create()

    # sin lanzar excepción
    service.compute_and_save(session, embeddings)

    assert SimilarityMetricResult.objects.filter(comparison=session).count() == expected_count
