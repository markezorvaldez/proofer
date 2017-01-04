from django import forms

from .models import Proof

class ProofForm(forms.ModelForm):

    class Meta:
        model = Proof
        fields = ('premise', 'proof',)
        widgets = {
        'premise': forms.Textarea(attrs={'rows':1, 'cols':15}),
        }