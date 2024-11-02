# assembler/forms.py
from django import forms
from .models import AssemblerFile

class AssemblerFileUploadForm(forms.ModelForm):
    class Meta:
        model = AssemblerFile
        fields = ['input_file', 'optab_file']
