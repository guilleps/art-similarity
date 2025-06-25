import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from api.domain.models import ImageComparisonSession, TransformedImageEmbedding, SimilarityMetricResult

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def secret_key_env(monkeypatch):
    monkeypatch.setenv('UPLOAD_SECRET_KEY', 'topsecret')
    import importlib
    import api.presentation.upload_transform_view as view_mod
    importlib.reload(view_mod)

@pytest.mark.django_db
def test_similarity_flow(mocker, api_client):

    # mock clpudinary
    mocker.patch(
        'api.infrastructure.services.cloudinary_service.CloudStorageService.upload_images',
        return_value=[
            'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831160/dot1wmhgjgktl68nboap.jpg', 
            'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831160/hvy6qmma5kul9tkiz4bs.jpg'
        ]
    )

    # mock de transformación de imagenes
    mocker.patch(
        'api.infrastructure.services.transformation_service.TransformationService.transform_images',
        return_value={
            'image_1': {
                'contrast': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831163/uugjx4vhlzszho3cqera.jpg',
                'texture': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831163/smevzpwklmmakxg2kela.jpg',
                'heat_color_map': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831164/vf37lvakqsmqetyfecxn.jpg',
                'hsv_hue': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831164/whtyfjje7nn5xq6qpko4.jpg',
                'hsv_saturation': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831165/jjigmumthhiajzjavthf.jpg',
                'hsv_value': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831165/w9287f7imjxvcqcywq7j.jpg',
            },
            'image_2': {
                'contrast': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831166/gk0k7vzev6hmlzfdgtqg.jpg',
                'texture': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831167/aeqnxuhcrkvsbo1z4zlk.jpg',
                'heat_color_map': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831167/i6uitpsvgyc0tznx4yyt.jpg',
                'hsv_hue': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831168/aabd50gebhksqcbx7tbp.jpg',
                'hsv_saturation': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831168/htrljv2sxpgh14k6iuyb.jpg',
                'hsv_value': 'https://res.cloudinary.com/dnydakj9z/image/upload/v1749831169/d0jrugitssbujfxkyp0h.jpg'
            }
        }
    )


    # mock obtención de embeddings
    mocker.patch(
        'api.infrastructure.services.external_request_service.ExternalRequestService.post_image_and_get_json',
        side_effect=[
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831170/embedding_72d0610d-4f92-4104-9070-84639ac3427e.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831177/embedding_0ab255de-ac22-4eaa-b157-6bf48ce81709.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831171/embedding_38f8b09c-f8b5-4a23-963e-38ed8e800d01.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831179/embedding_b7f760ca-63a1-42f7-9ff9-e4876beaf1cc.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831173/embedding_47631384-0d44-47ef-89f0-795722c70048.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831180/embedding_1274bede-bbf7-4231-b674-ea5fc9df985c.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831174/embedding_5adc2627-e07d-4866-bc67-fb4692e49938.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831181/embedding_b187a9c1-1939-4ba1-9edf-5f88f4c71fc1.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831175/embedding_aca894f7-78ff-49b0-9080-27114f7eec83.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831182/embedding_3f267ddc-1e2e-40f3-af8a-82858d670197.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831176/embedding_8b34fc0a-78ea-4dca-8921-5726e17be1ef.json'},
            {'embedding_url': 'https://res.cloudinary.com/dnydakj9z/raw/upload/v1749831184/embedding_d4e6c5e0-35ce-4f03-8ac9-9bb64ae240ce.json'},
        ]
    )
    mocker.patch(
        'api.infrastructure.services.external_request_service.ExternalRequestService.fetch_bytes',
        return_value=b"mock-bytes"
    )

    # mocker de recuperacion en similitud (vector a vector)
    mocker.patch(
        'api.infrastructure.services.external_request_service.ExternalRequestService.fetch_json',
        side_effect=[
            [-19.984930324570374, 5.327387492297433, -7.720515673677166, 1.6378418168549038, -4.476887099498267, -5.095000285779856, 3.206791015290649, -2.9409706418410915, -2.0881251312165356],
            [-20.972771315801136, 7.2586641405137735, -7.788072665433393, 3.2136568761945328, 1.7884830648055876, -0.9511303909793274, -1.6521414792503928, 3.659651942301106, -2.8580920984902405],
            [14.906020591383632, 10.301183745828606, -9.954850963052346, -12.20750842517017, -2.402664088452492, 2.241269084536748, 6.532992795158359, 6.45466870418461, 1.7385127779728584],
            [14.779910829531977, 8.207850012592681, -6.668632593655406, -7.798681936550701, 6.169222343597741, -3.9458151072626224, -6.801389072228012, -6.970086840189158, -2.4458480210044864],
            [-1.7463523410607829, -20.49265827371659, -5.352027238420361, -4.09665303473087, -2.821525313938101, -0.284017555539717, 2.294389750901511, -3.6629595228552154, 2.342457335077197],
            [-0.8368910146155903, -19.86001077347111, -6.1365096848197425, -2.881254725415061, 3.74961117498257, 1.8119418973710886, -3.289240216540971, 3.8495585964922268, -0.9880274575027291],
            [12.057445173173802, 2.3274946592691865, -3.651352702727681, 13.095283823262584, -8.108264714269387, 8.579402308055023, -3.4709808419608237, -1.7766161342428053, -3.3197540954430043],
            [11.028745760860527, 0.4757784989320628, -1.429640093262675, 18.175083029582176, 6.275839245389338, -5.159471144698927, 3.7597285068268684, 1.3639276698369598, 4.9898473195745225],
            [0.17211295930247417, 1.6636842943991421, 12.382342635634666, -2.4576640602127635, -6.272657367397776, -5.590420785882737, -8.530346718514666, 5.398260437311904, 3.9116140466530642],
            [1.0457562794863462, -1.7143830822594046, 16.07819002243532, -0.470759023144906, 5.375274095537487, 1.650092394252358, 3.1496850948398554, 3.1716253500582723, -7.933723455099877],
            [3.5813683015020703, -0.5169072609831871, 13.608738176511324, -3.2224603952060185, -4.256009599789475, -2.7559771486954467, 5.663719547838767, -5.461058540010346, -0.12698433050473246],
            [-14.030414899192929, 7.021916546597453, 6.632330780467447, -2.9868839454637053, 4.979578259032773, 9.499126734623418, -0.8632083823611422, -3.0860010210464695, 6.778123109983963]
        ]
    )
    mocker.patch(
        'api.infrastructure.services.similarity_service.cosine_similarity',
        return_value=[
            [0.9653631833581939],
            [0.9343139945863974],
            [0.9626167050452386],
            [0.942531117389266],
            [0.9448725352002827],
            [0.8712945860211257],
        ]
    )

    # HTTP POST: subida de imagenes
    url = reverse('upload_transform')
    img1 = SimpleUploadedFile('img1.jpg', b'image1', content_type='image/jpeg')
    img2 = SimpleUploadedFile('img2.jpg', b'image2', content_type='image/jpeg')
    response = api_client.post(
        url,
        {'image_1': img1, 'image_2': img2},
        format='multipart',
        HTTP_X_SECRET_KEY='topsecret'
    )
    print("RESPONSE:", response.status_code)
    print("BODY:", response.content.decode()) 
    
    assert response.status_code == 201
    session_id = response.json()['comparison_id']

    # Asegura la creacion de la sesión y datos fueron guardados
    session = ImageComparisonSession.objects.get(id=session_id)
    embeddings = TransformedImageEmbedding.objects.filter(comparison=session)
    similarity = SimilarityMetricResult.objects.filter(comparison=session)

    assert embeddings.count() == 14
    assert similarity.count() == 6
    transform_types = ['contrast', 'texture', 'heat_color_map', 'hsv_hue', 'hsv_saturation', 'hsv_value']
    for transform_type in transform_types:
        sim = similarity.get(transform_type=transform_type)
        assert 0 < sim.similarity_score <= 1.0

    # HTTP GET: consulta de resultados
    result_url = reverse('get_similarity_result', args=[session_id])
    res = api_client.get(result_url)
    assert res.status_code == 200
    json_res = res.json()
    assert json_res['comparison_id'] == session_id
    assert 'contrast' in json_res['similitud']