from django.contrib.sitemaps import Sitemap
from qartez.sitemaps import ImagesSitemap, StaticSitemap, RelAlternateHreflangSitemap

from outstation.apps.route.models import OutstationRoutePage
from outstation.apps.core.models import PlaceImages, Place


 # ---------------------- XML images sitemap part ---------------------------
 # Dictionary to feed to the images sitemap.
oustation_images_dict = {
    # Base queryset to iterate when procuding a site map
    'queryset': OutstationRoutePage.objects.all(),
    'image_location_field': 'banner_image_url', # Image location (URL)
    'image_title_field': 'banner_image_title', # Image title
    # An absolute URL of the page where image is shown
    'location_field': 'get_absolute_url'
}

oustation_route_images_dict = {
    # Base queryset to iterate when procuding a site map
    'queryset': PlaceImages.objects.all(),
    'image_location_field': 'place_image_url', # Image location (URL)
    'image_title_field': 'place_image_title', # Image title
    # An absolute URL of the page where image is shown
    'location_field': 'place_image_url'
}

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

images_dict = merge_two_dicts(oustation_images_dict, oustation_route_images_dict)
 # XML images sitemap.
oustation_route_images_sitemap = {
    'oustation_images': ImagesSitemap(oustation_images_dict, priority=0.6),
}
