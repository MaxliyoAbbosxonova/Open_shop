import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from PIL import Image
from products.models import (
    Product,  # Ilovangiz nomini to'g'rilang agar boshqacha bo'lsa
)


class Command(BaseCommand):
    help = _("Mavjud mahsulot rasmlarini WebP formatiga o\'tkazadi va DBda yangilaydi.")

    def handle(self, *args, **options):
        # Media ildiz katalogi
        media_root = Path(settings.MEDIA_ROOT)

        # O'zgartirilgan rasmlar soni
        converted_count = 0

        self.stdout.write(self.style.NOTICE("WebP formatiga o'tkazish boshlandi..."))

        # Ma'lumotlar bazasida atomik tranzaksiyani ta'minlaymiz
        with transaction.atomic():
            # Barcha Product ob'ektlarini olamiz
            products = Product.objects.all()

            for product in products:
                # Agar image maydoni bo'sh bo'lmasa
                if product.image:
                    original_file_path_rel = product.image.name
                    # Faylning to'liq absolyut yo'li
                    original_file_path_abs = media_root / original_file_path_rel

                    if original_file_path_abs.is_file():
                        # Yangi WebP fayl nomi (kengaytmasi .webp)
                        new_file_path_rel = f"{original_file_path_rel.rsplit('.', 1)[0]}.webp"
                        new_file_path_abs = media_root / new_file_path_rel

                        try:
                            # 1. Rasmni WebP ga konvertatsiya qilish
                            with Image.open(original_file_path_abs) as img:
                                # RGBA rejimini (shaffoflikni qo'llab-quvvatlaydigan) RGB ga aylantirish
                                # WebP sifatini oshirish uchun (agar shaffoflik muhim bo'lmasa)
                                if img.mode == 'RGBA':
                                    img = img.convert('RGB')

                                # Ota-onalar katalogini yaratish
                                new_file_path_abs.parent.mkdir(parents=True, exist_ok=True)

                                # WebP formatida saqlash (sifat 80 bilan)
                                img.save(new_file_path_abs, 'webp', quality=80)

                            self.stdout.write(self.style.SUCCESS(
                                f"{original_file_path_rel} -> {new_file_path_rel} ga o'tkazildi."
                            ))

                            # 2. Ma'lumotlar bazasini yangilash
                            product.image.name = new_file_path_rel
                            product.save(update_fields=['image'])

                            # 3. Eski faylni o'chirish (ixtiyoriy, tavsiya etiladi)
                            os.remove(original_file_path_abs)
                            self.stdout.write(self.style.WARNING(f'Eski fayl o\'chirildi: {original_file_path_abs}'))

                            converted_count += 1

                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Xatolik yuz berdi {original_file_path_rel}: {e}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Fayl topilmadi: {original_file_path_abs}'))

        self.stdout.write(
            self.style.SUCCESS(f"WebP formatiga o'tkazish yakunlandi. {converted_count} ta rasm yangilandi."))
