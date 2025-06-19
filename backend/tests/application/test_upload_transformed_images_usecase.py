import pytest
from types import SimpleNamespace
from api.application.upload_transformed_images_usecase import UploadTransformedImagesUseCase

@pytest.fixture
def patched_services(mocker):
    mock_cs = mocker.patch('api.application.upload_transformed_images_usecase.CloudStorageService')
    mock_css = mocker.patch('api.application.upload_transformed_images_usecase.ComparisonSessionService')
    mock_ts = mocker.patch('api.application.upload_transformed_images_usecase.TransformationService')
    mock_es = mocker.patch('api.application.upload_transformed_images_usecase.EmbeddingService')
    mock_ss = mocker.patch('api.application.upload_transformed_images_usecase.SimilarityService')
    # creamos instancias
    return {
        'cloud': mock_cs.return_value,
        'comp': mock_css.return_value,
        'trans': mock_ts.return_value,
        'emb': mock_es.return_value,
        'sim': mock_ss.return_value,
    }

def test_execute_calls_all_services_in_order(patched_services):
    # Preparar valores que devuelven los servicios
    patched_services['cloud'].upload_images.return_value = ['url1', 'url2']
    fake_session = SimpleNamespace(id='session-123')
    patched_services['comp'].create_session.return_value = fake_session
    patched_services['trans'].transform_images.return_value = ['tr1', 'tr2']
    patched_services['emb'].process_and_save_embeddings.return_value = ['emb1', 'emb2']
    patched_services['sim'].compute_and_save.return_value = None

    uc = UploadTransformedImagesUseCase()
    result_id = uc.execute('img1', 'img2')

    # Verificaciones
    patched_services['cloud'].upload_images.assert_called_once_with(['img1', 'img2'])
    patched_services['comp'].create_session.assert_called_once_with(['url1', 'url2'])
    patched_services['trans'].transform_images.assert_called_once_with('url1', 'url2')
    patched_services['emb'].process_and_save_embeddings.assert_called_once_with(fake_session, ['tr1', 'tr2'])
    patched_services['sim'].compute_and_save.assert_called_once_with(fake_session, ['emb1', 'emb2'])
    assert result_id == 'session-123'

def test_execute_propagates_exception_from_service(patched_services):
    patched_services['cloud'].upload_images.side_effect = RuntimeError("upload failed")
    uc = UploadTransformedImagesUseCase()
    with pytest.raises(RuntimeError):
        uc.execute('img1', 'img2')
