from django.shortcuts import render


# Create your views here.
# views.py
from django.shortcuts import render

def upload_image(request):
    return render(request, 'upload.html')
