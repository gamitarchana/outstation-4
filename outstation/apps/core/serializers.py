from rest_framework.fields import Field

class PlaceSerializer(Field):
    def to_representation(self, value):
        trip_types = []
        location_tags = []
        for trip_type in value.trip_types.all():
            trip_types.append({"id":trip_type.id , "trip_type":trip_type.trip_type})
        for tag in value.location_tags.all():
            location_tags.append({"id":tag.id , "tag":tag.tag})

        return {
            "id": value.id,
            "name": value.name,
            "details": value.details,
            "duration_of_visit": value.duration_of_visit,
            "trip_types": trip_types,
            "location_tags": location_tags,
        }

class PlaceListSerializer(Field):
    def to_representation(self, value):
        places = []
        for item in value.all():
            place = item.place
            if hasattr(item, 'distance_from_origin'):
                distance_from_origin = item.distance_from_origin
            trip_types = []
            location_tags = []

            for trip_type in place.trip_types.all():
                trip_types.append({"id":trip_type.id , "trip_type":trip_type.trip_type})
            for tag in place.location_tags.all():
                location_tags.append({"id":tag.id , "tag":tag.tag})
            if hasattr(item, 'distance_from_origin'):
                places.append({
                    "id": place.id,
                    "name": place.name,
                    "details": place.details,
                    "duration_of_visit": place.duration_of_visit,
                    "trip_types": trip_types,
                    "location_tags": location_tags,
                    "distance_from_origin": distance_from_origin
                })
            else :
                places.append({
                    "id": place.id,
                    "name": place.name,
                    "details": place.details,
                    "duration_of_visit": place.duration_of_visit,
                    "trip_types": trip_types,
                    "location_tags": location_tags
                })

        return {
            "places": places
        }
