import pytest
import requests
from types import SimpleNamespace
from api.infrastructure.services.transformation_service import TransformationService

def test_transform_images_success(mocker):
    # Configurar variable de entorno para la URL
    mocker.patch(
        'api.infrastructure.services.transformation_service.TRANSFORM_SERVICE_URL',
        'http://svc'
    )

    # Simular respuesta exitosa de requests.post
    resp = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {"img1": "t1", "img2": "t2"}
    )
    mocker.patch('api.infrastructure.services.transformation_service.requests.post', return_value=resp)

    svc = TransformationService()
    result = svc.transform_images('u1', 'u2')

    assert result == {"img1": "t1", "img2": "t2"}
    requests.post.assert_called_once_with(
        'http://svc/transform',
        json={"image_1_url": "u1", "image_2_url": "u2"}
    )

def test_transform_images_http_error(mocker):
    from requests.exceptions import HTTPError

    mocker.patch(
        'api.infrastructure.services.transformation_service.TRANSFORM_SERVICE_URL',
        'http://svc'
    )
    def raise_err():
        raise HTTPError("Bad response")
    resp = SimpleNamespace(raise_for_status=raise_err)
    mocker.patch('api.infrastructure.services.transformation_service.requests.post', return_value=resp)

    svc = TransformationService()
    with pytest.raises(HTTPError):
        svc.transform_images('u1', 'u2')
