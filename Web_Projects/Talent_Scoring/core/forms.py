from django import forms
from core import models as core_models


class ContactForm(forms.ModelForm):
    class Meta:
        model = core_models.Contact
        fields = '__all__'