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
            # Get the uploaded image
            image = request.FILES['image']
            
            # Convert image to base64
            base64_image = base64.b64encode(image.read()).decode('utf-8')
            
            # Send base64 image to Project 1
            response = requests.post(
                'http://127.0.0.1:8000/image/',
                json={'image': base64_image},
                headers={'Content-Type': 'application/json'}
            )
            
            # Get the response from Project 1
            if response.status_code == 200:
                data = response.json()
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    else:
        return JsonResponse({'error': 'Please provide a POST request.'}, status=400)
