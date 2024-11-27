from django.urls import path

from . import views
from .views import PDFGeneratorView

urlpatterns = [
    path("", PDFGeneratorView.as_view(), name="get_view"),
]
