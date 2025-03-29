
import os
import json
import requests
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from django.conf import settings


load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def home(request):
    return render(request, 'posts/index.html')



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_text(hotel_name, occasion):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    prompt = f"Generate a social media post for a hotel. Hotel: {hotel_name}. Occasion: {occasion}. Example: '{hotel_name} wishes you a wonderful {occasion}!'"  

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()  

        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "Couldn't generate text.")
        return "Unexpected API response format."
    except requests.exceptions.RequestException as e:
        logger.error(f"Text generation API error: {e}")
        return f"API Error: {str(e)}"

def generate_image(hotel_name, occasion):
    prompt = f"A stunning, high-quality image representing {occasion} at {hotel_name} hotel, vibrant and artistic."
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        if response.status_code == 200:
            image_data = response.content
            image_filename = "generated_image.png"
            image_path = os.path.join(settings.MEDIA_ROOT, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_data) 

            return settings.MEDIA_URL + image_filename  
        else:
            logger.error(f"Image generation failed: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Image generation API error: {e}")
        return None


def home(request):
    return render(request, 'posts/index.html')

@method_decorator(csrf_exempt, name="dispatch")  
class GeneratePostAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            hotel_name = data.get("hotel_name", "").strip()
            occasion = data.get("occasion", "").strip()

            if not hotel_name or not occasion:
                return JsonResponse({"error": "Hotel name and occasion are required!"}, status=400)

            logger.info(f"Generating post for Hotel: {hotel_name}, Occasion: {occasion}")

            caption = generate_text(hotel_name, occasion)
            image_url = generate_image(hotel_name, occasion)

            if "API Error" in caption:
                return JsonResponse({"error": caption}, status=500)

            return JsonResponse({"caption": caption, "imageURL": image_url})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.error(f"Internal Server Error: {e}")
            return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)
