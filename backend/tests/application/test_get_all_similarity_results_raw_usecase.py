import pytest
from types import SimpleNamespace
import uuid

from api.application import GetAllSimilarityResultsRawUseCase

# el resultado debe ser una lista vacía ([]).
@pytest.fixture(autouse=True)
def no_db(monkeypatch):
    # Asegura que no uses la DB por error
    monkeypatch.setattr(
        'api.application.get_all_similarity_results_raw_usecase.ImageComparisonSession.objects',
        SimpleNamespace()
    )

def test_execute_no_sessions(mocker):
    mocker.patch(
        'api.application.get_all_similarity_results_raw_usecase.ImageComparisonSession.objects',
        new=SimpleNamespace(
            prefetch_related=lambda *args, **kwargs: SimpleNamespace(order_by=lambda *a, **k: [])
        )
    )
    uc = GetAllSimilarityResultsRawUseCase()
    assert uc.execute() == []

# se incluye la sesión pero todas las transformaciones aparecen como None.
def test_execute_one_empty_session(mocker):
    fake_session = SimpleNamespace(
        id=uuid.uuid4(),
        transformedimageembedding_set=SimpleNamespace(all=lambda: []),
        similarities=SimpleNamespace(all=lambda: [])
    )
    mocker.patch(
        'api.application.get_all_similarity_results_raw_usecase.ImageComparisonSession.objects',
        new=SimpleNamespace(
            prefetch_related=lambda *a, **k: SimpleNamespace(order_by=lambda *a, **k: [fake_session])
        )
    )
    res = GetAllSimilarityResultsRawUseCase().execute()
    assert len(res) == 1
    out = res[0]
    assert out['comparison_id'] == str(fake_session.id)
    # Todos los campos _transformation deben ser None
    expected_keys = {
        'color_heat_map_transformation',
        'tone_transformation',
        'saturation_transformation',
        'brightness_transformation',
        'texture_transformation',
        'contrast_transformation',
    }
    assert expected_keys.issubset(out.keys())
    assert all(out[k] is None for k in expected_keys)

# Se mapea correctamente cada tipo de similitud (contrast, hsv_hue, etc.).
# Se redondea bien el valor (round(similarity_score, 4)).
def test_execute_full_session(mocker):
    session_id = uuid.uuid4()
    embeddings = [
        SimpleNamespace(embedding_url='url1', image_index=1),
        SimpleNamespace(embedding_url='url2', image_index=2),
    ]
    similarities = [
        SimpleNamespace(transform_type='contrast', similarity_score=0.123456, file_1='url1', file_2='url2'),
        SimpleNamespace(transform_type='hsv_hue', similarity_score=0.987654, file_1='url1', file_2='url2'),
        SimpleNamespace(transform_type='heat_color_map', similarity_score=0.5555, file_1='url1', file_2='url2'),
    ]
    fake_session = SimpleNamespace(
        id=session_id,
        transformedimageembedding_set=SimpleNamespace(all=lambda: embeddings),
        similarities=SimpleNamespace(all=lambda: similarities)
    )
    mocker.patch(
        'api.application.get_all_similarity_results_raw_usecase.ImageComparisonSession.objects',
        new=SimpleNamespace(
            prefetch_related=lambda *a, **k: SimpleNamespace(order_by=lambda *a, **k: [fake_session])
        )
    )
    res = GetAllSimilarityResultsRawUseCase().execute()[0]
    assert res['contrast_transformation'] == round(0.123456, 4)
    assert res['tone_transformation'] == round(0.987654, 4)
    assert res['color_heat_map_transformation'] == round(0.5555, 4)
    # Campos no establecidos deben seguir siendo None
    for key in ('saturation_transformation', 'brightness_transformation', 'texture_transformation'):
        assert res[key] is None


# : si un tipo está ausente en similarities, su campo correspondiente debe ser None.
def test_execute_partial_similarities(mocker):
    session_id = uuid.uuid4()
    embeddings = [ SimpleNamespace(embedding_url='url1', image_index=1) ]
    similarities = []  # ninguna similitud
    fake_session = SimpleNamespace(
        id=session_id,
        transformedimageembedding_set=SimpleNamespace(all=lambda: embeddings),
        similarities=SimpleNamespace(all=lambda: similarities)
    )
    mock_qs = [fake_session]
    mocker.patch(
        'api.application.get_all_similarity_results_raw_usecase.ImageComparisonSession.objects',
        new=SimpleNamespace(
            prefetch_related=lambda *a, **k: SimpleNamespace(order_by=lambda *a, **k: mock_qs)
        )
    )
    res = GetAllSimilarityResultsRawUseCase().execute()[0]
    assert res['comparison_id'] == str(session_id)
    assert res['contrast_transformation'] is None
    assert res['tone_transformation'] is None
    # Verifica también otros campos
    for key in ('saturation_transformation', 'brightness_transformation', 'texture_transformation', 'color_heat_map_transformation'):
        assert res[key] is None
