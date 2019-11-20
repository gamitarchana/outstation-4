from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^', include('favicon.urls')),
    #url(r'^login/$', outstationauth_views.login, name='login'),
    url(r'^like/$', outstationroute_views.like_route, name='like_route'),
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
]
