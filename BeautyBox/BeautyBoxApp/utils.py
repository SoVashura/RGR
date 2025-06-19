from django.urls import reverse_lazy

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Каталог', 'url_name': 'catalog'},
    {'title': 'Добавить товар', 'url_name': 'add_product'},
    {'title': 'Добавить товар (модель)', 'url_name': 'add_product_model'},
    {'title': 'Загрузка файла', 'url_name': 'upload_file'},
    {'title': 'О нас', 'url_name': 'about'},
    {'title': 'Контакты', 'url_name': 'contacts'},
]

class DataMixin:
    paginate_by = 3
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context