#import json

#from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

#from wagtail.core.blocks import Block, BlockField, StreamBlock, StreamValue


class RichCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', 'default')
        self.features = kwargs.pop('features', None)
        # TODO: preserve 'editor' and 'features' when deconstructing for migrations
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from wagtail.admin.rich_text import get_rich_text_editor_widget
        defaults = {'widget': get_rich_text_editor_widget(self.editor, features=self.features)}
        defaults.update(kwargs)
        return super().formfield(**defaults)
