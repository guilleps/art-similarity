import pytest
from api.infrastructure.services.image_loader_service import ImageLoaderService

def test_load_images_success(tmp_path):
    # Prepara directorio con dos imágenes
    img1 = tmp_path / "b.jpg"
    img2 = tmp_path / "a.PNG"
    img1.write_text("dummy")
    img2.write_text("dummy")

    svc = ImageLoaderService()
    images = svc.load_images(str(tmp_path))

    assert images == ["a.PNG", "b.jpg"]

def test_load_images_more_than_two(tmp_path):
    (tmp_path / "1.png").write_text("x")
    (tmp_path / "2.jpg").write_text("x")
    (tmp_path / "3.jpeg").write_text("x")

    svc = ImageLoaderService()
    with pytest.raises(ValueError) as exc:
        svc.load_images(str(tmp_path))
    assert "exactamente dos imágenes" in str(exc.value)

def test_load_images_less_than_two(tmp_path):
    (tmp_path / "only.jpg").write_text("x")

    svc = ImageLoaderService()
    with pytest.raises(ValueError):
        svc.load_images(str(tmp_path))

def test_load_images_ignore_non_image_files(tmp_path):
    (tmp_path / "1.png").write_text("x")
    (tmp_path / "note.txt").write_text("x")
    (tmp_path / "2.JPG").write_text("x")

    svc = ImageLoaderService()
    images = svc.load_images(str(tmp_path))

    assert images == sorted(["1.png", "2.JPG"])
