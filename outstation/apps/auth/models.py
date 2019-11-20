from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import os
import urllib.request

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_photo_url = models.URLField()
    profile_photo = models.ImageField(upload_to = 'user_profile/images', null = True)

    def save_image(self):
        if self.profile_photo_url and not self.profile_photo:
            result = urllib.request.urlretrieve(self.profile_photo_url)
            self.profile_photo.save(
                os.path.basename(self.profile_photo_url),
                File(open(result[0], 'rb'))
                )
            self.save()

    def __str__(self):
        return self.user.username
