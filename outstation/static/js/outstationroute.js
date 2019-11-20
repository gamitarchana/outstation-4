(function($) {

   'use strict'

    var placeFilter = {};
    var locationTypeFilter = new Map();
    var tripTypeFilter = new Map();
    var isSelectedAll = false;
    var isReviewScriptLoaded = false;
    var init = true;
    let lazyPictures = [].slice.call(document.querySelectorAll("picture.lazy"));
    let lazyImages = [].slice.call(document.querySelectorAll("img.lazy"));
    let active = false;
    let filteredPlaces = {};
    //let isCustomizedMap = false;

    var routeMap = function(){
      $("#routeMapButton").click(function(e){
        if(init){
          init = false;
          $("#filterPanel").removeClass("hide");
        }else{
          $("#selectAllButton").addClass("hide");
          $("#editButton").removeClass("hide");
          $("#routeMapButton").addClass("hide");
          $("#filterView").addClass("hide");
          showSelectedTagsView();
          generateRoute();
        }
      })
    }

    var showSelectedTagsView = function(){
      $('#selectedFilterView').empty();
      for (var [key, value] of locationTypeFilter) {
        $('#selectedFilterView').append("<div class='tag-selected'>"+value+"</div>");
      }
      for (var [key, value] of tripTypeFilter) {
        $('#selectedFilterView').append("<div class='tag-selected'>"+value+"</div>");
      }
      $('#selectedFilterView').removeClass('hide');
    }

    var generateRoute = function(){
      filteredPlaces={}
      $('#placesOnRoute').children('div').each(function(){
        let isPlaceFound = false;
        const placeId = $(this).data("id");
        const placeName = $(this).data("name");
        const locationTypes = $(this).data("location-tags");
        const tripTypes = $(this).data("trip-types");
        const filterMapId = "mapBlock-"+placeId;

        isPlaceFound = filterPlace(locationTypeFilter, locationTypes)

        if(!isPlaceFound){
          isPlaceFound = filterPlace(tripTypeFilter, tripTypes)
        }

        if(isPlaceFound){
          $(this).removeClass('hide');
          $(this).addClass('show');
          $('#'+filterMapId).removeClass('hide');
          $('#'+filterMapId).addClass('show');

          filteredPlaces[placeId] = placeName;

        } else {
          $(this).addClass('hide');
          $(this).removeClass('show');
          $('#'+filterMapId).removeClass('show');
          $('#'+filterMapId).addClass('hide');

          if(filteredPlaces[placeId] != undefined){
            delete filteredPlaces[placeId];
          }

        }
      })
    }

    var filterPlace = function(filterMap, tagList){
      let isPlaceFound = false
      for (var [key, value] of filterMap) {
        if(tagList[key] == value){
          isPlaceFound = true;
        }
      }
      return isPlaceFound;
    }
    /*var generateRoute = function() {
        filteredPlaces = {};
        if(!$.isEmptyObject(placeFilter) || !$.isEmptyObject(tripTypeFilter)){
            isCustomizedMap = true;
            $.each(outstationTaxiRoute.on_route_places.places, function( placeKey, placeValue ) {
              var place = placeValue;
              var locationTags = place.location_tags;
              var isPlaceFound = false;
              var tripTypes = place.trip_types;
              var filterLocationId = "placeOnRoute-"+place.id;
              var filterMapId = "mapBlock-"+place.id;
              let filteredPlace = {};

              $.each(locationTags, function( locationTagKey, locationTagValue ) {
                if(placeFilter[locationTagValue.id] != undefined){
                  $('#'+filterLocationId).removeClass('hide');
                  $('#'+filterMapId).removeClass('hide');
                  isPlaceFound = true;
                  filteredPlaces[place.id] = place.name;
                  return false;
                }
              });
              if(!isPlaceFound){
                $.each(tripTypes, function( tripTypeKey, tripTypeValue ) {
                  if(tripTypeFilter[tripTypeValue.id] != undefined){
                    $('#'+filterLocationId).removeClass('hide');
                    $('#'+filterMapId).removeClass('hide');
                    isPlaceFound = true;
                    filteredPlaces[place.id] = place.name;
                    return false;
                  }
                });
              }
              if(!isPlaceFound){
                  $('#'+filterLocationId).addClass('hide');
                  $('#'+filterMapId).addClass('hide');
              }
              isPlaceFound = false;
            });
          } else {
            isCustomizedMap = false;
            $('#dynamicRouteMap').children('div').each(function(){
              if($(this).hasClass("hide")){
                $(this).removeClass("hide")
              }
            })
            $('#placesOnRoute').children('div').each(function(){
              if($(this).hasClass("hide")){
                $(this).removeClass("hide")
              }
            })
          }
      }*/

    var locationTagButtons = function(){
      $('#placeFilter').on('click', function(e){
        e.stopImmediatePropagation()
        if(e.target !== e.currentTarget){
          var tagButton = e.target;
          var tagid = $(tagButton).data("id");
          var tag = $(tagButton).data("tag");
          if ($(tagButton).hasClass("tag-button-down")) {
              tagButton.classList.add("tag-button-up");
              tagButton.classList.remove("tag-button-down");
              locationTypeFilter.delete(tagid)
          } else {
            tagButton.classList.add("tag-button-down");
            tagButton.classList.remove("tag-button-up");
            if(locationTypeFilter.get(tagid) == undefined)
            {
              locationTypeFilter.set(tagid, tag);
            }
          }
        }
      });
    }

    var tripTypeButtons = function(){
      $('#tripTypeFilter').on('click', function(e){
        e.stopImmediatePropagation()
        if(e.target !== e.currentTarget){
          var tripTypeButton = e.target;
          var tripTypeid = $(tripTypeButton).data("id");
          var tripType = $(tripTypeButton).data("trip-type");
          if ($(tripTypeButton).hasClass("tripType-button-down")) {
              tripTypeButton.classList.add("tripType-button-up");
              tripTypeButton.classList.remove("tripType-button-down");
              tripTypeFilter.delete(tripTypeid)
          } else {
            tripTypeButton.classList.add("tripType-button-down");
            tripTypeButton.classList.remove("tripType-button-up");
            if(tripTypeFilter.get(tripTypeid) == undefined)
            {
              tripTypeFilter.set(tripTypeid, tripType);
            }
          }
        }
      });
    }

    var editFilterButton = function(){
      $('#editButton').on('click', function(e){
        $("#selectAllButton").removeClass("hide");
        $("#editButton").addClass("hide");
        $("#routeMapButton").removeClass("hide");
        $("#filterView").removeClass("hide");
        //enableFilterTags(false);
        $('#selectedFilterView').addClass('hide');
      })
    }

    var selectAllFilterButton = function(){
      $('#selectAllButton').on('click', function(e){
        e.stopImmediatePropagation();
        if(!isSelectedAll){
          $('#placeFilter').children('button').each(function(){
            $(this).addClass("tag-button-down");
            $(this).removeClass("tag-button-up");
            $('#selectAllButton').html("Remove All")
            var tagid = $(this).data("id");
            var tag = $(this).data("tag");
            if(locationTypeFilter.get(tagid) == undefined)
            {
              locationTypeFilter.set(tagid, tag);
            }
          });
        } else {
          locationTypeFilter.clear()
          $('#placeFilter').children('button').each(function(){
            $(this).removeClass("tag-button-down");
            $(this).addClass("tag-button-up");
            $('#selectAllButton').html("Select All")
          });
        }
        isSelectedAll=!isSelectedAll;
    });
  }

  $("#like_button_form").submit(function(e){
    e.preventDefault();
    const routeIdObj = JSON.parse(document.getElementById('routeId').textContent);
    $.ajax({
        type:'POST',
        url:'/like/',
        data:{
          route_id:routeIdObj['route_id'],
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(data){
          $("#likes_count").html(data.likes_count);
          if(data.is_liked == true){
            $('#like_button').addClass('border-bottom');
          }else{
            $('#like_button').removeClass('border-bottom');
          }
        }
      });
  })

  var reviewButton = function(){
    $("#writeReviewButton").on('click', function(e){
      if (!isReviewScriptLoaded ) {
        const reviewsURLObj = JSON.parse(document.getElementById('reviewUrl').textContent);
        $.getScript(reviewsURLObj["review_url"],function(){
          isReviewScriptLoaded = true;
          showReviewForm();
	     });
     } else {
       showReviewForm();
     }

   });
 }

  var showReviewForm = function(){
    $("#reviewListPanel").addClass("hide");
    $("#writeReviewPanel").removeClass("hide");
    $("html, body").animate({
     scrollTop: $("#writeReviewPanel").offset().top
   });
  }

  var scrollTo = function(section){
    $("html, body").animate({
      scrollTop: $(section).offset().top
    });
  }


  const lazyLoad = function() {
      if (active === false) {
        active = true;

        setTimeout(function() {
          lazyPictures.forEach(function(lazyPicture) {
            if ((lazyPicture.getBoundingClientRect().top <= window.innerHeight && lazyPicture.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyPicture).display !== "none") {
              let lazyPictureSources = [].slice.call(lazyPicture.querySelectorAll("source"));
              lazyPictureSources.forEach(function(lazyPictureSource) {
                lazyPictureSource.srcset = lazyPictureSource.dataset.srcset;
              });
              lazyPicture.classList.remove("lazy");
              lazyPictures = lazyPictures.filter(function(picture) {
                return picture !== lazyPicture;
              });
            }
          });
          lazyImages.forEach(function(lazyImage) {
            if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== "none") {
              lazyImage.src = lazyImage.dataset.src;
              lazyImage.classList.remove("lazy");

              lazyImages = lazyImages.filter(function(image) {
                return image !== lazyImage;
              });
            }
          });

          if (lazyImages.length === 0 && lazyPictures.length === 0) {
            document.removeEventListener("scroll", lazyLoad);
          }
          active = false;
        }, 200);
      }
    };

  $(document).scroll(lazyLoad);

  //$("#share_map_form").submit(function(e){

  $("#fbShareMap").on('click', function(e){
    e.preventDefault();
    shareMap('FACEBOOK')
    /*let isCustomizedMap = false;
    if(locationTypeFilter.size == 0 && tripTypeFilter.size == 0){
      isCustomizedMap = false;
    } else {
      isCustomizedMap = true;
    }
    $.ajax({
        type: 'POST',
        url: '/share_map/',
        data: {
          //route_id: routeIdObj['route_id'],
          filteredPlaces: JSON.stringify(filteredPlaces),
          isCustomizedMap: isCustomizedMap,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
          //console.log("share map success" + data);
          console.log("share map success" + data.map_url);
          console.log(FB);
          FB.ui({
            method: 'share',
            href: data.map_url,//'https://developers.facebook.com/docs/',
          }, function(response){
            if(response && !response.error_message){
              console.log("fb post success");
            } else {
              console.log("fb post error");
            }
          });
        }
      });*/
  });

  $("#pinShareMap").on('click', function(e){
    e.preventDefault();
    shareMap('PINTEREST');
  });

  var shareMap = function(socialMedia){
    let isCustomizedMap = false;
    if(locationTypeFilter.size == 0 && tripTypeFilter.size == 0){
      isCustomizedMap = false;
    } else {
      isCustomizedMap = true;
    }
    $.ajax({
        type: 'POST',
        url: '/share_map/',
        data: {
          //route_id: routeIdObj['route_id'],
          filteredPlaces: JSON.stringify(filteredPlaces),
          isCustomizedMap: isCustomizedMap,
          csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
          if(socialMedia === 'FACEBOOK'){
            FB.ui({
              method: 'share',
              href: 'https://meruimagestorage01.blob.core.windows.net/outstation/media/images/route-map_WN4FSLU.2e16d0ba.fill-900x400.png',//data.map_url,
            }, function(response){
              if(response && !response.error_message){
                console.log("fb post success");
              } else {
                console.log("fb post error");
              }
            });
          } else if(socialMedia === 'PINTEREST'){
            PinUtils.pinOne({
                /*'url': 'https://www.flickr.com/photos/kentbrew/6851/',*/
                'media': 'https://meruimagestorage01.blob.core.windows.net/outstation/media/images/route-map_WN4FSLU.2e16d0ba.fill-900x400.png',
                'description': 'Meru: route Map!'
            });
          }
        }
      });
  }
  /*var $("#fbShareMap").on('click', function(e){
    e.preventDefault();

  })*/
    var FBShareDialogInit = function(){
      $.getScript('https://connect.facebook.net/en_US/sdk.js', function(){
        FB.init({
          appId: '526324658135486',
          version: 'v2.7' // or v2.1, v2.2, v2.3, ...
        });
      });
    }
    var PinterestInit = function(){
      $.getScript("//assets.pinterest.com/js/pinit.js", function(){
        });
    }
	// Dom Ready
	$(function() {
    routeMap();
    locationTagButtons();
    tripTypeButtons();
    editFilterButton();
    selectAllFilterButton();
    reviewButton();
    FBShareDialogInit();
    PinterestInit();
   	});
})(jQuery);
