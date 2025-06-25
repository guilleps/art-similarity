"""
Validacion de integridad de los modelos de dominio
Modelos testeados: ImageComparisonSession, SimilarityMetricResult, TransformedImageEmbedding
"""

import pytest
from django.core.exceptions import ValidationError
from django.db.models import DateTimeField
from api.domain.models.comparison_session import ImageComparisonSession
from api.domain.models.similarity_result import SimilarityMetricResult, TransformType as SimilarityTransformType
from api.domain.models.transformed_image_embedding import TransformedImageEmbedding, TransformType as EmbeddingTransformType

@pytest.mark.django_db
# Verificación de que el modelo ImageComparisonSession se crea correctamente (contenga UUID y campo created_at)
def test_image_comparison_session_str():
    session = ImageComparisonSession.objects.create()

    assert str(session) == f"ImageComparisonSession {session.id}"
    
    field = session._meta.get_field('created_at')
    assert isinstance(field, DateTimeField)
    assert field.auto_now_add is True

@pytest.mark.django_db
# Garantizar que se cree un unico resultado de métrica de similitud por sesión y tipo de transformación
def test_similarity_unique_together():
    session = ImageComparisonSession.objects.create()
    SimilarityMetricResult.objects.create(
        comparison=session,
        transform_type=SimilarityTransformType.CONTRAST,
        similarity_score=0.5,
        file_1="f1",
        file_2="f2"
    )
    with pytest.raises(Exception):
        SimilarityMetricResult.objects.create(
            comparison=session,
            transform_type=SimilarityTransformType.CONTRAST,
            similarity_score=0.6,
            file_1="f3",
            file_2="f4"
        )

@pytest.mark.django_db
# Asegurar que al no indicar un tipo de transformación, se asigne el tipo por defecto
def test_transformed_image_default_transform():
    session = ImageComparisonSession.objects.create()
    emb = TransformedImageEmbedding.objects.create(
        comparison=session,
        image_index=1,
        image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgBBKSpsFEwi6RMAvfvKEh1J_lCgVTsI-7yg&s",
        embedding_url="https://res.cloudinary.com/dnydakj9z/raw/upload/v1749830609/embedding_4139e2bf-7b17-4c65-a1b1-e3dbd54ececc.json",
        filename="gatito.jpg"
    )
    assert emb.transform_type == EmbeddingTransformType.ORIGINAL
    assert str(emb).startswith(f"{session.id} - Img1 - {EmbeddingTransformType.ORIGINAL}")

@pytest.mark.django_db
# Lanzar un error al querer asignar un tipo de transformación inválido
def test_similarity_transform_type_invalid():
    session = ImageComparisonSession.objects.create()
    with pytest.raises(ValidationError):
        sim = SimilarityMetricResult(
            comparison=session,
            transform_type="invalid_type",
            similarity_score=0.5,
            file_1="f1",
            file_2="f2"
        )
        sim.full_clean()

@pytest.mark.django_db
# Verificar que el puntaje de similitud no pueda ser negativo
def test_similarity_score_negative():
    session = ImageComparisonSession.objects.create()
    with pytest.raises(ValidationError):
        sim = SimilarityMetricResult(
            comparison=session,
            transform_type=SimilarityTransformType.CONTRAST,
            similarity_score=-0.1,
            file_1="f1",
            file_2="f2"
        )
        sim.full_clean()
