# myapp/management/commands/add_data.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Category, Product


class Command(BaseCommand):
    help = "Add random categories and/or products"

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories', type=int, default=0,
            help='Number of categories to create'
        )
        parser.add_argument(
            '--products', type=int, default=0,
            help='Number of products to create'
        )
        parser.add_argument(
            '--all', action='store_true',
            help='Create both categories and products (defaults numbers apply)'
        )

    def _generate_categories(self, number=5):
        for _ in range(number):
            name = self.faker.text(max_nb_chars=50)
            obj = Category.objects.create(name=name)
            self.stdout.write(self.style.SUCCESS(f"Created category: {obj.name}"))

    def _generate_products(self, number=5):
        for _ in range(number):
            category = Category.objects.order_by('?').first()
            if not category:
                self.stdout.write(self.style.WARNING("No categories found, skipping product creation."))
                return
            obj = Product.objects.create(
                name=self.faker.text(max_nb_chars=50),
                category=category,
                price=random.randint(10, 100) * 1000,
                image=self.faker.image_url(),
                description=self.faker.text(max_nb_chars=255),
                slug=self.faker.slug()
            )
            self.stdout.write(self.style.SUCCESS(f"Created product: {obj.name} (category: {category.name})"))

    def handle(self, *args, **options):
        self.faker = Faker('uz_UZ')

        num_categories = options['categories']
        num_products = options['products']
        if options['all']:
            num_categories = num_categories or 5
            num_products = num_products or 5

        if num_categories:
            self._generate_categories(num_categories)
        if num_products:
            self._generate_products(num_products)
        if not num_categories and not num_products:
            self.stdout.write(self.style.ERROR("No items created. Use --categories or --products or --all."))
