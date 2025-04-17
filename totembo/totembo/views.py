from django.shortcuts import render
from django.views.generic import ListView

# class Index(ListView):
#     template_name = "totembo/index.html"

def index(request):
    return render(request,"totembo/index.html")