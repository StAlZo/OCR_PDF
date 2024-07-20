from django.http import HttpResponse, FileResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import FileUploadForm
from django.core.files.storage import default_storage


def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Обработка загруженных файлов
            with default_storage.open(request.FILES['file'].name, 'wb+') as destination:
                for f in request.FILES['file'].chunks():
                    destination.write(f)
            ploaded_file = request.FILES['file']
            with default_storage.open(request.FILES['file'].name, 'wb+') as destination:
                filw = FileResponse(destination)
            # Здесь вы можете добавить логику для обработки файла перед отправкой обратно клиенту
            # return HttpResponse(f"Файл {request.FILES['file'].name} успешно загружен и обработан")
            return filw
    else:
        form = FileUploadForm()
    return render(request, 'trans_PDF/upload.html', {'form': form})

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.core.files.storage import FileSystemStorage
# import docx
# import pytesseract
# from PIL import Image
# from io import BytesIO
#
# def home(request):
#     return render(request, 'trans_PDF/home.html')
#
# def handle_uploaded_file(f):
#     with open('uploaded_file', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
#
# def extract_text_from_image(image):
#     img = Image.open(image)
#     text = pytesseract.image_to_string(img)
#     return text
#
# def generate_docx(request):
#     if request.method == 'POST' and request.FILES['document']:
#         uploaded_file = request.FILES['document']
#         handle_uploaded_file(uploaded_file)
#
#         extracted_text = extract_text_from_image(uploaded_file)
#
#         doc = docx.Document()
#         doc.add_paragraph(extracted_text)
#
#         f = BytesIO()
#         doc.save(f)
#         length = f.tell()
#         f.seek(0)
#
#         response = HttpResponse(
#             f.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
#         )
#         response['Content-Disposition'] = 'attachment; filename=extracted_text.docx'
#         return response
#     else:
#         return HttpResponse('Invalid request')