from django import forms

class ContactForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Fist name'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-Mail'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))