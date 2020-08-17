from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_image/", views.add_new, name="add_new"),
    path("upload/", views.upload, name="upload"),
    path("resize", views.resize, name="resize"),
    path("images/<int:image_id>/", views.image, name="image"),
]
