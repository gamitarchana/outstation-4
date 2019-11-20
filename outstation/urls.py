from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from search import views as search_views

from outstation.apps.reviews import views as reviews_views
from outstation.apps.auth import views as outstationauth_views
from outstation.apps.route import views as outstationroute_views
#from outstation.apps.reviews.views import ApprovedView

from .api import api_router
#from .sitemap import oustation_route_images_sitemap

#from qartez.views import render_images_sitemap

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

#    url(r'^admin/outstationreview/review/approved', ApprovedView.as_view()),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^', include('favicon.urls')),
    #url(r'^login/$', outstationauth_views.login, name='login'),
    url(r'^like/$', outstationroute_views.like_route, name='like_route'),
    url(r'^share_map/$', outstationroute_views.share_map, name='share_map'),
    #url(r'^amenities/(?P<route_id>[0-9]+)/$', outstationroute_views.amenities, name='amenities'),

    url(r'^oauth/', include('social_django.urls', namespace='social')),


    url(r'^reviewlist/(?P<route_id>[0-9]+)/$', reviews_views.review_list, name='review_list'),
    url(r'^review/$', reviews_views.review, name='review'),

    #url(r'^sitemap.xml$', sitemap),
    #url(r'^sitemap-images\.xml$', render_images_sitemap , {'sitemaps': oustation_route_images_sitemap}),
    #url(r'^robots\.txt', include('robots.urls')),
    #url(r'^%s/api/v2/' % settings.SUB_SITE, api_router.urls),
    url(r'^api/v2/', api_router.urls),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #url(r'^pages/', include(wagtail_urls)),
    #url(r'^%s/' % settings.SUB_SITE, include(wagtail_urls)),
    #url(r'^%s/#holes/$' % settings.SUB_SITE, 'donut.holes'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
