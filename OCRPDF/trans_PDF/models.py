from django.db import models

# Create your models here.


class KeyWord(models.Model):
    file_path = models.CharField(max_length=200)


class UploadedFile(models.Model):
    pdf_file = models.FileField(upload_to='pdf_files/')
    docx_file = models.FilePathField(blank=True, null=True)
    summary = models.FilePathField(blank=True, null=True)