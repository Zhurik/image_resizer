import base64
from io import BytesIO
from PIL import Image

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import ResizableImage, ResizableImagePretender


def index(request) -> HttpResponse:
    """Главная страница"""
    images = ResizableImage.objects.all()

    context = {
        "images": images
    }

    return render(request, "imager/index.html", context)


def add_new(request) -> HttpResponse:
    """Страничка добавления нового изображения"""

    return render(request, "imager/adder.html")


def upload(request) -> HttpResponse:
    """Логика обработки загружаемого изображения"""

    new_image = None

    if request.POST["url"] and request.FILES:
        return render(request, "imager/adder.html", {"error_message": "Укажите что-то одно!"})

    elif request.POST["url"]:
        new_image = ResizableImage.retrieve_from_url(request.POST["url"])

    elif request.FILES:
        new_image = ResizableImage(name=str(request.FILES["file"]), file=request.FILES["file"])

    else:
        return render(
            request,
            "imager/adder.html",
            {
                "error_message": "Не указано ни одной картинки для загрузки!"
            }
        )

    new_image.save()

    return render(request, "imager/image.html", {"image": new_image})


def resize(request) -> HttpResponse:
    """Страница изменения размеров изображения"""

    img = get_object_or_404(ResizableImage, pk=request.POST["image_id"])
    error_message = None

    if not request.POST["width"] and not request.POST["height"]:
        error_message = "Укажите хотя бы одно значение!"

    else:
        # try:
        new_width = int(request.POST["width"]) if request.POST["width"] else img.file.width
        new_height = int(request.POST["height"]) if request.POST["height"] else img.file.height

        new_image = Image.open(img.file.path)

        # Сжимаем картинку до нужных размеров
        new_image.thumbnail((new_width, new_height))

        buffered = BytesIO()

        new_image.save(buffered, format="JPEG")

        base64_image = base64.b64encode(buffered.getvalue())

        img = ResizableImagePretender(
            new_image,
            request.POST["image_id"],
            base64_image.decode("ascii")
        )

        # except ValueError:
        #     error_message = "Допустимы только целочисленные значения!"

        # except:
        #     error_message = "Ошибка на сервере! Приносим свои извинения!"

    return render(
        request,
        "imager/image.html",
        {
            "image": img,
            "error_message": error_message
        }
    )


def image(request, image_id) -> HttpResponse:
    """Отображаем картинку по id"""

    img = get_object_or_404(ResizableImage, pk=image_id)

    return render(request, "imager/image.html", {"image": img})
