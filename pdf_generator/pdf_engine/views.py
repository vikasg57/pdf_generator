from rest_framework import status

from base.response import APIResponse
from base.views import AbstractAPIView
from pdf_engine.handlers.resume_template_handler import ResumeTemplateHandler


class PDFGeneratorView(AbstractAPIView):

    def post(self, request, *args, **kwargs):
        template_id = kwargs.get('template_id')
        data = ResumeTemplateHandler().create_resume(template_id)
        return APIResponse(data=data, status=status.HTTP_200_OK)
