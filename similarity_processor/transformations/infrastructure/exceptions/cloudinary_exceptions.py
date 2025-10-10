class CloudinaryUploadError(Exception):
    def __init__(self, message="No se pudo subir la imagen a Cloudinary"):
        self.message = message
        super().__init__(self)