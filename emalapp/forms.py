from django import forms

class register(forms.Form):
    name=forms.CharField(max_length=20)
    phone=forms.IntegerField()
    image=forms.FileField()

class contactusForm(forms.Form):
    Name=forms.CharField(max_length=30)
    Email= forms.EmailField()
    Message=forms.CharField(max_length=500,
                            widget=forms.Textarea(attrs={'rows':3,'cols':30}))

