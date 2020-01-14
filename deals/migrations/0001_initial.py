# Generated by Django 3.0.2 on 2020-01-14 10:30

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('brand_image', imagekit.models.fields.ProcessedImageField(blank=True, max_length=250, upload_to='brand_images/%Y/%m')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('short_description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('favorites', models.BooleanField(default=False)),
                ('category_image', imagekit.models.fields.ProcessedImageField(blank=True, max_length=250, upload_to='category_images/%Y/%m')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='deals.Category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('shop_image', imagekit.models.fields.ProcessedImageField(blank=True, max_length=250, upload_to='shop_images/%Y/%m')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('oldprice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_procent', models.IntegerField(blank=True, null=True)),
                ('link_to_shop', models.TextField()),
                ('actual_deal_status', models.BooleanField(default=True)),
                ('status_publish', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='published', max_length=10)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, max_length=250, upload_to='category_images/%Y/%m')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('brands', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brands', to='deals.Brand')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='deals.Category')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop', to='deals.Shop')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
                'ordering': ['-create'],
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['slug'], name='deals_categ_slug_6e44ce_idx'),
        ),
    ]
