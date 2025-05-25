from django import forms
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'link', 'difficulty', 'platform', 'status']


class ExcelUploadForm(forms.Form):
    file = forms.FileField(label='Upload Excel file')
