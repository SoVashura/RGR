from django.contrib import admin
from django.contrib import messages
from .models import Product, Category, Tag, Manufacturer, Comment
from django.utils.safestring import mark_safe

class ManufacturerFilter(admin.SimpleListFilter):
    title = 'Наличие производителя'
    parameter_name = 'manufacturer_status'

    def lookups(self, request, model_admin):
        return [
            ('has_manufacturer', 'С производителем'),
            ('no_manufacturer', 'Без производителя'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'has_manufacturer':
            return queryset.filter(manufacturer__isnull=False)
        elif self.value() == 'no_manufacturer':
            return queryset.filter(manufacturer__isnull=True)
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status', 'created_at', 'description_length', 'tags_count', 'photo_thumbnail')
    list_display_links = ('id', 'name')
    list_editable = ('price', 'status')
    ordering = ['-created_at', 'name']
    list_per_page = 10
    actions = ['make_available', 'make_out_of_stock']
    search_fields = ['name__startswith', 'description']
    list_filter = [ManufacturerFilter, 'category__name', 'status']
    exclude = ['created_at', 'updated_at']
    filter_horizontal = ['tags']

    @admin.display(description="Длина описания")
    def description_length(self, obj):
        return f"{len(obj.description)} символов"

    @admin.display(description="Количество тегов")
    def tags_count(self, obj):
        return obj.tags.count()
    
    @admin.display(description="Превью фото")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')
        return "Без фото"

    @admin.action(description="Сделать товары доступными")
    def make_available(self, request, queryset):
        count = queryset.update(status=Product.ProductStatus.AVAILABLE.name)
        self.message_user(request, f"{count} товар(ов) сделано доступными.", messages.SUCCESS)

    @admin.action(description="Сделать товары недоступными")
    def make_out_of_stock(self, request, queryset):
        count = queryset.update(status=Product.ProductStatus.OUT_OF_STOCK.name)
        self.message_user(request, f"{count} товар(ов) снято с продажи.", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    list_editable = ('slug',)

admin.site.register(Tag)
admin.site.register(Manufacturer)
admin.site.register(Comment)