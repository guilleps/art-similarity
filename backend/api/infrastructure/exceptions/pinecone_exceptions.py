class PineconeConnectionError(Exception):
    def __init__(self, message="No se pudo conectar con Pinecone"):
        self.message = message
        super().__init__(self.message)


class PineconeQueryError(Exception):
    def __init__(self, message="Fallo al consultar imágenes similares en Pinecone"):
        self.message = message
        super().__init__(self.message)


class PineconeUpsertError(Exception):
    def __init__(self, message="Fallo al guardar el embedding en Pinecone"):
        self.message = message
        super().__init__(self.message)
