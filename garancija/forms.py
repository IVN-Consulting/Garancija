from django import forms
from garancija.models import Warranty

class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ['product_name', 'file']
