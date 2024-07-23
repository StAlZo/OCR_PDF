# Create your views here.
import zipfile
from io import BytesIO

from django.http import FileResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import FileUploadForm
from .models import UploadedFile
from handler.handler import DOCX, PdfToDocx
from django.core.files.base import ContentFile

@csrf_exempt
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadedFile(pdf_file=form.cleaned_data['file'])
            fp.save()
            name_docx = fp.pdf_file.name.replace('/', '')
            det = PdfToDocx(name_docx)
            docx_name = det.init_recognition(f'media/{fp.pdf_file.name}')
            fp.docx_file = f'media/docx_files/{docx_name[0]}.docx'
            fp.save()
            fp.summary = f'media/summary/{docx_name[1]}.docx'
            fp.save()
            buffer = BytesIO()
            with zipfile.ZipFile(buffer, 'w') as zipf:
                # Добавляем файлы в архив
                zipf.write(fp.docx_file)
                zipf.write(fp.summary)

            # Подготавливаем буфер для отправки
            buffer.seek(0)

            # Создаем FileResponse и отправляем архив
            response = FileResponse(buffer, as_attachment=True, filename='example.zip')
            return response
    else:
        form = FileUploadForm()
    return render(request, 'trans_PDF/upload.html', {'form': form})


