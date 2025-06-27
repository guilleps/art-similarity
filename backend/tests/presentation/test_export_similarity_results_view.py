import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

def test_export_similarity_results_success(mocker, api_client):
    fake_data = {
        "par": {
            "1": {
                "image_1": "https://res.cloudinary.com/dnydakj9z/image/upload/v1749831160/dot1wmhgjgktl68nboap.jpg",
                "image_2": "https://res.cloudinary.com/dnydakj9z/image/upload/v1749831160/hvy6qmma5kul9tkiz4bs.jpg",
                "contrast": {
                    "files": {
                        "image_1": "https://res.cloudinary.com/dnydakj9z/image/upload/v1749831163/uugjx4vhlzszho3cqera.jpg",
                        "image_2": "https://res.cloudinary.com/dnydakj9z/image/upload/v1749831166/gk0k7vzev6hmlzfdgtqg.jpg"
                    },
                    "similarity": 0.9876
                }
            }
        }
    }

    mocker.patch(
        'api.presentation.export_similarity_results_view.ExportSimilarityResultsUseCase.execute',
        return_value=fake_data
    )

    url = reverse('export_similarity_results')
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.json() == fake_data


def test_export_similarity_results_failure(mocker, api_client):
    mocker.patch(
        'api.presentation.export_similarity_results_view.ExportSimilarityResultsUseCase.execute',
        side_effect=Exception("fallo interno")
    )

    url = reverse('export_similarity_results')
    response = api_client.get(url)

    assert response.status_code == 500
    assert "error" in response.json()
    assert "fallo interno" in response.json()["error"]