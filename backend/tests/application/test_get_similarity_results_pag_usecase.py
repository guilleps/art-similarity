import uuid
import pytest
from types import SimpleNamespace
from api.application import GetSimilarityResultsPagUseCase
from datetime import datetime

def test_execute_no_sessions(mocker):
    mocker.patch(
        'api.application.get_similarity_results_pag_usecase.ImageComparisonSession.objects.prefetch_related',
        return_value=SimpleNamespace(order_by=lambda *_: [])
    )
    uc = GetSimilarityResultsPagUseCase()
    assert uc.execute(offset=0, limit=5) == []

def test_execute_empty_sessions_no_embeddings_or_similarities(mocker):
    now = datetime.now()
    fake_session = SimpleNamespace(
        id=uuid.uuid4(),
        created_at=now,
        transformedimageembedding_set=SimpleNamespace(all=lambda: []),
        similarities=SimpleNamespace(all=lambda: [])
    )
    mocker.patch(
        'api.application.get_similarity_results_pag_usecase.ImageComparisonSession.objects.prefetch_related',
        return_value=SimpleNamespace(order_by=lambda *_: [fake_session])
    )
    uc = GetSimilarityResultsPagUseCase()
    res = uc.execute(offset=0, limit=1)[0]
    assert res['comparison_id'] == str(fake_session.id)
    assert res['created_at'] == now
    assert res['contrast_transformation'] is None
    assert res['tone_transformation'] is None

def test_execute_populated_session_with_data(mocker):
    now = datetime.now()
    session_id = uuid.uuid4()
    fake_session = SimpleNamespace(
        id=session_id,
        created_at=now,
        transformedimageembedding_set=SimpleNamespace(all=lambda: [
            SimpleNamespace(image_index=1, transform_type="original_image", image_url="u1_img", embedding_url="u1_emb"),
            SimpleNamespace(image_index=1, transform_type="contrast", image_url="u1_contrast_img", embedding_url="u1_contrast_emb"),
        ]),
        similarities=SimpleNamespace(all=lambda: [
            SimpleNamespace(transform_type="contrast", similarity_score=0.45678, file_1="u1_contrast_emb", file_2="u1_emb")
        ])
    )
    mocker.patch(
        'api.application.get_similarity_results_pag_usecase.ImageComparisonSession.objects.prefetch_related',
        return_value=SimpleNamespace(order_by=lambda *_: [fake_session])
    )
    uc = GetSimilarityResultsPagUseCase()
    res = uc.execute(offset=0, limit=10)[0]
    assert res['comparison_id'] == str(session_id)
    assert res['created_at'] == now
    assert res['contrast_transformation'] == round(0.45678, 4)

def test_execute_applies_offset_and_limit(mocker):
    sessions = [
        SimpleNamespace(id=uuid.uuid4(), created_at=datetime.now(),
                        transformedimageembedding_set=SimpleNamespace(all=lambda: []),
                        similarities=SimpleNamespace(all=lambda: []))
        for _ in range(5)
    ]
    obj = SimpleNamespace(prefetch_related=lambda *_: SimpleNamespace(order_by=lambda *_: sessions))
    mocker.patch(
        'api.application.get_similarity_results_pag_usecase.ImageComparisonSession.objects',
        new=obj
    )
    uc = GetSimilarityResultsPagUseCase()
    res = uc.execute(offset=1, limit=2)
    assert len(res) == 2
    assert res[0]['comparison_id'] == str(sessions[1].id)
    assert res[1]['comparison_id'] == str(sessions[2].id)

def test_execute_empty_sessions_no_embeddings_or_similarities(mocker):
    now = datetime.now()
    fake_session = SimpleNamespace(
        id=uuid.uuid4(),
        created_at=now,
        transformedimageembedding_set=SimpleNamespace(all=lambda: []),
        similarities=SimpleNamespace(all=lambda: [])
    )
    mocker.patch(
        'api.application.get_similarity_results_pag_usecase.ImageComparisonSession.objects.prefetch_related',
        return_value=SimpleNamespace(order_by=lambda *_: [fake_session])
    )
    uc = GetSimilarityResultsPagUseCase()
    res = uc.execute(offset=0, limit=1)[0]
    assert res['comparison_id'] == str(fake_session.id)
    assert res['created_at'] == now
    assert res['contrast_transformation'] is None
    assert res['tone_transformation'] is None