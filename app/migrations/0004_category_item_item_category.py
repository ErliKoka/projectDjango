# Generated by Django 5.2.3 on 2025-06-25 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_item_item_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_slug', models.SlugField(primary_key=True, serialize=False, unique=True)),
                ('category_name', models.CharField(blank=True, max_length=200, null=True)),
                ('category_image', models.ImageField(blank=True, null=True, upload_to='category/')),
                ('category_description', models.TextField(blank=True, max_length=2000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='item_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.category'),
        ),
    ]
