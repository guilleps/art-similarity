import pytest
from types import SimpleNamespace
import requests

def test_fetch_json_success(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    response = SimpleNamespace(
        raise_for_status=lambda: None,
        json=lambda: {"key": "value"}
    )
    mocker.patch('api.infrastructure.services.external_request_service.requests.get', return_value=response)

    result = ExternalRequestService.fetch_json('http://fake.url')
    assert result == {"key": "value"}

def test_fetch_json_retry_then_success(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    resp_error = SimpleNamespace(raise_for_status=lambda: (_ for _ in ()).throw(requests.RequestException("err")))
    resp_ok = SimpleNamespace(raise_for_status=lambda: None, json=lambda: {"ok": True})
    mock_get = mocker.patch('api.infrastructure.services.external_request_service.requests.get',
                            side_effect=[resp_error, resp_ok])

    result = ExternalRequestService.fetch_json('http://fake')
    assert result == {"ok": True}
    assert mock_get.call_count == 2

def test_fetch_json_failure(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    mocker.patch('api.infrastructure.services.external_request_service.requests.get',
                 side_effect=requests.RequestException("fail"))
    with pytest.raises(Exception) as exc:
        ExternalRequestService.fetch_json('http://fake')
    assert "Error al obtener JSON" in str(exc.value)

def test_fetch_bytes_success(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    resp = SimpleNamespace(raise_for_status=lambda: None, content=b'bytes')
    mocker.patch('api.infrastructure.services.external_request_service.requests.get', return_value=resp)

    svc = ExternalRequestService()
    result = svc.fetch_bytes('http://fake')
    assert result == b'bytes'

def test_fetch_bytes_failure(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    mocker.patch('api.infrastructure.services.external_request_service.requests.get',
                 side_effect=requests.RequestException("net err"))

    svc = ExternalRequestService(retries=2, timeout=1)
    with pytest.raises(Exception) as exc:
        svc.fetch_bytes('http://fake')
    assert "Error al obtener bytes" in str(exc.value)

def test_post_image_and_get_json_success(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    resp = SimpleNamespace(raise_for_status=lambda: None, json=lambda: {"resp": 1})
    mocker.patch('api.infrastructure.services.external_request_service.requests.post', return_value=resp)

    svc = ExternalRequestService()
    result = svc.post_image_and_get_json('http://fake', b'data', headers={'h':'v'})
    assert result == {"resp": 1}

def test_post_image_and_get_json_failure(mocker):
    from api.infrastructure.services.external_request_service import ExternalRequestService
    mocker.patch('api.infrastructure.services.external_request_service.requests.post',
                 side_effect=requests.RequestException("post err"))
    svc = ExternalRequestService(retries=1, timeout=1)
    with pytest.raises(Exception) as exc:
        svc.post_image_and_get_json('http://fake', b'data', headers={})
    assert "Error al postear imagen" in str(exc.value)
