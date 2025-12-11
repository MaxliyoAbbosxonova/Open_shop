from root import settings
from django import template
from PIL import Image
import os
import logging
register = template.Library()
logger = logging.getLogger(__name__)

def convert_to_webp(image_path):
    webp_path = image_path.rsplit(".", 1)[0] + ".webp"

    if os.path.exists(webp_path):
        return webp_path

    try:
        img = Image.open(image_path).convert("RGB")
        img.save(webp_path, "WEBP", quality=85)
        logger.info(f"Converted: {image_path} → {webp_path}")
        return webp_path

    except Exception as e:
        logger.error(f"WebP conversion error for {image_path}: {e}")
        return None

@register.simple_tag(takes_context=True)
def webp(context, img_url):
    original_url = settings.STATIC_URL + img_url
    original_path = os.path.join(settings.STATIC_ROOT, img_url)

    webp_url = settings.STATIC_URL + img_url.rsplit(".", 1)[0] + ".webp"
    webp_path = os.path.join(settings.STATIC_ROOT, img_url.rsplit(".", 1)[0] + ".webp")

    req = context.get("request")

    if req and "image/webp" in req.META.get("HTTP_ACCEPT", ""):
        if not os.path.exists(webp_path):
            convert_to_webp(original_path)

        if os.path.exists(webp_path):
            return webp_url

    return original_url

