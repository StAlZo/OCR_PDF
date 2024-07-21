# Create your views here.
from django.http import FileResponse
from django.shortcuts import render
from .forms import FileUploadForm
from .models import UploadedFile
from handler.handler import DOCX, PdfToDocx
from django.core.files.base import ContentFile

def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadedFile(pdf_file=form.cleaned_data['file'])
            fp.save()
            name_docx = fp.pdf_file.name.replace('/', '')
            det = PdfToDocx(name_docx)
            docx_name = det.init_recognition(f'media/{fp.pdf_file.name}')
            fp.docx_file = f'media/docx_files/ + {docx_name}.docx'
            fp.save()
            filw = FileResponse(open(f'media/docx_files/{docx_name}.docx', "rb"))
            return filw
    else:
        form = FileUploadForm()
    return render(request, 'trans_PDF/upload.html', {'form': form})

