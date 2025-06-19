from django import forms
from django.core.validators import MinLengthValidator
from .models import Category, Product

class AddProductForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        min_length=5,
        label="Название товара",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': 'Название слишком короткое (минимум 5 символов)',
            'required': 'Название обязательно'
        }
    )
    slug = forms.SlugField(
        max_length=200,
        label="URL-идентификатор",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[MinLengthValidator(5, message="URL должен содержать минимум 5 символов")]
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Цена",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'Цена обязательна'}
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label="Описание",
        required=False
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="Выберите категорию",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- "
        if not (set(name) <= set(ALLOWED_CHARS)):
            raise forms.ValidationError("Название должно содержать только русские буквы, цифры, дефис и пробел.")
        return name
    

class AddProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'price', 'description', 'category', 'status', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название товара',
            'slug': 'URL-идентификатор',
            'price': 'Цена',
            'description': 'Описание',
            'category': 'Категория',
            'status': 'Статус',
            'photo': 'Фото',
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 50:
            raise forms.ValidationError('Название не должно превышать 50 символов.')
        return name
    

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл", widget=forms.FileInput(attrs={'class': 'form-control'}))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Ваш комментарий",
        max_length=1000,
        error_messages={'required': 'Комментарий обязателен'}
    )