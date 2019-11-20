from wagtail.core import blocks
from .enums import AmenitiesChoice

class AmenitiesBlock(blocks.StructBlock):
    amenity_type = blocks.ChoiceBlock(required = True,
                                    choices = [(amenity.value, amenity.name.replace("_", " ").title()) for amenity in AmenitiesChoice],
                                    default = AmenitiesChoice.lodging
                                )

    location = blocks.CharBlock(required = True)
