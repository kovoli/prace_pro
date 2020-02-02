from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = ProcessedImageField(upload_to='user_photo/',
                                 processors=[ResizeToFit(None, 50)],
                                 format='JPEG',
                                 options={'quality': 100},
                                 blank=True,
                                 max_length=250)

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)


