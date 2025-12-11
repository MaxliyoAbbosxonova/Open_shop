from django.core.management.base import BaseCommand
from django.conf import settings
import os

from products.utils import convert_to_webp


class Command(BaseCommand):
    help = "Convert all existing images in MEDIA_ROOT to WebP"

    def handle(self, *args, **kwargs):
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                if file.lower().endswith((".jpg", ".jpeg", ".png")):
                    full_path = os.path.join(root, file)
                    convert_to_webp(full_path)
                    self.stdout.write(f"Converted {file}")