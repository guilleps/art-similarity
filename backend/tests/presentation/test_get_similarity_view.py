import pytest
import uuid
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_get_similarity_result_success(mocker, api_client):
    # Datos simulados que retorna el caso de uso
    fake_payload = {
        "comparison_id": "my-id",
        "image_1": {"original_image": "url1"},
        "image_2": {"original_image": "url2"},
        "similitud": {"contrast": {"files": ["url1", "url2"], "similarity": 0.5678}}
    }
    mocker.patch(
        'api.presentation.get_similarity_view.GetSimilarityResultUseCase.execute',
        return_value=fake_payload
    )

    valid_uuid = str(uuid.uuid4())
    url = reverse('get_similarity_result', args=[str(valid_uuid)])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json() == fake_payload

@pytest.mark.django_db
def test_get_similarity_result_not_found(mocker, api_client):
    # Hacemos que el use case lance error simulando sesión no encontrada
    mocker.patch(
        'api.presentation.get_similarity_view.GetSimilarityResultUseCase.execute',
        side_effect=ValueError("No se encontró")
    )

    valid_uuid = str(uuid.uuid4())
    url = reverse('get_similarity_result', args=[str(valid_uuid)])
    response = api_client.get(url)

    assert response.status_code == 404
    assert response.json() == {"error": "No se encontró"}

@pytest.mark.django_db
def test_get_similarity_result_usecase_called(mocker, api_client):
    spy = mocker.patch(
        'api.presentation.get_similarity_view.GetSimilarityResultUseCase.execute',
        return_value={}
    )

    valid_uuid = uuid.uuid4()
    url = reverse('get_similarity_result', args=[str(valid_uuid)])
    response = api_client.get(url)

    assert response.status_code == 200
    spy.assert_called_once_with(valid_uuid)
