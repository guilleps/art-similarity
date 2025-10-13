class EmbeddingModelError(Exception):
    def __init__(self, message="Error al procesar la imagen"):
        self.message = message
        super().__init__(self.message)
