# Create your views here.
from django.shortcuts import render
from .forms import FileUploadForm
from .models import UploadedFile
from handler.handler import DOCX
from django.core.files.base import ContentFile

def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadedFile(pdf_file=form.cleaned_data['file'])
            fp.save()
            name_docx = fp.pdf_file.name

            # fp.docx_file =
            fp.save()
            # filw = FileResponse(open(request.FILES['file'].name, "rb"))
            # return filw
    else:
        form = FileUploadForm()
    return render(request, 'trans_PDF/upload.html', {'form': form})

