import cv2
import pytesseract
import base64
import json
import io
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def extract_text_and_info_from_image(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            base64_encoded_image_data = json_data.get('image')
            
            if base64_encoded_image_data:
                decoded_image_data = base64.b64decode(base64_encoded_image_data)
                
                image = Image.open(io.BytesIO(decoded_image_data))
                
                extracted_text = pytesseract.image_to_string(image,lang='mon+eng')
                
                lines = extracted_text.split("\n")
                
                surname = ""
                given_name = ""
                
                surname_found = False
                given_name_found = False
                
                for i, line in enumerate(lines):
                    if "Овог" in line or "Family name" in line:
                        surname = lines[i + 1].strip()
                        surname_found = True
                    elif "Эцэг/эх/-ийн нэр" in line or "Surname" in line:
                        surname = lines[i + 1].strip()
                        surname_found = True
                    elif "Hэp" in line or "Given" in line:
                        given_name = lines[i + 1].strip()
                        given_name_found = True
                    if surname_found and given_name_found:
                        break
                
                return JsonResponse({
                    'extracted_text': extracted_text,
                    'surname': surname,
                    'given_name': given_name
                })
            else:
                return JsonResponse({'error': 'Base64 encoded image data not provided in JSON request.'}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format in request body.'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Please provide a POST request.'}, status=400)
