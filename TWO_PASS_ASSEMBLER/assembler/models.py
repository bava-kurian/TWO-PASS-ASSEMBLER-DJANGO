# models.py
from django.db import models

class UploadedFile(models.Model):
    FILE_TYPES = (
        ('input', 'Input File'),
        ('optab', 'Optab File'),
    )

    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)

    def __str__(self):
        return f"{self.file_type}: {self.file.name}"
