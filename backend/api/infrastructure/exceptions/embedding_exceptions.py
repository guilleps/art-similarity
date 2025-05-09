class EmbeddingModelError(Exception):
    def __init__(self, message="Error al generar el embedding con EfficientNet"):
        self.message = message
        super().__init__(self.message)
