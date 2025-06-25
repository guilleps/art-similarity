import pytest
from types import SimpleNamespace
from django.core.exceptions import ObjectDoesNotExist
from api.application import GetSimilarityResultUseCase

@pytest.mark.django_db
def test_execute_session_not_found(mocker):
    mocker.patch(
        'api.application.get_similarity_result_usecase.ImageComparisonSession.objects.get',
        side_effect=ObjectDoesNotExist
    )
    uc = GetSimilarityResultUseCase()
    comp_id = 'id-inexistente'
    with pytest.raises(ValueError) as exc:
        uc.execute(comp_id)
    assert comp_id in str(exc.value)

@pytest.mark.django_db
def test_execute_empty_data(mocker):
    fake_session = object()
    # get() devuelve la sesión ficticia
    mocker.patch(
        'api.application.get_similarity_result_usecase.ImageComparisonSession.objects.get',
        return_value=fake_session
    )
    # filter() sobre embeddings y similitudes devuelve listas vacías
    mocker.patch(
        'api.application.get_similarity_result_usecase.TransformedImageEmbedding.objects.filter',
        return_value=[]
    )
    mocker.patch(
        'api.application.get_similarity_result_usecase.SimilarityMetricResult.objects.filter',
        return_value=[]
    )

    uc = GetSimilarityResultUseCase()
    res = uc.execute('algún-id')
    assert res == {
        'comparison_id': 'algún-id',
        'image_1': {},
        'image_2': {},
        'similitud': {}
    }

@pytest.mark.django_db
def test_execute_populated_data_corrected(mocker):
    fake_session = object()
    mocker.patch(
        'api.application.get_similarity_result_usecase.ImageComparisonSession.objects.get',
        return_value=fake_session
    )

    emb1 = SimpleNamespace(image_index=1, transform_type="original_image",
                           image_url="url1_img", embedding_url="url1_emb")
    emb2 = SimpleNamespace(image_index=2, transform_type="color",
                           image_url="url2_img", embedding_url="url2_emb")
    embeddings_list = [emb1, emb2]

    def fake_filter_embeddings(comparison):
        return embeddings_list
    mocker.patch(
        'api.application.get_similarity_result_usecase.TransformedImageEmbedding.objects.filter',
        side_effect=fake_filter_embeddings
    )

    # 2️⃣ Al filtrar por file_1/file_2, necesitamos otro comportamiento
    def fake_filter_lookup(**kwargs):
        emb_url = kwargs.get('embedding_url')
        match = next((e for e in embeddings_list if e.embedding_url == emb_url), None)
        return SimpleNamespace(first=lambda: match)
    # Parcheamos el mismo filter pero con condicional según args
    mocker.patch(
        'api.application.get_similarity_result_usecase.TransformedImageEmbedding.objects.filter',
        side_effect=lambda *args, **kwargs: (
            embeddings_list if 'comparison' in kwargs and 'embedding_url' not in kwargs
            else fake_filter_lookup(**kwargs)
        )
    )

    sim = SimpleNamespace(transform_type="color", file_1="url2_emb", file_2="url1_emb", similarity_score=0.333333)
    mocker.patch(
        'api.application.get_similarity_result_usecase.SimilarityMetricResult.objects.filter',
        return_value=[sim]
    )

    uc = GetSimilarityResultUseCase()
    res = uc.execute('test-id')

    assert res['comparison_id'] == 'test-id'
    assert res['image_1']['original_image'] == "url1_emb"
    assert res['image_2']['color']['image_transformed'] == "url2_img"
    assert res['similitud']['color']['similarity'] == round(0.333333, 4)
    assert res['similitud']['color']['files'][0] == "url2_img"

