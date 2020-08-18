from urllib import request
from PIL import Image

from django.db import models
from django.core.files import File


class ResizableImage(models.Model):
    """Модель содержит одно поле, собственно, картинку"""

    name = models.CharField(max_length=255)
    file = models.ImageField(upload_to="images/")

    @staticmethod
    def retrieve_from_url(image_url: str) -> "ResizableImage":
        """Создаем новую картинку по URLу"""

        new_image = ResizableImage(name=image_url.split("/")[-1])
        image_data = request.urlretrieve(image_url)

        new_image.file.save(
            new_image.name,
            File(open(image_data[0], "rb"))
        )

        return new_image


class ResizableImagePretender:
    """
    Притворяется классом ResizableImage, чтобы выводить
    измененные изображения
    """

    def __init__(self, img: Image, img_id: int, base64_image: str) -> None:
        self.file = img
        self.image_id = img_id

        self.file.url = "data:image/jpeg;base64," + base64_image

    @property
    def id(self) -> int:
        return self.image_id
