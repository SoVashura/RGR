# Generated by Django 5.1.6 on 2025-06-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeautyBoxApp', '0002_product_created_by_comment_reaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Одобрен'),
        ),
    ]
