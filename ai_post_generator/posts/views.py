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
import time 
import urllib.parse
from django.shortcuts import redirect
import urllib.parse


load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
print(f"Hugging Face API Key: {HUGGINGFACE_API_KEY}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_text(hotel_name, occasion):
    API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    prompt = f"Generate a social media post for a hotel. Hotel: {hotel_name}. Occasion: {occasion}. Example:'{hotel_name} wishes you a wonderful {occasion}!'"
    
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
    return generate_image_with_prompt(prompt, hotel_name, occasion)

def generate_image_with_prompt(prompt, hotel_name, occasion):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
            posts_dir = os.path.join(settings.MEDIA_ROOT, 'posts')
            os.makedirs(posts_dir, exist_ok=True)
            
            clean_hotel = ''.join(e for e in hotel_name if e.isalnum())
            clean_occasion = ''.join(e for e in occasion if e.isalnum())
            timestamp = int(time.time())
            image_filename = f"post_{clean_hotel}_{clean_occasion}_{timestamp}.png"
            image_path = os.path.join(posts_dir, image_filename)

            with open(image_path, "wb") as f:
                f.write(response.content)

            image_url = os.path.join(settings.MEDIA_URL, 'posts', image_filename)
            return image_url.replace('\\', '/')

        logger.error(f"Unexpected API response: {response.status_code} - {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Image generation API error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in generate_image: {str(e)}")
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

@method_decorator(csrf_exempt, name="dispatch")
class RegenerateImageView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            hotel_name = data.get("hotel_name", "").strip()
            occasion = data.get("occasion", "").strip()
            additional_prompt = data.get("additional_prompt", "").strip()
            
            if not hotel_name or not occasion:
                return JsonResponse({"error": "Hotel name and occasion are required!"}, status=400)
            
            full_prompt = f"A stunning, high-quality image representing {occasion} at {hotel_name} hotel, {additional_prompt}"
            
            image_url = generate_image_with_prompt(full_prompt, hotel_name, occasion)
            
            if not image_url:
                return JsonResponse({"error": "Failed to regenerate image"}, status=500)
                
            return JsonResponse({"imageURL": image_url})
            
        except Exception as e:
            logger.error(f"Error regenerating image: {str(e)}")
            return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)
@method_decorator(csrf_exempt, name="dispatch")
class SocialMediaShareView(View):
    def get(self, request, *args, **kwargs):
        platform = kwargs.get('platform')
        caption = request.GET.get('caption', '')
        image_url = request.GET.get('image_url', '')
        
        if not caption and not image_url:
            return JsonResponse({"error": "Caption or image URL required"}, status=400)
        
        if platform == 'instagram':
            if image_url:
                return redirect(f"https://www.instagram.com/create/story?image_url={urllib.parse.quote(image_url)}")
            return JsonResponse({"error": "Instagram requires an image"}, status=400)
        
        elif platform == 'facebook':
            return redirect(
                f"https://www.facebook.com/sharer/sharer.php?"
                f"u={urllib.parse.quote(image_url)}&"
                f"quote={urllib.parse.quote(caption)}"
            )
        
        elif platform == 'twitter':
            return redirect(
                f"https://twitter.com/intent/tweet?"
                f"text={urllib.parse.quote(caption)}&"
                f"url={urllib.parse.quote(image_url)}"
            )
        
        elif platform == 'linkedin':
            return redirect(
                f"https://www.linkedin.com/sharing/share-offsite/?"
                f"url={urllib.parse.quote(image_url)}&"
                f"title={urllib.parse.quote('Check out this post!')}&"
                f"summary={urllib.parse.quote(caption)}"
            )
        
        return JsonResponse({"error": "Invalid platform"}, status=400)