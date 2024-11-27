from django.http import HttpResponse

from base.views import AbstractAPIView


class PDFGeneratorView(AbstractAPIView):

    def get(self, request):
        return HttpResponse("Hello, world. You're at the pdf_generator index.")
