from django.contrib import admin
from django.urls import path
from trans_PDF.views import *


urlpatterns = [
    path('trans/', file_upload_view),
    # path('', home, name='home'),
    # path('generate_docx/', generate_docx, name='generate_docx'),
]