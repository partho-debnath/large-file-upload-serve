from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("file-upload/", views.FileUploadView.as_view(), name="file-upload"),
    path(
        "server-file/<int:pk>/",
        views.ServeFileAPiView.as_view(),
        name="file-server",
    ),
]
