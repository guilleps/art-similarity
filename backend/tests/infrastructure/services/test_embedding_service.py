import pytest
from types import SimpleNamespace
from api.infrastructure.services.embedding_service import EmbeddingService
from api.domain.models import ImageComparisonSession, TransformedImageEmbedding
from api.infrastructure.exceptions.embedding_exceptions import EmbeddingModelError

@pytest.mark.django_db
def test_process_and_save_embeddings_success(mocker):
    # Mock de ExternalRequestService
    mock_ext = mocker.patch('api.infrastructure.services.embedding_service.ExternalRequestService')
    inst = mock_ext.return_value
    inst.fetch_bytes.return_value = b'fakebytes'
    inst.post_image_and_get_json.side_effect = [
        {'embedding_url': 'http://emb1'},
        {'embedding_url': 'http://emb2'}
    ]

    # Crear sesión real en la BD
    session = ImageComparisonSession.objects.create()

    transformed = {
        "imagen_1": {"contrast": "url_c1"},
        "imagen_2": {"texture": "url_t2", "original_image": "url_o2"}
    }

    svc = EmbeddingService()
    result = svc.process_and_save_embeddings(session, transformed)

    assert result == {
        1: {"contrast": "http://emb1"},
        2: {"texture": "http://emb2"}
    }

    db_embs = list(TransformedImageEmbedding.objects.filter(comparison=session).order_by('image_index'))
    assert len(db_embs) == 2
    assert db_embs[0].embedding_url == 'http://emb1'
    assert db_embs[0].transform_type == 'contrast'
    assert db_embs[1].transform_type == 'texture'

@pytest.mark.django_db
def test_process_and_save_embeddings_failure(mocker):
    mock_ext = mocker.patch('api.infrastructure.services.embedding_service.ExternalRequestService')
    inst = mock_ext.return_value
    inst.fetch_bytes.return_value = b''
    inst.post_image_and_get_json.side_effect = Exception("CNN unreachable")

    session = ImageComparisonSession.objects.create()
    transformed = {"imagen_1": {"contrast": "url_c1"}, "imagen_2": {}}

    svc = EmbeddingService()
    with pytest.raises(EmbeddingModelError):
        svc.process_and_save_embeddings(session, transformed)

    assert TransformedImageEmbedding.objects.filter(comparison=session).count() == 0
