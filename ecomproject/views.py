from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

def index(request):
    context = {"title": "Home"}
    return render(request,"home.html",context)