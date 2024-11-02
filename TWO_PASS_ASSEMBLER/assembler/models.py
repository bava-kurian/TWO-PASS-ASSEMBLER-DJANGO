# assembler/models.py
from django.db import models
from django.utils import timezone

class AssemblerFile(models.Model):
    input_file = models.FileField(upload_to='assembler_inputs/', null=True, blank=True)
    optab_file = models.FileField(upload_to='assembler_optabs/', null=True, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.input_file.name} (Uploaded on {self.upload_date})"
