from django.urls import path, register_converter
from . import views, converters
from django.conf import settings
from django.conf.urls.static import static

register_converter(converters.SlugConverter, 'slug')

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('catalog/', views.CatalogView.as_view(), name='catalog'),
    path('product/<slug:product_slug>/', views.ShowProductView.as_view(), name='product'),
    path('category/<slug:cat_slug>/', views.ShowCategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.ShowTagView.as_view(), name='tag'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('add_product_model/', views.AddProductModelView.as_view(), name='add_product_model'),
    path('edit/<slug:product_slug>/', views.UpdateProductView.as_view(), name='edit_product'),
    path('delete/<slug:product_slug>/', views.DeleteProductView.as_view(), name='delete_product'),
    path('upload_file/', views.UploadFileView.as_view(), name='upload_file'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('product/<slug:product_slug>/react/<str:reaction_type>/', views.ReactToProductView.as_view(), name='react_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)