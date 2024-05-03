from django.shortcuts import render

# Create your views here.
import base64

with open('C:\\Users\\monst\\Downloads\\list daalgavar 1.PNG' ,'rb') as image_file:


    base64_encoded_image = base64.b64encode(image_file.read())

print(base64_encoded_image.decode('utf-8'))


from django.http import JsonResponse
import pytesseract
from PIL import Image
import io
from django.views.decorators.csrf import csrf_exempt
import json
import pytesseract



pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\monst\\AppData\\Local\\Programs\\Python\\Python311\\tesseract'



@csrf_exempt
def extract_text_from_image(request):
    if request.method == 'POST':
        try:
            # Extract the Base64 encoded image data from the JSON request body
            json_data = json.loads(request.body.decode('utf-8'))
            base64_encoded_image_data = json_data.get('image')
            
            if base64_encoded_image_data:
                # Decode the Base64 encoded image data
                decoded_image_data = base64.b64decode(base64_encoded_image_data)
                
                # Convert the binary image data to a PIL image
                image = Image.open(io.BytesIO(decoded_image_data))
                
                # Process the image with Tesseract to extract text
                extracted_text = pytesseract.image_to_string(image)
                
                return JsonResponse({'extracted_text': extracted_text})
            else:
                return JsonResponse({'error': 'Base64 encoded image data not provided in JSON request.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Please provide a POST request.'}, status=400)
