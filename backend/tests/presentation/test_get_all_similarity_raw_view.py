import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.presentation.get_all_similarity_raw_view import GetAllSimilarityResultsRawUseCase

@pytest.fixture
def api_client():
    return APIClient()

def test_get_all_similarity_results_raw_success(mocker, api_client):
    fake_data = [
        {"comparison_id": "id1", "contrast_transformation": 0.1234},
        {"comparison_id": "id2", "contrast_transformation": None}
    ]
    mocker.patch(
        'api.presentation.get_all_similarity_raw_view.GetAllSimilarityResultsRawUseCase.execute',
        return_value=fake_data
    )
    url = reverse('get_all_similarity_results_raw') 
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json() == fake_data

def test_get_all_similarity_results_raw_error(mocker, api_client):
    mocker.patch(
        'api.presentation.get_all_similarity_raw_view.GetAllSimilarityResultsRawUseCase.execute',
        side_effect=Exception("algo falló")
    )
    url = reverse('get_all_similarity_results_raw')
    response = api_client.get(url)

    assert response.status_code == 500
    payload = response.json()
    assert "error" in payload
    assert "algo falló" in payload["error"]
