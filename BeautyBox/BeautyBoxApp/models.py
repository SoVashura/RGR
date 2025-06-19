from django.db import models
from django.urls import reverse
from enum import Enum
from django.contrib.auth import get_user_model



# Менеджер для модели продуктов
class ProductManager(models.Manager):
    def available(self):
        """Возвращает только доступные товары"""
        return self.filter(status=Product.ProductStatus.AVAILABLE.name)
    
    def by_category(self, category_slug):
        """Возвращает товары из указанной категории"""
        return self.filter(category__slug=category_slug, status=Product.ProductStatus.AVAILABLE.name)
    
    def search(self, query):
        """Поиск товаров по названию или описанию"""
        return self.filter(models.Q(name__icontains=query) | 
                          models.Q(description__icontains=query))

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-идентификатор")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Product(models.Model):
    # Создаем перечисление для статуса товара
    class ProductStatus(Enum):
        AVAILABLE = 'Доступен'
        OUT_OF_STOCK = 'Нет в наличии'
        COMING_SOON = 'Скоро в продаже'
        
        @classmethod
        def choices(cls):
            return [(item.name, item.value) for item in cls]
        
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        default=None,
        blank=True,
        null=True,
        verbose_name="Фото"
    )
    name = models.CharField(max_length=200, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-идентификатор")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    tags = models.ManyToManyField('Tag', blank=True, related_name='products', verbose_name="Теги")
    manufacturer = models.OneToOneField('Manufacturer', on_delete=models.SET_NULL, null=True, blank=True, related_name='product', verbose_name="Производитель")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    status = models.CharField(
        max_length=20, 
        choices=[(status.name, status.value) for status in ProductStatus],
        default=ProductStatus.AVAILABLE.name,
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_products',
        verbose_name="Создан пользователем"
    )
    
    # Используем пользовательский менеджер
    objects = ProductManager()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})
    
    @property
    def is_available(self):
        """Возвращает True, если товар доступен"""
        return self.status == self.ProductStatus.AVAILABLE.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название тега")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-идентификатор")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название производителя")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Товар"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
        verbose_name="Пользователь"
    )
    content = models.TextField(max_length=1000, verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_approved = models.BooleanField(default=True, verbose_name="Одобрен")

    def __str__(self):
        return f"Комментарий от {self.user} к {self.product}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']
    

class Reaction(models.Model):
    REACTION_TYPES = (
        ('LIKE', 'Лайк'),
        ('DISLIKE', 'Дизлайк'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name="Товар"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name="Пользователь"
    )
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES, verbose_name="Тип реакции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Реакция"
        verbose_name_plural = "Реакции"
        unique_together = ['product', 'user']  # Один пользователь — одна реакция на продукт