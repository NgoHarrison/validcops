from django.forms import TextInput
from django import forms

class ShoeForm(forms.Form):
    shoe_name= forms.CharField(label='Shoe name',max_length=100, widget=forms.TextInput(attrs={'placeholder':'What shoe are you looking for?'}))
    shoe_size=forms.DecimalField(label='Shoe size',widget=forms.TextInput(attrs={'placeholder':'Size?'}))

    def clean_shoe_size(self):
        data = self.cleaned_data['shoe_size']

        return data