from django.shortcuts import render
from .models import Contact
from .form import ContactForm
from django.http import HttpRequest
from django.shortcuts import render, redirect

def contactView(request):
    form = ContactForm(request.POST)
    if request.method == 'POST' and form.is_valid():
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        Contact.objects.create(firstname=firstname, lastname=lastname, email=email, subject=subject, message=message)
        return redirect('contact')
    context = {'form': form}
    return render(request, 'contacts/contact.html', context)