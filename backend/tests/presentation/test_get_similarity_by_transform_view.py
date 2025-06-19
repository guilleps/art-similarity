import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

def test_get_by_transform_missing_param(api_client):
    url = reverse('get_similarity_by_transform')  # asegúrate de que coincida con tu configuración
    response = api_client.get(url)
    assert response.status_code == 400
    assert response.json() == {"error": "Debe proporcionar el parámetro 'transform'"}

@pytest.mark.django_db  # aunque no accedemos a BD, añade compatibilidad
def test_get_by_transform_filtering(mocker, api_client):
    # Preparamos datos simulados
    fake_data = [
        {"par": 1, "color_heat_map_transformation": 0.1, "contrast_transformation": None},
        {"par": 2, "color_heat_map_transformation": None, "contrast_transformation": 0.2},
        {"par": 3, "color_heat_map_transformation": 0.3, "contrast_transformation": 0.4},
    ]
    # Mockeamos ejecución del use case
    mocker.patch(
        'api.presentation.get_similarity_by_transform_view.GetAllSimilarityResultsRawUseCase.execute',
        return_value=fake_data
    )
    url = reverse('get_similarity_by_transform')
    response = api_client.get(url, {'transform': 'color_heat_map'})

    assert response.status_code == 200
    result = response.json()
    # Sólo los items con valor no nulo
    assert result == [
        {"par": 1, "value": 0.1},
        {"par": 3, "value": 0.3}
    ]

@pytest.mark.django_db
def test_get_by_transform_no_matches(mocker, api_client):
    mocker.patch(
        'api.presentation.get_similarity_by_transform_view.GetAllSimilarityResultsRawUseCase.execute',
        return_value=[{"par": 1, "texture_transformation": None}]
    )
    url = reverse('get_similarity_by_transform')
    response = api_client.get(url, {'transform': 'texture'})

    assert response.status_code == 200
    assert response.json() == []
