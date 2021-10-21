from django import forms
from .models import Chirp

MAX_CHIRP_LENGTH = 280

class ChirpForm(forms.ModelForm):
    class Meta:
        model = Chirp
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_CHIRP_LENGTH:
            raise forms.ValidationError("This Chirp is too long")
        return content
