import io
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def secret_key_env(monkeypatch):
    monkeypatch.setenv('UPLOAD_SECRET_KEY', 'topsecret')
    import importlib
    import api.presentation.upload_transform_view as view_mod
    importlib.reload(view_mod)

def make_image_file(name='img.jpg', content=b'data'):
    return SimpleUploadedFile(name=name, content=content, content_type='image/jpeg')

def test_upload_transform_success(mocker, api_client):
    img1 = make_image_file('a.jpg')
    img2 = make_image_file('b.jpg')
    mocker.patch(
        'api.presentation.upload_transform_view.UploadTransformedImagesUseCase.execute',
        return_value="session-xyz"
    )
    url = reverse('upload_transform')
    response = api_client.post(
        url,
        {'image_1': img1, 'image_2': img2},
        format='multipart',
        HTTP_X_SECRET_KEY='topsecret'
    )
    assert response.status_code == 201
    assert response.json() == {"comparison_id": "session-xyz"}

def test_upload_transform_missing_secret(api_client):
    img1 = make_image_file('a.jpg'); img2 = make_image_file('b.jpg')
    url = reverse('upload_transform')
    response = api_client.post(
        url,
        {'image_1': img1, 'image_2': img2},
        format='multipart'
    )
    assert response.status_code == 403
    assert 'invalid' in response.json()['error'].lower()

def test_upload_transform_missing_file(api_client):
    url = reverse('upload_transform')
    response = api_client.post(
        url,
        {'image_1': make_image_file()},
        format='multipart',
        HTTP_X_SECRET_KEY='topsecret'
    )
    assert response.status_code == 400
    assert 'must be included' in response.json()['error']

def test_upload_transform_usecase_error(mocker, api_client):
    img1 = make_image_file(); img2 = make_image_file()
    mocker.patch(
        'api.presentation.upload_transform_view.UploadTransformedImagesUseCase.execute',
        side_effect=Exception("ups")
    )
    url = reverse('upload_transform')
    response = api_client.post(
        url,
        {'image_1': img1, 'image_2': img2},
        format='multipart',
        HTTP_X_SECRET_KEY='topsecret'
    )
    assert response.status_code == 500
    assert response.json()['error'] == "ups"
