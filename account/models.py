from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill
from django.shortcuts import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = ProcessedImageField(upload_to='user_photo/',
                                 processors=[ResizeToFill(100, 100)],
                                 format='JPEG',
                                 options={'quality': 100},
                                 blank=True,
                                 max_length=250)

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)

    def get_absolute_url(self):
         return reverse('profile', args=[self.user])

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'




