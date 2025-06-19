from django.core.management.base import BaseCommand
from BeautyBoxApp.models import Category, Product, ProductStatus
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Заполняет базу данных начальными данными'

    def handle(self, *args, **options):
        # Очистка базы данных
        self.stdout.write('Очистка базы данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        self.stdout.write('Создание категорий...')
        categories = {
            'lips': Category.objects.create(name='Губы', slug='lips'),
            'eyes': Category.objects.create(name='Глаза', slug='eyes'),
            'face': Category.objects.create(name='Лицо', slug='face'),
            'nails': Category.objects.create(name='Ногти', slug='nails'),
            'skin': Category.objects.create(name='Уход за кожей', slug='skin'),
        }

        # Создание товаров
        self.stdout.write('Создание товаров...')
        products = [
            {
                'name': 'Помада Matte',
                'slug': 'pomada-matte',
                'price': 1500,
                'description': 'Матовая помада с насыщенным цветом. Долгое время держится на губах, не сушит кожу.',
                'category': categories['lips'],
                'is_available': True,
                'status': ProductStatus.AVAILABLE.name,
            },
            {
                'name': 'Тушь Volume',
                'slug': 'tush-volume',
                'price': 1200,
                'description': 'Тушь для объема ресниц. Не осыпается и не растекается в течение дня.',
                'category': categories['eyes'],
                'is_available': True,
                'status': ProductStatus.AVAILABLE.name,
            },
            {
                'name': 'Тональный крем',
                'slug': 'tonalnyj-krem',
                'price': 2000,
                'description': 'Легкий тональный крем для всех типов кожи. Обладает SPF-защитой.',
                'category': categories['face'],
                'is_available': False,
                'status': ProductStatus.OUT_OF_STOCK.name,
            },
            {
                'name': 'Лак для ногтей',
                'slug': 'lak-dlya-nogtej',
                'price': 800,
                'description': 'Лак для ногтей с блестками. Стойкое покрытие до 7 дней.',
                'category': categories['nails'],
                'is_available': True,
                'status': ProductStatus.AVAILABLE.name,
            },
            {
                'name': 'Крем для лица ночной',
                'slug': 'krem-dlya-litsa-nochnoy',
                'price': 2500,
                'description': 'Ночной крем для лица с гиалуроновой кислотой. Глубоко увлажняет и питает кожу.',
                'category': categories['skin'],
                'is_available': True,
                'status': ProductStatus.AVAILABLE.name,
            },
            {
                'name': 'Гель для умывания',
                'slug': 'gel-dlya-umyvaniya',
                'price': 1100,
                'description': 'Мягкий гель для умывания для всех типов кожи. Удаляет макияж и загрязнения.',
                'category': categories['skin'],
                'is_available': True,
                'status': ProductStatus.AVAILABLE.name,
            },
            {
                'name': 'Тени для век',
                'slug': 'teni-dlya-vek',
                'price': 1800,
                'description': 'Палетка теней для век с 12 оттенками. Матовые и шиммерные текстуры.',
                'category': categories['eyes'],
                'is_available': True,
                'status': ProductStatus.COMING_SOON.name,
            },
            {
                'name': 'Блеск для губ',
                'slug': 'blesk-dlya-gub',
                'price': 900,
                'description': 'Блеск для губ с эффектом увеличения объема. Не липкий.',
                'category': categories['lips'],
                'is_available': True,
                'status': ProductStatus.AVAILABLE.name,
            },
        ]

        for product_data in products:
            Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!')) 