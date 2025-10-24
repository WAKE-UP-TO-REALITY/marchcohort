import os
import json
import logging
import time
import urllib.parse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from huggingface_hub import InferenceClient
from PIL import Image

# Load Hugging Face API key
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
print(f"Hugging Face API Key: {HUGGINGFACE_API_KEY}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize HF InferenceClient globally
hf_client = InferenceClient(api_key=HUGGINGFACE_API_KEY)

# ----------------- Image Generation -----------------
def generate_image(hotel_name, occasion, additional_prompt=""):
    prompt = f"A stunning, high-quality image representing {occasion} at {hotel_name} hotel, {additional_prompt}".strip()
    try:
        # Generate image via Hugging Face
        image = hf_client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )

        # Save image locally
        posts_dir = os.path.join(settings.MEDIA_ROOT, 'posts')
        os.makedirs(posts_dir, exist_ok=True)

        clean_hotel = ''.join(e for e in hotel_name if e.isalnum())
        clean_occasion = ''.join(e for e in occasion if e.isalnum())
        timestamp = int(time.time())
        image_filename = f"post_{clean_hotel}_{clean_occasion}_{timestamp}.png"
        image_path = os.path.join(posts_dir, image_filename)
        image.save(image_path)

        image_url = os.path.join(settings.MEDIA_URL, 'posts', image_filename)
        return image_url.replace('\\', '/')
    except Exception as e:
        logger.error(f"Error generating image with SDXL API: {e}")
        return None

# ----------------- Views -----------------
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

            logger.info(f"Generating image for Hotel: {hotel_name}, Occasion: {occasion}")

            image_url = generate_image(hotel_name, occasion)
            if not image_url:
                return JsonResponse({"error": "Failed to generate image"}, status=500)

            return JsonResponse({"imageURL": image_url})
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

            image_url = generate_image(hotel_name, occasion, additional_prompt)

            if not image_url:
                return JsonResponse({"error": "Failed to regenerate image"}, status=500)

            return JsonResponse({"imageURL": image_url})
        except Exception as e:
            logger.error(f"Error regenerating image: {e}")
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
            return redirect(f"https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(image_url)}&quote={urllib.parse.quote(caption)}")
        elif platform == 'twitter':
            return redirect(f"https://twitter.com/intent/tweet?text={urllib.parse.quote(caption)}&url={urllib.parse.quote(image_url)}")
        elif platform == 'linkedin':
            return redirect(f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(image_url)}&title={urllib.parse.quote('Check out this post!')}&summary={urllib.parse.quote(caption)}")

        return JsonResponse({"error": "Invalid platform"}, status=400)
