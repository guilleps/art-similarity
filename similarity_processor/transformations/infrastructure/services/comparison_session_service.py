from transformations.domain.models import ImageComparisonSession, TransformedImageEmbedding

class ComparisonSessionService:
    def create_session(self, image_urls: list[str]) -> ImageComparisonSession:
        session = ImageComparisonSession.objects.create()
        for i, url in enumerate(image_urls, start=1):
            TransformedImageEmbedding.objects.create(
                comparison=session,
                image_index=i,
                transform_type="original_image",
                filename=url,
                embedding_url=url
            )
        return session
        
            