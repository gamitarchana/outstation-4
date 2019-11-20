from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import OutstationRoutePage, OnRouteTouristPlaces
from django.utils.http import urlencode
from django.conf import settings
from django.core.files import File
import urllib.request
import os, hmac, hashlib, json, time
from django.core.files.storage import FileSystemStorage


def like_route(request):
    route = get_object_or_404(OutstationRoutePage, id = request.POST.get('route_id'))
    is_liked = False
    if(route.likes.filter(id = request.user.id)).exists():
        route.likes.remove(request.user)
        is_liked = False
    else:
        route.likes.add(request.user)
        is_liked = True
    count = route.likes.count()
    return JsonResponse({'likes_count':count, 'is_liked':is_liked})

def share_map(request):
    #route = get_object_or_404(OutstationRoutePage, id = request.POST.get('route_id'))
    #customized_map_url = settings.BASE_URL + request.get_full_path() + '/customized_route_map/'
    customized_map_url = 'https://gamita.pythonanywhere.com/chennai-pondicherry-2/customized_route_map/'
    #customized_map_url = 'http://localhost:8000/chennai-pondicherry/customized_route_map/'
    #print(customized_map_url)
    route_title = ""
    if request.method == 'POST':
        filtered_places = request.POST.get('filteredPlaces')
        is_customized_map = request.POST.get('isCustomizedMap')
        if filtered_places:
            #filtered_places = json.loads(filtered_places)
            #is_customized_map = "True"
            customized_map_url = customized_map_url+'?filteredPlaces='+filtered_places+'&isCustomizedMap='+is_customized_map
            #customized_map_url = 'http://gamita.pythonanywhere.com/chennai-pondicherry/customized_route_map/?filteredPlaces={"5":"Crocodile Park"}'
    #customized_map_url = settings.BASE_URL + request.get_full_path() + '/customized_route_map/?filteredPlaces=filtered_places'
    #customized_map_url = 'http://gamita.pythonanywhere.com/chennai-pondicherry/customized_route_map/?
    # set your access key, secret keyword and target URL
    #access_key = settings.SCREENSHOT_API_ACCESS_KEY #"34a63cc49f74b24d224538eb1e9893be"
    #secret_keyword = settings.SCREENSHOT_API_SECRET_KEYWORD#"outstationroute"
    #url = customized_map_url #"https://www.meru.in/outstation-cab-booking/mumbai-to-nashik-cabs/"
    #print(url)
    # set optional parameters (leave blank if unused)
    params = {
        'fullpage': '1',
        'width': '',
        'viewport': '',
        'format': 'JPG',
        'css_url': '',
        'delay': '',
        'ttl': '',
        'force': '',
        'placeholder': '',
        'user_agent': '',
        'accept_lang': '',
        'export': ''
    };
    customized_map_image_url = screenshotlayer(settings.SCREENSHOT_API_ACCESS_KEY, settings.SCREENSHOT_API_SECRET_KEYWORD, customized_map_url, params)
    #print(customized_map_image_url)
    current_time = time.strftime("%Y%m%d_%H%M%S")
    filename = "map_"+route_title+current_time+"."+params["format"]
    fs = FileSystemStorage(location = settings.MEDIA_ROOT+'/customized_map', base_url=settings.MEDIA_ROOT)
    if customized_map_image_url:
        map_image = urllib.request.urlretrieve(customized_map_image_url)
        #print(type(map_image))
        #route.customized_map.save(
        #    os.path.basename(filename),
        #    File(open(map_image[0], 'rb'))
        #    )
        #route.save()
        file = fs.save(os.path.basename(filename), File(open(map_image[0], 'rb')))
        uploaded_file_url = fs.url(file)
    #print(settings.MEDIA_ROOT)
    map_url = settings.BASE_URL+'/customized_map/'+uploaded_file_url#settings.MEDIA_ROOT+uploaded_file_url
    return JsonResponse({'map_url':map_url})

def screenshotlayer(access_key, secret_keyword, url, args):

    # encode URL
    query = urlencode(dict(url=url, **args))

    url_secret_keyword= '{}{}'.format(url, secret_keyword)

    # generate md5 secret key
    secret_key = hashlib.md5(url_secret_keyword.encode()).hexdigest()

    return "https://api.screenshotlayer.com/api/capture?access_key=%s&secret_key=%s&%s" % (access_key, secret_key, query)
