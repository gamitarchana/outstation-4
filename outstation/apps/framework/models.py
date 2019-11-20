from django.db import models
from wagtail.images.models import AbstractImage, AbstractRendition
from unidecode import unidecode
import os.path

# Create your models here.
class AdvancedImage(AbstractImage):
    upload_folder=models.CharField(max_length=100, null=False, default='original_images')

    def get_upload_to(self, filename):
        folder_name = self.upload_folder
        filename = self.file.field.storage.get_valid_name(filename)

        # do a unidecode in the filename and then
        # replace non-ascii characters in filename with _ , to sidestep issues with filesystem encoding
        filename = "".join((i if ord(i) < 128 else '_') for i in unidecode(filename))

        # Truncate filename so it fits in the 100 character limit
        # https://code.djangoproject.com/ticket/9893
        full_path = os.path.join(folder_name, filename)
        if len(full_path) >= 95:
            chars_to_trim = len(full_path) - 94
            prefix, extension = os.path.splitext(filename)
            filename = prefix[:-chars_to_trim] + extension
            full_path = os.path.join(folder_name, filename)

        return full_path

class AdvancedImageRendition(AbstractRendition):
    image = models.ForeignKey(AdvancedImage, related_name='renditions', on_delete = models.CASCADE)

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
