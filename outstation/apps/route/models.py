from django.db import models
from django.db.models import Avg
from wagtail.core.models import Page, Orderable
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.template.response import TemplateResponse
from wagtailmetadata.models import MetadataPageMixin

from wagtail.core.fields import RichTextField

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
    FieldRowPanel,
    HelpPanel
)
from wagtail.api import APIField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from modelcluster.fields import ParentalKey
from django.conf import settings
from django.contrib.auth.models import User
from outstation.apps.core import blocks, enums

from outstation.apps.core.models import LocationTag, TripType, FareTable, Place, PopularRoutes
from outstation.apps.core.serializers import PlaceSerializer, PlaceListSerializer
from wagtail.snippets.edit_handlers import SnippetChooserPanel


from wagtailschemaorg.models import PageLDMixin
from wagtailschemaorg.utils import extend

from outstation.apps.framework.fields import RichCharField

import json

#import logging
#logger = logging.getLogger(__name__)


# Create your models here.

class OutstationRoutePage(RoutablePageMixin, MetadataPageMixin, Page):
    template = "route/outstation_route_page.html"

    banner_title = RichCharField(max_length=255, features = ['h1','h2', 'h3', 'h4', 'h5', 'h6'], null=True)
    banner_image = models.ForeignKey(
            "wagtailimages.Image",
            null = True,
            blank = False,
            on_delete = models.SET_NULL,
            related_name = "+"
        )

    origin = models.ForeignKey(
            "outstationcore.Place",
            null = True,
            on_delete = models.SET_NULL,
            related_name = "route_origin"
        )
    origin_display_name = RichCharField(max_length=255, null = True, blank = True, features = ['h1','h2', 'h3', 'h4', 'h5', 'h6'])

    destination = models.ForeignKey(
            "outstationcore.Place",
            null = True,
            on_delete = models.SET_NULL,
            related_name = "route_destination"
        )
    destination_display_name = RichCharField(max_length=255, null = True, blank = True, features = ['h1','h2', 'h3', 'h4', 'h5', 'h6'])

    road_condition_rating = models.PositiveSmallIntegerField()
    highway = models.CharField(max_length=255, null = False)
    total_distance = models.DecimalField(null = False,
                                            default = 0,
                                            max_digits=10,
                                            decimal_places=2,
                                            verbose_name = ('Total distance (km)'))
    likes = models.ManyToManyField(User, related_name = 'likes', blank = True)

    canonical_url = models.URLField(null = True, blank = False, help_text = "Canonical url for this page")
    robots_tag = models.CharField(max_length = 255, null = True, blank = True)
    excerpt = models.CharField(max_length = 255, null = True, blank = True)
    #customized_map = models.ImageField(upload_to = 'customized_map', null = True, max_length=255)

    api_fields = [
        APIField("banner_title"),
        APIField("banner_image"),
        APIField("origin", serializer = PlaceSerializer()),
        APIField("destination", serializer = PlaceSerializer()),
        APIField("on_route_places", serializer = PlaceListSerializer()),
        APIField("destination_places", serializer = PlaceListSerializer()),
        APIField("road_condition_rating"),
        APIField("highway"),
        APIField("total_distance"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        ImageChooserPanel("banner_image"),
        FieldRowPanel([
            SnippetChooserPanel('origin', classname="col6"),
            FieldPanel('origin_display_name', classname="col6"),
        ]),
        FieldRowPanel([
            SnippetChooserPanel('destination', classname="col6"),
            FieldPanel('destination_display_name', classname="col6"),
        ]),
        FieldPanel("highway"),
        MultiFieldPanel([
            InlinePanel("on_route_places"),
        ], heading="On Route Places" ),
        MultiFieldPanel([
            InlinePanel("destination_places"),
        ], heading="Destination Tourist Places" ),
        MultiFieldPanel([
            InlinePanel("route_information"),
        ], heading="Route Information"),
        FieldPanel("road_condition_rating"),
        FieldPanel("total_distance"),
        FieldPanel("excerpt"),
    ]

    promote_panels = MetadataPageMixin.promote_panels + [
            FieldPanel("canonical_url"),
            FieldPanel("robots_tag")
        ]

    @route(r'^amp/$')
    def amp(self, request):
        context = self.get_context(request)
        response = TemplateResponse(
            request, 'route/outstation_route_page_amp.html', context
        )
        return response

    @route(r'^customized_route_map/$')
    def customized_route_map(self, request):
        context = self.get_context(request)
        filtered_places = request.GET.get('filteredPlaces')
        is_customized_map = request.GET.get('isCustomizedMap')
        '''print("---filtered_places----")
        print(filtered_places)
        logger.info('---filtered_places----')
        logger.info(filtered_places)'''
        if filtered_places:
            filtered_places = json.loads(filtered_places)
            context["is_customized_map"] = True if is_customized_map == 'true' else False
            context["filtered_places"] = filtered_places
            '''print("---context[filtered_places]----")
            print(filtered_places)
            logger.info('------context[filtered_places]--------')
            logger.info(filtered_places)'''
        response = TemplateResponse(
            request, 'map/customized_route_map.html', context
        )
        return response

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        location_tags = LocationTag.objects.all()
        context["location_tags"] = location_tags

        trip_types = TripType.objects.all()
        context["trip_types"] = trip_types

        fare_table = FareTable.objects.all()
        context["fare_table"] = fare_table

        context["total_likes"] = self.total_likes()

        context["total_reviews"] = self.total_reviews()

        context["reviews_list"] = self.reviews_list()

        popular_routes = PopularRoutes.objects.all()
        context["popular_routes"] = popular_routes

        context["amenities"] = enums.AmenitiesChoice

        context["vehicle_types"] = enums.VehicleTypeChoice

        context["booking_form_url"] = settings.BOOKING_FORM_URL

        return context

    def total_likes(self):
        return self.likes.count()

    def total_reviews(self):
        return self.page_review.count()

    def reviews_list(self):
        reviews = self.page_review.all().order_by('-publish_date')
        return reviews

'''    def aggregate_rating(self):
        avg_rating = self.page_review.aggregate(Avg('rating'))["rating__avg"]
        return avg_rating

    def get_absolute_url(self):
        """
            Returns absolute url for banner_image to generate image site map
        """
        kwargs = {'slug': self.slug}
        return reverse('outstationroute.detail', kwargs=kwargs)

    def banner_image_url(self):
        """
            Returns the banner_image url for XML images sitemap.
        """
        url = settings.MEDIA_URL + self.banner_image.file.name
        return url if self.banner_image else ''

    def banner_image_title(self):
        """
            Returns the banner_image title for XML images sitemap.
        """
        return self.banner_image.title if self.banner_image else ''

'''


class OnRouteTouristPlaces(Orderable):
    """

    """
    page = ParentalKey("outstationroute.OutstationRoutePage",
                    related_name = "on_route_places",
                    null = False,
                    blank = False
                )
    #place = models.ForeignKey(
    #    "outstationcore.Place",
    #    null=True, unique=True,
    #    on_delete=models.SET_NULL,
    #    related_name="+")
    place = models.ForeignKey(
            "outstationcore.Place",
            null = True,
            on_delete = models.CASCADE,
            related_name = "+"
        )

    distance_from_origin = models.DecimalField(null = False,
                                            default = 0,
                                            max_digits=10,
                                            decimal_places=2,
                                            verbose_name = ('Distance From Origin (km)'))

    detour = models.CharField(max_length = 255, null = True, blank = True, verbose_name = ('Detour via'))
    #detour_distance = models.IntegerField(null = True, blank = True, default = 0, verbose_name = ('Detour from main route (km)'))
    detour_distance = models.DecimalField(null = True, blank = True, default = 0, verbose_name = ('Distance from main route (km)'), max_digits=10, decimal_places=2)

    amenities = StreamField(
            [
                ("amenity", blocks.AmenitiesBlock()),
            ],
            null = True,
            blank = True
        )
    panels = [
            SnippetChooserPanel("place"),
            FieldPanel("distance_from_origin"),
            HelpPanel(content=" Please provide below information if it is detour"),
            FieldRowPanel([
                FieldPanel('detour', classname="col6"),
                FieldPanel('detour_distance', classname="col6"),
            ]),
            StreamFieldPanel("amenities"),
        ]

    class Meta:
        unique_together = (
            ('page', 'place'),
        )


class DestinationTouristPlaces(Orderable):
    page = ParentalKey("outstationroute.OutstationRoutePage",
                    related_name = "destination_places",
                    null = False,
                    blank = False
                )
    place = models.ForeignKey(
        "outstationcore.Place",
        null=True,
        on_delete = models.CASCADE,
        related_name="+"
    )

    panels = [
            SnippetChooserPanel("place"),
        ]

    class Meta:
        unique_together = (
            ('page', 'place'),
        )

class RouteInformation(Orderable):
    """

    """
    page = ParentalKey(
            "outstationroute.OutstationRoutePage",
            related_name = "route_information",
            null = False,
            blank = False
        )
    information = RichTextField( features = ['h1','h2', 'h3', 'h4', 'h5', 'h6'], help_text = "Add information with heading" )
    #information = models.TextField( null = False, help_text = "Add details" )
    panels = [
            #FieldPanel("heading"),
            FieldPanel("information"),
        ]
