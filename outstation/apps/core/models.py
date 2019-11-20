from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from modelcluster.models import ClusterableModel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    FieldRowPanel
)
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from django import forms
from .enums import VehicleFeatureChoice, VehicleTypeChoice
from wagtailmetadata.models import MetadataMixin
from django.utils.translation import ugettext_lazy

class Place(index.Indexed, ClusterableModel):
    name = models.CharField(max_length = 255, null = False, blank = False, unique=True)
    details = models.TextField(null = False, blank = False, help_text = "Add place details")

    duration_of_visit = models.DurationField(null = True,
                                            blank = True,
                                            default = '00:00:00',
                                            verbose_name = ('Duration Of Visit (HH:MM:SS)'),
                                            help_text = ('[DD] [HH:[MM:]]ss[.uuuuuu] format')
                                )

    map_icon = models.ForeignKey(
            "wagtailimages.Image",
            null = True,
            blank = True,
            on_delete = models.SET_NULL,
            related_name = "+"
        )

    trip_types = ParentalManyToManyField('TripType', blank = False)
    location_tags = ParentalManyToManyField('LocationTag', blank = False)
    panels = [
                FieldPanel("name"),
                FieldPanel("details"),
                FieldPanel("duration_of_visit"),
                ImageChooserPanel("map_icon"),
                MultiFieldPanel([
                    InlinePanel("place_images", min_num=1),
                    ], heading="Images" ),
                FieldPanel('trip_types', widget = forms.CheckboxSelectMultiple),
                FieldPanel('location_tags', widget = forms.CheckboxSelectMultiple),
            ]

    search_fields = [
            index.SearchField('name', partial_match = True),
        ]

    def __str__(self):
        return self.name

register_snippet(Place)

class PlaceImages(Orderable):
    place = ParentalKey('Place',
                    related_name = "place_images",
                    null = False,
                    blank = False
                )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.CASCADE,
        related_name = "+"
    )


    panels = [
            ImageChooserPanel("image"),
        ]

    """def get_absolute_url(self):

            Returns absolute url for banner_image to generate image site map

        kwargs = {'slug': self.slug}
        return reverse('places.detail', kwargs=kwargs)"""

    def place_image_url(self):
        """
            Returns the banner_image url for XML images sitemap.
        """
        url = settings.MEDIA_URL + self.image.file.name
        print(self.image.file.name)
        return url if self.image else ''

    def place_image_title(self):
        """
            Returns the banner_image title for XML images sitemap.
        """
        return self.image.title if self.image else ''

    class Meta:
        unique_together = (
            ('place', 'image'),
        )


class LocationTag(models.Model):
    tag = models.CharField(max_length = 255, blank = False, null = False, unique=True, help_text = "Location tag")

    panels = [
                FieldPanel("tag"),
            ]

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = "Location Tag"
        verbose_name_plural = "Location Tags"


register_snippet(LocationTag)

class TripType(models.Model):
    trip_type = models.CharField(max_length = 255, blank = False, null = False, unique=True, help_text = "Trip type")

    panels = [
                FieldPanel("trip_type"),
            ]

    def __str__(self):
        return self.trip_type

    class Meta:
        verbose_name = "Trip Type"
        verbose_name_plural = "Trip Types"


register_snippet(TripType)

class FareTable(models.Model):
    vehicle_type = models.CharField(max_length = 50,
                                    blank = False,
                                    null = False,
                                    choices = [(type.value, type.name.replace("_", " - ").upper()) for type in VehicleTypeChoice],
                                    default = VehicleTypeChoice.hatchback
                                )

    model = models.CharField(max_length = 255, blank = False, null = False)
    seater = models.PositiveSmallIntegerField(null = False, default = 0)
    per_km_rate = models.PositiveSmallIntegerField(null = False, default = 0, verbose_name = ('Per km rate (\u20B9)'))
    vehicle_feature = models.CharField( max_length = 20,
                                    choices = [(feature.value, feature.name.replace("_", " - ").upper()) for feature in VehicleFeatureChoice],
                                    default = VehicleFeatureChoice.AC
                                )

    panels = [
                FieldPanel("vehicle_type"),
                FieldPanel("model"),
                FieldPanel("seater"),
                FieldPanel("per_km_rate"),
                FieldPanel("vehicle_feature"),
            ]

    def __str__(self):
        return self.vehicle_type +' - '+ self.model

    class Meta:
        verbose_name = "Fare"
        verbose_name_plural = "Fares"


register_snippet(FareTable)


class PopularRoutes(ClusterableModel):
    region = models.CharField(max_length = 255, blank = False, null = True, unique=True)

    panels = [
                FieldPanel("region"),
                MultiFieldPanel([
                    InlinePanel("region_routes", min_num=1),
                ], heading="Poular Routes"),
            ]

    class Meta:
        verbose_name = "Popular Route"
        verbose_name_plural = "Popular Routes"

    def __str__(self):
        return self.region;

register_snippet(PopularRoutes)

class RouteLink(Orderable):
    popular_route = ParentalKey('PopularRoutes',
                    related_name = "region_routes",
                    null = False,
                    blank = False
                )
    name = models.CharField(max_length = 255, blank = False, null = False, unique = True)
    url = models.URLField()

    panels = [
                FieldRowPanel([
                    FieldPanel('name', classname="col6"),
                    FieldPanel('url', classname="col6"),
                ]),
            ]
    class Meta:
        unique_together = (
            ('popular_route', 'name'),
        )

class PageMetadataMixin(MetadataMixin, models.Model):
    """An implementation of MetadataMixin for Wagtail pages."""
    search_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=ugettext_lazy('Search image')
    )

    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldPanel('seo_title'),
            FieldPanel('show_in_menus'),
            FieldPanel('search_description'),
            ImageChooserPanel('search_image'),
            FieldPanel('canonical_url'),
            FieldPanel('robots_tag')

        ], ugettext_lazy('Common page configuration')),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description

    def get_meta_image(self):
        return self.search_image

    def get_canonical_url(self):
        return self.canonical_url

    def get_robots_tag(self):
        return self.robots_tag

    class Meta:
        abstract = True
