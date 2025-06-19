from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView, View, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, JsonResponse
from .models import Product, Category, Tag, Comment, Reaction
from .forms import AddProductForm, AddProductModelForm, UploadFileForm, ContactForm, CommentForm
from .utils import DataMixin
from django.conf import settings
import uuid
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from django.core.exceptions import PermissionDenied


class UploadFileView(FormView):
    form_class = UploadFileForm
    template_name = 'cosmetics/upload_file.html'
    success_url = reverse_lazy('upload_file')
    title_page = 'Загрузка файла'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        name, ext = (file.name.rsplit('.', 1) if '.' in file.name else (file.name, ''))
        suffix = str(uuid.uuid4())
        file_path = f"uploads/{name}_{suffix}{'.' + ext if ext else ''}"
        with open(settings.MEDIA_ROOT / file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        messages.success(self.request, f"Файл {file.name} успешно загружен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка загрузки файла.")
        return super().form_invalid(form)


class IndexView(DataMixin, ListView):
    model = Product
    template_name = 'cosmetics/index.html'
    context_object_name = 'products'
    title_page = 'Главная - Косметика'

    def get_queryset(self):
        return Product.objects.available()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, cat_selected=0)


class CatalogView(DataMixin, ListView):
    model = Product
    template_name = 'cosmetics/catalog.html'
    context_object_name = 'products'
    title_page = 'Каталог товаров'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort', '-created_at')
        search_query = self.request.GET.get('search', '')
        products = Product.objects.all()
        if search_query:
            products = Product.objects.search(search_query)
        return products.order_by(sort_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context,
            cat_selected=0,
            search_query=self.request.GET.get('search', ''),
            sort_by=self.request.GET.get('sort', '-created_at')
        )





class ShowCategoryView(DataMixin, ListView):
    model = Product
    template_name = 'cosmetics/catalog.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.by_category(self.kwargs['cat_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return self.get_mixin_context(
            context,
            title=f'Категория: {category.name}',
            cat_selected=category.id
        )


class ShowTagView(DataMixin, ListView):
    model = Product
    template_name = 'cosmetics/catalog.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(tags__slug=self.kwargs['tag_slug'], status=Product.ProductStatus.AVAILABLE.name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f'Тег: {tag.name}')


class AddProductView(LoginRequiredMixin, DataMixin, CreateView):
    model = Product
    form_class = AddProductForm
    template_name = 'cosmetics/add_product.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Добавить товар'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.status = Product.ProductStatus.AVAILABLE.name
        product.created_by = self.request.user
        product.save()
        messages.success(self.request, "Товар успешно добавлен!")
        return super().form_valid(form)

class AddProductModelView(LoginRequiredMixin, DataMixin, CreateView):
    permission_required = 'BeautyBoxApp.add_product'
    model = Product
    form_class = AddProductModelForm
    template_name = 'cosmetics/add_product_model.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Добавить товар (модель)'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.save()
        messages.success(self.request, "Товар успешно добавлен!")
        return super().form_valid(form)


class UpdateProductView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Product
    fields = ['name', 'slug', 'price', 'description', 'category', 'status', 'photo']
    template_name = 'cosmetics/add_product.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Редактирование товара'
    slug_url_kwarg = 'product_slug'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("Вы не можете редактировать этот товар.")
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно обновлен!")
        return super().form_valid(form)

class DeleteProductView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Product
    template_name = 'cosmetics/delete_product.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Удаление товара'
    slug_url_kwarg = 'product_slug'
    login_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("Вы не можете удалить этот товар.")
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно удален!")
        return super().form_valid(form)


class ContactView(DataMixin, View):
    template_name = 'cosmetics/contact.html'
    title_page = 'Контакты'

    def get(self, request):
        form = ContactForm()
        context = self.get_mixin_context({'form': form})
        return render(request, self.template_name, context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            
            messages.success(request, "Ваше сообщение успешно отправлено!")
            return redirect('contacts')
        else:
            messages.error(request, "Ошибка в данных формы.")
            context = self.get_mixin_context({'form': form})
            return render(request, self.template_name, context)


class AboutView(DataMixin, TemplateView):
    template_name = 'cosmetics/about.html'
    title_page = 'О нас'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)

class ShowProductView(DataMixin, DetailView):
    model = Product
    template_name = 'cosmetics/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True)
        # Добавляем количество лайков и дизлайков
        context['like_count'] = self.object.reactions.filter(reaction_type='LIKE').count()
        context['dislike_count'] = self.object.reactions.filter(reaction_type='DISLIKE').count()
        return self.get_mixin_context(context, title=self.object.name)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            Comment.objects.create(
                product=self.object,
                user=request.user,
                content=form.cleaned_data['content'],
                is_approved=True
            )
            messages.success(request, "Комментарий отправлен на модерацию!")
            return redirect(self.object.get_absolute_url())
        else:
            messages.error(request, "Ошибка в форме комментария.")
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)
    
class ReactToProductView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def post(self, request, product_slug, reaction_type):
        print(f"Received reaction: {reaction_type} for product: {product_slug} by user: {request.user}")  # Отладка
        product = get_object_or_404(Product, slug=product_slug)
        if reaction_type not in ['LIKE', 'DISLIKE']:
            return JsonResponse({'error': 'Недопустимый тип реакции'}, status=400)

        Reaction.objects.filter(product=product, user=request.user).delete()
        Reaction.objects.create(
            product=product,
            user=request.user,
            reaction_type=reaction_type
        )

        likes = product.reactions.filter(reaction_type='LIKE').count()
        dislikes = product.reactions.filter(reaction_type='DISLIKE').count()

        return JsonResponse({
            'success': True,
            'likes': likes,
            'dislikes': dislikes
        })