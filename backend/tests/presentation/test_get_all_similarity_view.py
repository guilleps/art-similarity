import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_get_similarity_paginated_success(mocker, api_client):
    fake_page = 2
    fake_limit = 5
    fake_offset = (fake_page - 1) * fake_limit

    # Simula datos paginados
    fake_data = [
        {"comparison_id": "x1", "contrast_transformation": 0.1},
        {"comparison_id": "x2", "contrast_transformation": 0.2}
    ]
    mocker.patch(
        'api.presentation.get_all_similarity_view.GetSimilarityResultsPagUseCase.execute',
        return_value=fake_data
    )
    mocker.patch(
        'api.presentation.get_all_similarity_view.ImageComparisonSession.objects.count',
        return_value=42
    )

    url = reverse('get_all_similarity_results')  # Asegúrate de que coincida con tu urls.py
    response = api_client.get(url, {'page': fake_page, 'limit': fake_limit})

    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 42
    assert data['results'] == fake_data

@pytest.mark.parametrize("params", [
    ({'page': 'NaN', 'limit': '10'}),
    ({'page': '1', 'limit': 'foo'}),
])
def test_get_similarity_paginated_bad_params(mocker, api_client, params):
    url = reverse('get_all_similarity_results')
    response = api_client.get(url, params)
    assert response.status_code == 500
    assert 'error' in response.json()

@pytest.mark.django_db
def test_get_similarity_paginated_error_in_use_case(mocker, api_client):
    mocker.patch(
        'api.presentation.get_all_similarity_view.GetSimilarityResultsPagUseCase.execute',
        side_effect=Exception("use case falló")
    )
    mocker.patch(
        'api.presentation.get_all_similarity_view.ImageComparisonSession.objects.count',
        return_value=0
    )

    url = reverse('get_all_similarity_results')
    response = api_client.get(url)
    assert response.status_code == 500
    assert 'error' in response.json()
    assert "use case falló" in response.json()['error']
