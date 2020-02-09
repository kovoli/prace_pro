from django.db import models
# slugify
from django.urls import reverse
from unidecode import unidecode
from django.template.defaultfilters import slugify
# Text-editor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Images
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.conf import settings


class Shop(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField(blank=True, null=True)
    link_to_shop = models.URLField(blank=True, null=True)  # TODO Убрать при Production
    favorites = models.BooleanField(default=False)
    shop_image = ProcessedImageField(upload_to='shop_images/%Y/%m',
                                     processors=[ResizeToFit(None, 250)],
                                     format='JPEG',
                                     options={'quality': 80},
                                     blank=True,
                                     max_length=250)

    class Meta:
        ordering = ['name']
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Shop, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('deals:deals_by_shop', args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = RichTextField(blank=True, null=True)
    brand_image = ProcessedImageField(upload_to='brand_images/%Y/%m',
                                      processors=[ResizeToFit(None, 250)],
                                      format='JPEG',
                                      options={'quality': 80},
                                      blank=True,
                                      max_length=250)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Brand, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('deals:brand', args=[self.slug])


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    short_description = RichTextField(blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    favorites = models.BooleanField(default=False)
    category_image = ProcessedImageField(upload_to='category_images/%Y/%m',
                                         processors=[ResizeToFit(None, 250)],
                                         format='JPEG',
                                         options={'quality': 80},
                                         blank=True,
                                         max_length=250)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [models.Index(fields=['slug'])]

    class MPTTMeta:
        order_insertion_by = ['-name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('deals:deals_by_category', args=[self.slug])


class Deal(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = RichTextUploadingField(blank=True, null=True, config_name='default')
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    oldprice = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    discount_procent = models.IntegerField(blank=True, null=True)
    link_to_shop = models.TextField()
    deal_is_online = models.BooleanField(default=True)
    status_publish = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    image = ProcessedImageField(upload_to='deal_images/%Y/%m',
                                processors=[ResizeToFit(None, 250)],
                                format='JPEG',
                                options={'quality': 80},
                                blank=True,
                                max_length=250)
    # user likes
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like', blank=True)
    like_counter = models.SmallIntegerField(default=0)

    # Related fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                               null=True, related_name='deal_author')
    category = TreeForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', related_name='brands', null=True, blank=True, on_delete=models.SET_NULL)
    shop = models.ForeignKey('Shop', related_name='shop', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-create']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def __str__(self):
        return self.name

    # Slugify function
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        if self.oldprice:
            self.discount_procent = round((self.oldprice - self.price) * 100 / self.oldprice)
        super(Deal, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('deals:deal_detail', args=[self.slug])


# class LikeDislike(models.Model):
#     deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='likes')
#     user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like', blank=True)
#     like_counter = models.SmallIntegerField(default=0)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    body = RichTextField(config_name='default')
    created = models.DateTimeField(auto_now_add=True)
    deal = models.ForeignKey(Deal, related_name='comments', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    like = models.PositiveIntegerField(default=0)

    # def __str__(self):
    #     return self.author.username

    class Meta:
        ordering = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'

