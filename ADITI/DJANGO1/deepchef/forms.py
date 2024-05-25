from django import forms

class Image_Upload(forms.Form):
    image=forms.ImageField()