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
    embeddings = {1: {'foo': 'url1'}, 2: {'foo': 'url2'}}

    service.compute_and_save(fake_session, embeddings)

    results = SimilarityMetricResult.objects.filter(comparison=fake_session)
    assert results.count() == 1
    saved = results.first()
    assert saved.transform_type == 'foo'
    assert abs(saved.similarity_score - 0.8) < 1e-6
    assert saved.file_1 == 'url1'
    assert saved.file_2 == 'url2'

@pytest.mark.django_db
def test_compute_and_save_multiple_transforms(mocker):
    mocker.patch(
        'api.infrastructure.services.similarity_service.ExternalRequestService.fetch_json',
        side_effect=[ [1,1], [0,1], [2,2], [1,0] ]
    )
    mocker.patch(
        'api.infrastructure.services.similarity_service.cosine_similarity',
        side_effect=[ [[0.7]], [[0.3]] ]
    )

    service = SimilarityService()
    fake_session = ImageComparisonSession.objects.create()
    embeddings = {
        1: {'a': 'urlA1', 'b': 'urlB1'},
        2: {'a': 'urlA2', 'b': 'urlB2'}
    }

    service.compute_and_save(fake_session, embeddings)
    results = {r.transform_type: r.similarity_score for r in SimilarityMetricResult.objects.filter(comparison=fake_session)}
    assert pytest.approx(results['a'], rel=1e-6) == 0.7
    assert pytest.approx(results['b'], rel=1e-6) == 0.3
