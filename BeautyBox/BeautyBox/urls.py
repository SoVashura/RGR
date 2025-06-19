from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Панель администрирования BeautyBox"
admin.site.index_title = "Управление косметическим магазином"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BeautyBoxApp.urls')),
    path('users/', include('users.urls')),
]