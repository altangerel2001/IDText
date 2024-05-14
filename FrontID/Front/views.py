# Project 2: myapp/views.py
import base64
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def upload_view(request):
    return render(request, 'upload.html')

@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            base64_image = base64.b64encode(image.read()).decode('utf-8')
            
            response = requests.post(
                'http://127.0.0.1:8000/image/',
                json={'image': base64_image},
                headers={'Content-Type': 'application/json'}
            )
            data = response.json()
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Please provide a POST request.'}, status=400)
